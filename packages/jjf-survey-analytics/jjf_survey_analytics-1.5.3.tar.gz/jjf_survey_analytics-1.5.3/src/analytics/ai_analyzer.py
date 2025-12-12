"""
AI-Powered Survey Response Analyzer
Uses Anthropic Claude Sonnet 4.5 for qualitative analysis
"""

import asyncio
import json
import logging
import os
import re
from functools import wraps
from typing import Any, Callable, Dict, List, TypeVar

# Python 3.9 compatibility - ParamSpec added in 3.10
try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI

# Configure logging
logger = logging.getLogger(__name__)

# Type variables for retry decorator
P = ParamSpec('P')
T = TypeVar('T')

# Load environment variables
load_dotenv(".env.local")


def retry_on_connection_error(
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    exceptions: tuple = (ConnectionError, TimeoutError, Exception)
):
    """
    Retry decorator for handling transient API connection errors.

    Implements exponential backoff to gracefully handle temporary OpenRouter API failures.
    Critical for production stability when dealing with remote API dependencies.

    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        backoff_factor: Exponential backoff multiplier in seconds (default: 2.0)
        exceptions: Tuple of exceptions to catch and retry (default: ConnectionError, TimeoutError, Exception)

    Returns:
        Decorated async function with retry logic

    Example:
        @retry_on_connection_error(max_retries=3, backoff_factor=2.0)
        async def api_call():
            return await client.chat.completions.create(...)

        # Retries on failure: attempt 1 (immediate), attempt 2 (after 2s), attempt 3 (after 4s)
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    # Don't retry on last attempt
                    if attempt == max_retries - 1:
                        logger.error(
                            f"Max retries ({max_retries}) reached for {func.__name__}",
                            extra={
                                "attempt": attempt + 1,
                                "error": str(e),
                                "error_type": type(e).__name__
                            },
                            exc_info=True
                        )
                        raise

                    # Calculate exponential backoff
                    wait_time = backoff_factor ** attempt

                    logger.warning(
                        f"Retry attempt {attempt + 1}/{max_retries} for {func.__name__} "
                        f"after {wait_time}s",
                        extra={
                            "attempt": attempt + 1,
                            "max_retries": max_retries,
                            "wait_time": wait_time,
                            "error": str(e)
                        }
                    )

                    await asyncio.sleep(wait_time)

            # Should never reach here, but satisfy type checker
            raise last_exception

        return wrapper
    return decorator


class AIAnalyzer:
    """AI-powered analyzer for qualitative survey responses."""

    def __init__(self):
        """Initialize OpenRouter client for Claude Sonnet 4.5."""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")

        # Synchronous client (for backward compatibility)
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            timeout=120.0,  # 2 minute timeout for API calls (increased for production)
        )

        # Async client (for concurrent operations)
        self.async_client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            timeout=120.0,
        )

        # Use Claude 3.5 Sonnet via OpenRouter
        self.model = "anthropic/claude-3.5-sonnet"
        print(f"[AI] Using OpenRouter with Claude 3.5 Sonnet: {self.model}")

    def _clean_json_response(self, content: str) -> str:
        """
        Clean common JSON formatting issues from AI responses.

        Args:
            content: Raw JSON string from AI response

        Returns:
            Cleaned JSON string
        """
        # Remove markdown code blocks if present
        content = re.sub(r"^```json\s*\n", "", content, flags=re.MULTILINE)
        content = re.sub(r"^```\s*\n", "", content, flags=re.MULTILINE)
        content = re.sub(r"\n```$", "", content)
        content = re.sub(r"```$", "", content)

        # Fix common issues with positive number formatting (JSON doesn't allow +0.3)
        content = re.sub(r":\s*\+(\d)", r": \1", content)

        # Fix unescaped quotes within strings (basic approach)
        # This handles common cases like: "text": "He said "hello" there"
        # Convert to: "text": "He said \"hello\" there"
        # Strategy: Find string values and escape internal quotes

        # Handle newlines within JSON string values by replacing with \n
        # This is a simplified approach - more complex patterns may need AST parsing

        # Remove trailing commas before closing braces/brackets (common JSON error)
        content = re.sub(r",(\s*[}\]])", r"\1", content)

        return content.strip()

    def _sanitize_survey_responses(self, responses_text: str) -> str:
        """
        Sanitize survey responses before sending to AI to prevent JSON issues.

        Args:
            responses_text: Raw survey response text

        Returns:
            Sanitized text safe for AI processing
        """
        if not responses_text:
            return responses_text

        # Escape problematic characters that might cause JSON issues
        # Replace actual newlines with space to prevent multi-line string issues
        sanitized = responses_text.replace("\n", " ")

        # Replace multiple spaces with single space
        sanitized = re.sub(r"\s+", " ", sanitized)

        # Escape quotes (though AI should handle this, pre-escaping helps)
        # We'll use a marker that AI can understand
        sanitized = sanitized.replace('"', "'")  # Convert double quotes to single quotes

        return sanitized

    def _validate_ai_response(
        self, ai_result: Dict[str, Any], input_responses: List[Dict[str, Any]], dimension: str
    ) -> Dict[str, Any]:
        """
        Validate AI-generated modifiers against actual input data to prevent hallucinations.

        This function ensures data integrity by:
        1. Verifying all respondent names exist in the input data
        2. Validating that original_text matches actual survey responses
        3. Flagging or removing hallucinated content
        4. Logging validation failures for audit trail

        Args:
            ai_result: AI-generated analysis with modifiers and summary
            input_responses: Original survey responses that were sent to AI
            dimension: Dimension name for logging

        Returns:
            Validated result with hallucinated content flagged or removed
        """
        if not ai_result or "modifiers" not in ai_result:
            return ai_result

        # Build lookup of valid respondents and their actual text responses
        valid_respondents = {r["respondent"]: r for r in input_responses}
        validated_modifiers = []
        validation_errors = []

        for idx, modifier in enumerate(ai_result["modifiers"]):
            respondent_name = modifier.get("respondent", "")
            original_text = modifier.get("original_text", "")
            is_valid = True

            # Check 1: Verify respondent exists in input data
            if respondent_name not in valid_respondents:
                validation_errors.append(
                    f"Modifier {idx}: Respondent '{respondent_name}' not found in input data - REMOVED"
                )
                logger.warning(
                    f"[VALIDATION] {dimension} - Modifier {idx}: Invalid respondent '{respondent_name}' - REMOVING from output"
                )
                is_valid = False

            # Check 2: Verify original_text matches one of the actual responses
            if is_valid and original_text:
                # Check if this text appears in ANY of the input responses
                text_found = False
                for response in input_responses:
                    actual_text = response.get("text", "")
                    # Check for exact match or substring match (AI may quote portions)
                    if original_text in actual_text or actual_text in original_text:
                        text_found = True
                        break

                if not text_found:
                    validation_errors.append(
                        f"Modifier {idx}: Original text does not match any input response - REMOVED"
                    )
                    logger.warning(
                        f"[VALIDATION] {dimension} - Modifier {idx}: Unverified quote from '{respondent_name}' - REMOVING from output"
                    )
                    is_valid = False

            # Only include modifiers that passed ALL validation checks
            if is_valid:
                validated_modifiers.append(modifier)
            else:
                logger.info(f"[VALIDATION] {dimension} - Removed hallucinated modifier {idx} (respondent: '{respondent_name}')")

        # Log validation summary
        removed_count = len(ai_result["modifiers"]) - len(validated_modifiers)
        if validation_errors:
            logger.error(
                f"[VALIDATION] {dimension} - Found {len(validation_errors)} validation errors. Removed {removed_count} hallucinated modifiers from output.",
                extra={
                    "dimension": dimension,
                    "total_modifiers": len(ai_result["modifiers"]),
                    "valid_modifiers": len(validated_modifiers),
                    "removed_modifiers": removed_count,
                    "validation_errors": validation_errors,
                    "error_count": len(validation_errors),
                },
            )
            # Add validation metadata to result
            ai_result["validation"] = {
                "status": "cleaned",
                "error_count": len(validation_errors),
                "removed_count": removed_count,
                "errors": validation_errors,
            }
        else:
            logger.info(f"[VALIDATION] {dimension} - All {len(validated_modifiers)} modifiers validated successfully (0 removed)")
            ai_result["validation"] = {
                "status": "passed",
                "error_count": 0,
                "removed_count": 0,
                "errors": [],
            }

        ai_result["modifiers"] = validated_modifiers
        return ai_result

    def _sanity_check_against_source(
        self,
        ai_result: Dict[str, Any],
        input_responses: List[Dict[str, Any]],
        dimension: str,
        org_name: str
    ) -> Dict[str, Any]:
        """
        Comprehensive sanity check comparing AI output against source data.

        This provides an additional verification layer beyond validation:
        1. Verifies all narrative content is grounded in actual responses
        2. Checks that summary doesn't contain hallucinated respondent names
        3. Provides confidence scoring based on data alignment
        4. Logs detailed audit trail for review

        Args:
            ai_result: AI-generated analysis result
            input_responses: Original survey responses
            dimension: Dimension name
            org_name: Organization name for logging

        Returns:
            Enhanced result with sanity_check metadata
        """
        sanity_check = {
            "status": "passed",
            "confidence_score": 1.0,
            "warnings": [],
            "source_data_summary": {},
        }

        # Build source data summary for comparison
        valid_respondents = [r["respondent"] for r in input_responses]
        valid_roles = list(set(r.get("role", "Unknown") for r in input_responses))

        sanity_check["source_data_summary"] = {
            "total_responses": len(input_responses),
            "unique_respondents": len(valid_respondents),
            "respondent_names": valid_respondents,
            "roles_represented": valid_roles,
        }

        # Check 1: Scan narrative content for respondent names
        summary_text = ai_result.get("summary", "") or ai_result.get("content", "") or ai_result.get("html", "")

        if summary_text:
            # Look for any names that aren't in our valid respondents
            # Pattern: capitalized words that look like names (2+ consecutive capitalized words)
            potential_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', summary_text)

            hallucinated_names = []
            for name in potential_names:
                # Check if this name is NOT in our valid respondents
                if name not in valid_respondents:
                    # Also check if it's not a common non-name phrase
                    common_phrases = [
                        "Technology", "Survey", "Staff", "Program", "Business", "Data",
                        "Management", "Infrastructure", "Organizational", "Culture",
                        "Cloud", "Security", "Mobile", "Remote", "Social Media"
                    ]
                    if not any(phrase in name for phrase in common_phrases):
                        hallucinated_names.append(name)

            if hallucinated_names:
                sanity_check["status"] = "warning"
                sanity_check["confidence_score"] = 0.7
                warning_msg = f"Potential hallucinated names in narrative: {', '.join(hallucinated_names)}"
                sanity_check["warnings"].append(warning_msg)
                logger.warning(
                    f"[SANITY CHECK] {org_name} - {dimension}: {warning_msg}. "
                    f"Valid respondents: {', '.join(valid_respondents)}"
                )

        # Check 2: Verify modifier count makes sense relative to input
        modifier_count = len(ai_result.get("modifiers", []))
        response_count = len(input_responses)

        if modifier_count > response_count * 2:
            # AI generated more than 2 modifiers per response - suspicious
            sanity_check["status"] = "warning"
            sanity_check["confidence_score"] = min(sanity_check["confidence_score"], 0.8)
            warning_msg = f"Modifier count ({modifier_count}) seems high for {response_count} responses"
            sanity_check["warnings"].append(warning_msg)
            logger.warning(f"[SANITY CHECK] {org_name} - {dimension}: {warning_msg}")

        # Check 3: Compare modifier respondents against source data
        modifier_respondents = [m.get("respondent") for m in ai_result.get("modifiers", [])]
        for resp in modifier_respondents:
            if resp and resp not in valid_respondents:
                sanity_check["status"] = "failed"
                sanity_check["confidence_score"] = 0.0
                error_msg = f"Modifier references unknown respondent: {resp}"
                sanity_check["warnings"].append(error_msg)
                logger.error(f"[SANITY CHECK] {org_name} - {dimension}: {error_msg}")

        # Log successful sanity check
        if sanity_check["status"] == "passed":
            logger.info(
                f"[SANITY CHECK] {org_name} - {dimension}: PASSED "
                f"(confidence: {sanity_check['confidence_score']:.2f}, "
                f"{modifier_count} modifiers from {response_count} responses)"
            )

        # Add sanity check metadata to result
        ai_result["sanity_check"] = sanity_check

        return ai_result

    def _validate_narrative_text(
        self, text: str, valid_respondents: List[str], source_context: str = ""
    ) -> str:
        """
        Validates narrative text for hallucinated respondent names.

        This function prevents AI hallucinations by:
        1. Scanning for capitalized word patterns that look like names
        2. Cross-checking against actual respondent list from survey data
        3. Removing hallucinated names from the text
        4. Logging all removals for audit trail

        Args:
            text: The AI-generated narrative text
            valid_respondents: List of actual respondent names from survey data
            source_context: Context for logging (e.g., "dimension insights", "aggregate summary")

        Returns:
            Cleaned text with hallucinated names removed
        """
        if not text or not valid_respondents:
            return text

        original_text = text

        # Common title words that precede names
        title_words = [
            "The", "Tech", "Chief", "Executive", "Director", "Manager", "Lead",
            "Senior", "Junior", "Staff", "Board", "Member", "Development",
            "Program", "Data", "Analyst", "Coordinator", "Specialist"
        ]

        # Pattern: Look for typical first name + last name patterns (2 consecutive capitalized words)
        # But exclude patterns that start with common title words
        potential_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', text)

        hallucinated_names = []

        for name in potential_names:
            # Check if this name is NOT in our valid respondents
            if name not in valid_respondents:
                name_words = name.split()

                # Skip if the first word is a title word (e.g., "Tech Lead", "Executive Director")
                if name_words[0] in title_words:
                    continue

                # Skip if it's a known title phrase
                common_titles = [
                    "Tech Lead", "Chief Executive", "Executive Director",
                    "Board Member", "Development Director", "Program Director",
                    "Staff Member", "Program Manager", "Data Analyst"
                ]
                if name in common_titles:
                    continue

                # Skip if all words are common business/tech terms
                common_words = [
                    "Technology", "Survey", "Staff", "Program", "Business", "Data",
                    "Management", "Infrastructure", "Organizational", "Culture",
                    "Cloud", "Security", "Mobile", "Remote", "Social", "Media",
                    "Google", "Microsoft", "Amazon", "Apple", "Systems"
                ]
                is_all_common_words = all(word in common_words for word in name_words)
                if is_all_common_words:
                    continue

                # This looks like a person's name that's not in our valid list
                hallucinated_names.append(name)
                # Remove the hallucinated name from text
                text = text.replace(name, "[respondent]")

        # Log any hallucinations detected
        if hallucinated_names:
            logger.warning(
                f"[NARRATIVE VALIDATION] {source_context}: Removed hallucinated names: "
                f"{', '.join(hallucinated_names)}. Valid respondents were: {', '.join(valid_respondents)}"
            )
            print(
                f"[AI] WARNING: Removed hallucinated names from {source_context}: "
                f"{', '.join(hallucinated_names)}"
            )

        return text

    def _parse_ai_json(self, content: str, dimension: str = "unknown") -> dict:
        """
        Parse JSON with multiple fallback strategies for robustness.

        Args:
            content: JSON string to parse
            dimension: Dimension name for logging

        Returns:
            Parsed dict or error dict with empty modifiers
        """
        # Strategy 1: Try parsing original content
        try:
            result = json.loads(content)
            logger.debug(f"Successfully parsed JSON for {dimension} (original)")
            return result
        except json.JSONDecodeError as e:
            logger.debug(f"Original parse failed for {dimension}: {e}")

        # Strategy 2: Try cleaned content
        try:
            cleaned = self._clean_json_response(content)
            result = json.loads(cleaned)
            logger.debug(f"Successfully parsed JSON for {dimension} (cleaned)")
            return result
        except json.JSONDecodeError as e:
            logger.debug(f"Cleaned parse failed for {dimension}: {e}")

        # Strategy 3: Try extracting JSON object using regex
        try:
            # Find the outermost JSON object
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                json_str = match.group(0)
                cleaned_json = self._clean_json_response(json_str)
                result = json.loads(cleaned_json)
                logger.debug(f"Successfully parsed JSON for {dimension} (regex extraction)")
                return result
        except (json.JSONDecodeError, AttributeError) as e:
            logger.debug(f"Regex extraction parse failed for {dimension}: {e}")

        # Strategy 4: Try to fix common string escaping issues manually
        try:
            # Replace unescaped newlines in strings
            fixed = re.sub(r"(?<!\\)\n", r"\\n", content)
            # Replace unescaped tabs
            fixed = re.sub(r"(?<!\\)\t", r"\\t", fixed)
            cleaned_fixed = self._clean_json_response(fixed)
            result = json.loads(cleaned_fixed)
            logger.debug(f"Successfully parsed JSON for {dimension} (escape fix)")
            return result
        except json.JSONDecodeError as e:
            logger.debug(f"Escape fix parse failed for {dimension}: {e}")

        # All strategies failed - log comprehensive error and return empty result
        logger.error(
            f"All JSON parsing strategies failed for {dimension}",
            extra={
                "dimension": dimension,
                "content_length": len(content),
                "content_preview": content[:200] if content else "None",
            },
        )

        # Return error dict with structured format
        return {
            "modifiers": [],
            "summary": "Error: Unable to parse AI response. JSON formatting issue detected.",
        }

    def analyze_dimension_responses(
        self, dimension: str, free_text_responses: List[Dict[str, Any]], org_name: str = "Unknown"
    ) -> Dict[str, Any]:
        """
        Analyze free text responses for a dimension to generate score modifiers.

        Args:
            dimension: Technology dimension name
            free_text_responses: List of dicts with 'respondent', 'role', 'text' keys
            org_name: Organization name for logging and sanity checks

        Returns:
            Dict with 'modifiers' list and 'summary' string
        """
        # Enhanced debug logging
        logger.info(f"Starting analysis for dimension: {dimension}")
        logger.debug(f"Response count: {len(free_text_responses) if free_text_responses else 0}")

        # Check for null/empty responses
        if not free_text_responses:
            logger.warning(f"No free text responses provided for {dimension}")
            return {"modifiers": [], "summary": "No free text responses provided for analysis."}

        # Validate response structure
        valid_responses = []
        for idx, response in enumerate(free_text_responses):
            if response is None:
                logger.warning(f"Null response at index {idx} for {dimension}")
                continue
            elif not isinstance(response, dict):
                logger.warning(
                    f"Invalid response type at index {idx} for {dimension}: {type(response)}"
                )
                continue

            # Log fields present
            logger.debug(f"Response {idx} fields: {list(response.keys())}")

            # Validate required fields and handle None values
            role = response.get("role")
            respondent = response.get("respondent")
            text = response.get("text")

            if role is None or respondent is None or text is None:
                logger.warning(
                    f"Response {idx} has None values - role: {role}, respondent: {respondent}, text: {text is not None}"
                )
                continue

            # Ensure text is not empty
            if not str(text).strip():
                logger.warning(f"Response {idx} has empty text field")
                continue

            valid_responses.append(response)

        if not valid_responses:
            logger.warning(f"No valid responses after validation for {dimension}")
            return {"modifiers": [], "summary": "No valid responses to analyze"}

        # Prepare context for AI with safe string handling
        responses_text = "\n\n".join(
            [
                f"[{str(r.get('role', 'Unknown'))} - {str(r.get('respondent', 'Unknown'))}]:\n{str(r.get('text', 'No response'))}"
                for r in valid_responses
            ]
        )

        # Validate responses_text
        if not responses_text or responses_text.strip() == "":
            logger.warning(f"Empty responses text generated for {dimension}")
            return {"modifiers": [], "summary": "No valid responses to analyze"}

        logger.debug(f"Generated responses text length: {len(responses_text)} chars")
        logger.debug(f"First 200 chars of responses text: {responses_text[:200]}")

        prompt = f"""Analyze the following free text survey responses for the "{dimension}" technology dimension.

Your task is to identify qualitative factors that ADJUST the quantitative scores UP or DOWN based on additional context.

**CRITICAL SCORING RULES:**
- POSITIVE modifiers (+0.1 to +1.0): Capabilities, strengths, or strategic advantages BEYOND what quantitative scores capture
- NEGATIVE modifiers (-0.1 to -1.0): Gaps, challenges, or weaknesses NOT REFLECTED in quantitative scores
- ZERO modifiers (0.0): Neutral factual statements that simply describe current state without indicating strength or weakness

**Examples of Correct Scoring:**
- "We distribute content digitally through our website and social media" → 0.0 (neutral factual description)
- "Our innovative multi-platform distribution strategy exceeds industry standards" → +0.5 to +0.7 (clear positive capability)
- "We struggle with digital distribution due to outdated systems" → -0.5 to -0.7 (clear gap/challenge)
- "Staff purchase software without approval or oversight" → -0.3 to -0.5 (governance gap)

**What NOT to penalize:**
- Factual descriptions of current capabilities (unless explicitly problematic)
- Neutral technical statements
- Descriptions of normal operational activities

Survey Responses:
{responses_text}

Please provide:
1. Score Modifiers: Identify specific factors mentioned that warrant score adjustments
   - Use POSITIVE values (+) for strengths and capabilities that exceed baseline expectations
   - Use NEGATIVE values (-) for gaps, challenges, and weaknesses below baseline
   - Use ZERO (0.0) for neutral factual descriptions
   - Include the respondent name and role for each modifier
   - Explain the reasoning for each modifier

2. Summary: Brief overview of common themes and insights

**IMPORTANT JSON FORMATTING:**
- Return VALID JSON only (no markdown code blocks)
- Escape all quotes within string values using backslash
- Do NOT include literal newlines in string values - use spaces instead
- Use numeric values without + prefix (0.5 not +0.5)
- Keep all text on single lines within JSON strings

Return your analysis in this JSON format:
{{
  "modifiers": [
    {{
      "respondent": "Name",
      "role": "CEO/Tech Lead/Staf",
      "value": 0.0,
      "factor": "Brief description of the factor",
      "reasoning": "Why this warrants a score adjustment (or why it is neutral)",
      "original_text": "The exact original comment text that led to this modifier"
    }}
  ],
  "summary": "Concise 2-3 paragraph summary of qualitative insights. STRICT LIMIT: Maximum 250 words total. Be succinct and focus on key points only."
}}

Focus on:
- Concrete capabilities or gaps mentioned BEYOND the quantitative scores
- Context that explains WHY scores should be adjusted UP or DOWN
- Strategic advantages (positive modifiers) or challenges (negative modifiers)
- Governance, process, or cultural factors affecting technology effectiveness

IMPORTANT: Keep summary under 250 words. Prioritize the most critical insights and be concise.
"""

        try:
            print(f"[AI] Making API call for dimension analysis: {dimension}")
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert technology assessment analyst. Analyze survey responses to identify qualitative factors that should adjust quantitative technology maturity scores.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            print(f"[AI] Received response for dimension analysis: {dimension}")

            # Check for null response
            if not response or not response.choices:
                logger.error(f"Claude API returned null or empty response for {dimension}")
                return {"modifiers": [], "summary": "Error: API returned empty response"}

            content = response.choices[0].message.content

            # Check for null content
            if content is None:
                logger.error(f"Claude API returned null content for {dimension}")
                return {"modifiers": [], "summary": "Error: API returned empty response"}

            logger.debug(f"Raw AI response for {dimension} - Length: {len(content)} chars")
            logger.debug(f"Raw content (first 500 chars):\n{content[:500]}")

            # Extract JSON from markdown code blocks if present
            original_content = content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
                logger.debug(f"Extracted from ```json block - New length: {len(content)}")
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                logger.debug(f"Extracted from ``` block - New length: {len(content)}")

            # Check if extraction resulted in empty content
            if not content or content.strip() == "":
                logger.error(f"Content became empty after extraction for {dimension}")
                logger.debug(f"Original content was:\n{original_content}")
                return {"modifiers": [], "summary": "Error: Could not extract JSON from response"}

            logger.debug(f"Content to parse (first 300 chars):\n{content[:300]}")

            # Use robust JSON parsing with multiple fallback strategies
            result = self._parse_ai_json(content, dimension)

            # Validate result structure
            if not isinstance(result, dict):
                logger.error(f"Parsed result is not a dict for {dimension}: {type(result)}")
                return {"modifiers": [], "summary": "Error: Invalid response format"}

            # Ensure required keys exist
            if "modifiers" not in result:
                result["modifiers"] = []
            if "summary" not in result:
                result["summary"] = "AI analysis completed."

            # CRITICAL: Validate AI response against actual input data to prevent hallucinations (JJF-11 fix)
            result = self._validate_ai_response(result, valid_responses, dimension)

            # JJF-11: Additional sanity check comparing AI output to source data
            result = self._sanity_check_against_source(result, valid_responses, dimension, org_name)

            # JJF-42: Validate modifiers have reasoning for non-zero values
            for i, modifier in enumerate(result.get('modifiers', [])):
                if modifier.get('value', 0) != 0:
                    if not modifier.get('reasoning'):
                        logger.warning(
                            f"AI returned modifier without reasoning for {dimension}: {modifier}"
                        )
                        # Add default reasoning to prevent validation failure downstream
                        modifier['reasoning'] = f"Adjustment based on {modifier.get('factor', 'unspecified factor')}"

                    if not modifier.get('original_text'):
                        logger.warning(
                            f"AI returned modifier without original_text for {dimension}: {modifier}"
                        )
                        modifier['original_text'] = "[Citation not provided by AI]"

            logger.info(f"Successfully parsed JSON for {dimension}")
            return result

        except Exception as e:
            # Generic error handler for non-JSON errors
            logger.error(
                f"Unexpected error analyzing dimension responses for {dimension}",
                extra={
                    "dimension": dimension,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "response_count": len(free_text_responses),
                },
                exc_info=True,  # Include full traceback
            )

            return {"modifiers": [], "summary": f"Error analyzing responses: {str(e)}"}

    @retry_on_connection_error(max_retries=3, backoff_factor=2.0)
    async def _analyze_with_retry(
        self, dimension: str, prompt: str, org_name: str = "Unknown"
    ) -> Dict[str, Any]:
        """
        Execute OpenRouter API call with automatic retry on connection errors.

        This method wraps the actual API call with exponential backoff retry logic:
        - Attempt 1: Immediate
        - Attempt 2: After 2 seconds
        - Attempt 3: After 4 seconds

        Args:
            dimension: Technology dimension name
            prompt: Full prompt to send to AI
            org_name: Organization name for logging

        Returns:
            Dict with 'modifiers' list and 'summary' string

        Raises:
            Exception: After all retries exhausted
        """
        print(f"[AI] Making ASYNC API call for dimension analysis: {dimension}")
        response = await self.async_client.chat.completions.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technology assessment analyst. Analyze survey responses to identify qualitative factors that should adjust quantitative technology maturity scores.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        print(f"[AI] Received ASYNC response for dimension analysis: {dimension}")

        # Check for null response
        if not response or not response.choices:
            logger.error(f"Claude API returned null or empty response for {dimension}")
            raise ValueError("API returned empty response")

        content = response.choices[0].message.content

        # Check for null content
        if content is None:
            logger.error(f"Claude API returned null content for {dimension}")
            raise ValueError("API returned empty response")

        logger.debug(f"Raw AI response for {dimension} - Length: {len(content)} chars")
        logger.debug(f"Raw content (first 500 chars):\n{content[:500]}")

        # Extract JSON from markdown code blocks if present
        original_content = content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
            logger.debug(f"Extracted from ```json block - New length: {len(content)}")
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            logger.debug(f"Extracted from ``` block - New length: {len(content)}")

        # Check if extraction resulted in empty content
        if not content or content.strip() == "":
            logger.error(f"Content became empty after extraction for {dimension}")
            logger.debug(f"Original content was:\n{original_content}")
            raise ValueError("Could not extract JSON from response")

        logger.debug(f"Content to parse (first 300 chars):\n{content[:300]}")

        # Use robust JSON parsing with multiple fallback strategies
        result = self._parse_ai_json(content, dimension)

        # Validate result structure
        if not isinstance(result, dict):
            logger.error(f"Parsed result is not a dict for {dimension}: {type(result)}")
            raise ValueError("Invalid response format")

        # Ensure required keys exist
        if "modifiers" not in result:
            result["modifiers"] = []
        if "summary" not in result:
            result["summary"] = "AI analysis completed."

        return result

    async def analyze_dimension_responses_async(
        self, dimension: str, free_text_responses: List[Dict[str, Any]], org_name: str = "Unknown"
    ) -> Dict[str, Any]:
        """
        Async version: Analyze free text responses for a dimension to generate score modifiers.

        Args:
            dimension: Technology dimension name
            free_text_responses: List of dicts with 'respondent', 'role', 'text' keys
            org_name: Organization name for logging and sanity checks

        Returns:
            Dict with 'modifiers' list and 'summary' string
        """
        # Enhanced debug logging
        logger.info(f"[ASYNC] Starting analysis for dimension: {dimension}")
        logger.debug(f"Response count: {len(free_text_responses) if free_text_responses else 0}")

        # Check for null/empty responses
        if not free_text_responses:
            logger.warning(f"No free text responses provided for {dimension}")
            return {"modifiers": [], "summary": "No free text responses provided for analysis."}

        # Validate response structure
        valid_responses = []
        for idx, response in enumerate(free_text_responses):
            if response is None:
                logger.warning(f"Null response at index {idx} for {dimension}")
                continue
            elif not isinstance(response, dict):
                logger.warning(
                    f"Invalid response type at index {idx} for {dimension}: {type(response)}"
                )
                continue

            # Log fields present
            logger.debug(f"Response {idx} fields: {list(response.keys())}")

            # Validate required fields and handle None values
            role = response.get("role")
            respondent = response.get("respondent")
            text = response.get("text")

            if role is None or respondent is None or text is None:
                logger.warning(
                    f"Response {idx} has None values - role: {role}, respondent: {respondent}, text: {text is not None}"
                )
                continue

            # Ensure text is not empty
            if not str(text).strip():
                logger.warning(f"Response {idx} has empty text field")
                continue

            valid_responses.append(response)

        if not valid_responses:
            logger.warning(f"No valid responses after validation for {dimension}")
            return {"modifiers": [], "summary": "No valid responses to analyze"}

        # Prepare context for AI with safe string handling
        responses_text = "\n\n".join(
            [
                f"[{str(r.get('role', 'Unknown'))} - {str(r.get('respondent', 'Unknown'))}]:\n{str(r.get('text', 'No response'))}"
                for r in valid_responses
            ]
        )

        # Validate responses_text
        if not responses_text or responses_text.strip() == "":
            logger.warning(f"Empty responses text generated for {dimension}")
            return {"modifiers": [], "summary": "No valid responses to analyze"}

        logger.debug(f"Generated responses text length: {len(responses_text)} chars")
        logger.debug(f"First 200 chars of responses text: {responses_text[:200]}")

        prompt = f"""Analyze the following free text survey responses for the "{dimension}" technology dimension.

Your task is to identify qualitative factors that ADJUST the quantitative scores UP or DOWN based on additional context.

**CRITICAL SCORING RULES:**
- POSITIVE modifiers (+0.1 to +1.0): Capabilities, strengths, or strategic advantages BEYOND what quantitative scores capture
- NEGATIVE modifiers (-0.1 to -1.0): Gaps, challenges, or weaknesses NOT REFLECTED in quantitative scores
- ZERO modifiers (0.0): Neutral factual statements that simply describe current state without indicating strength or weakness

**Examples of Correct Scoring:**
- "We distribute content digitally through our website and social media" → 0.0 (neutral factual description)
- "Our innovative multi-platform distribution strategy exceeds industry standards" → +0.5 to +0.7 (clear positive capability)
- "We struggle with digital distribution due to outdated systems" → -0.5 to -0.7 (clear gap/challenge)
- "Staff purchase software without approval or oversight" → -0.3 to -0.5 (governance gap)

**What NOT to penalize:**
- Factual descriptions of current capabilities (unless explicitly problematic)
- Neutral technical statements
- Descriptions of normal operational activities

Survey Responses:
{responses_text}

Please provide:
1. Score Modifiers: Identify specific factors mentioned that warrant score adjustments
   - Use POSITIVE values (+) for strengths and capabilities that exceed baseline expectations
   - Use NEGATIVE values (-) for gaps, challenges, and weaknesses below baseline
   - Use ZERO (0.0) for neutral factual descriptions
   - Include the respondent name and role for each modifier
   - Explain the reasoning for each modifier

2. Summary: Brief overview of common themes and insights

**IMPORTANT JSON FORMATTING:**
- Return VALID JSON only (no markdown code blocks)
- Escape all quotes within string values using backslash
- Do NOT include literal newlines in string values - use spaces instead
- Use numeric values without + prefix (0.5 not +0.5)
- Keep all text on single lines within JSON strings

Return your analysis in this JSON format:
{{
  "modifiers": [
    {{
      "respondent": "Name",
      "role": "CEO/Tech Lead/Staf",
      "value": 0.0,
      "factor": "Brief description of the factor",
      "reasoning": "Why this warrants a score adjustment (or why it is neutral)",
      "original_text": "The exact original comment text that led to this modifier"
    }}
  ],
  "summary": "Concise 2-3 paragraph summary of qualitative insights. STRICT LIMIT: Maximum 250 words total. Be succinct and focus on key points only."
}}

Focus on:
- Concrete capabilities or gaps mentioned BEYOND the quantitative scores
- Context that explains WHY scores should be adjusted UP or DOWN
- Strategic advantages (positive modifiers) or challenges (negative modifiers)
- Governance, process, or cultural factors affecting technology effectiveness

IMPORTANT: Keep summary under 250 words. Prioritize the most critical insights and be concise.
"""

        try:
            # Call API with retry logic
            result = await self._analyze_with_retry(dimension, prompt, org_name)

            # CRITICAL: Validate AI response against actual input data to prevent hallucinations (JJF-11 fix)
            result = self._validate_ai_response(result, valid_responses, dimension)

            # JJF-11: Additional sanity check comparing AI output to source data
            result = self._sanity_check_against_source(result, valid_responses, dimension, org_name)

            # JJF-42: Validate modifiers have reasoning for non-zero values
            for i, modifier in enumerate(result.get('modifiers', [])):
                if modifier.get('value', 0) != 0:
                    if not modifier.get('reasoning'):
                        logger.warning(
                            f"AI returned modifier without reasoning for {dimension}: {modifier}"
                        )
                        # Add default reasoning to prevent validation failure downstream
                        modifier['reasoning'] = f"Adjustment based on {modifier.get('factor', 'unspecified factor')}"

                    if not modifier.get('original_text'):
                        logger.warning(
                            f"AI returned modifier without original_text for {dimension}: {modifier}"
                        )
                        modifier['original_text'] = "[Citation not provided by AI]"

            logger.info(f"Successfully parsed JSON for {dimension}")
            return result

        except Exception as e:
            # Final fallback after all retries exhausted
            error_msg = str(e)
            if "retries" in error_msg.lower() or isinstance(e, (ConnectionError, TimeoutError)):
                logger.error(
                    f"All retries exhausted for {dimension} analysis",
                    extra={
                        "dimension": dimension,
                        "error": error_msg,
                        "org_name": org_name
                    },
                    exc_info=True
                )
                return {
                    "modifiers": [],
                    "summary": f"Error analyzing responses: Connection error (retries exhausted)"
                }
            else:
                # Generic error handler for non-connection errors
                logger.error(
                    f"Unexpected error analyzing dimension responses for {dimension}",
                    extra={
                        "dimension": dimension,
                        "error_type": type(e).__name__,
                        "error_message": error_msg,
                        "response_count": len(free_text_responses),
                    },
                    exc_info=True,
                )
                return {"modifiers": [], "summary": f"Error analyzing responses: {error_msg}"}

    def summarize_all_feedback(self, all_responses: List[Dict[str, Any]]) -> str:
        """
        Generate a comprehensive summary of all free text feedback across organizations.

        Args:
            all_responses: List of all free text responses across all orgs

        Returns:
            Summary string for the home page
        """
        if not all_responses:
            logger.info("No free text feedback available for summarization")
            return "No free text feedback available for analysis."

        # Validate and filter responses
        valid_responses = []
        for idx, r in enumerate(all_responses):
            if r is None:
                logger.warning(f"Null response at index {idx} in summarize_all_feedback")
                continue
            if not isinstance(r, dict):
                logger.warning(
                    f"Invalid response type at index {idx} in summarize_all_feedback: {type(r)}"
                )
                continue

            # Ensure required fields exist
            if not r.get("organization") or not r.get("text"):
                logger.debug(f"Response {idx} missing organization or text field")
                continue

            valid_responses.append(r)

        if not valid_responses:
            logger.warning("No valid responses after validation in summarize_all_feedback")
            return "No valid feedback available for analysis."

        # Group by organization
        org_responses = {}
        for r in valid_responses:
            org = str(r.get("organization", "Unknown"))
            if org not in org_responses:
                org_responses[org] = []
            org_responses[org].append(r)

        logger.info(
            f"Summarizing feedback from {len(org_responses)} organizations ({len(valid_responses)} total responses)"
        )

        # Prepare summary context with safe string handling
        summary_text = f"Analyzing {len(valid_responses)} free text responses from {len(org_responses)} organizations:\n\n"

        for org, responses in org_responses.items():
            summary_text += f"[{org}] - {len(responses)} responses\n"
            for r in responses[:3]:  # Limit to first 3 per org for token efficiency
                role = str(r.get("role", "Unknown"))
                text = str(r.get("text", ""))[:150] if r.get("text") else ""
                summary_text += f"  {role}: {text}...\n"

        prompt = f"""Analyze the following free text survey feedback from multiple nonprofit organizations about their technology readiness.

{summary_text}

Provide a concise 2-3 paragraph summary highlighting:
1. Common themes and patterns across organizations
2. Key challenges or gaps mentioned
3. Notable strengths or innovative approaches
4. Overall sentiment about technology readiness

Keep the summary professional, actionable, and suitable for a dashboard overview.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=500,
                temperature=0.4,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technology consultant summarizing feedback from nonprofit organizations about their technology capabilities.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error summarizing feedback: {e}")
            return f"Error generating summary: {str(e)}"

    def consolidate_text(self, text: str, max_chars: int = 150) -> str:
        """
        Consolidate long text into concise version using LLM.

        Args:
            text: Original text to consolidate
            max_chars: Target character count (approximate)

        Returns:
            Consolidated text that preserves key insights
        """
        # Handle None or empty text
        if text is None:
            logger.warning("consolidate_text called with None text")
            return ""

        if not isinstance(text, str):
            logger.warning(f"consolidate_text called with non-string: {type(text)}")
            text = str(text)

        if not text.strip():
            logger.warning("consolidate_text called with empty text")
            return ""

        # If already short enough, return as-is
        if len(text) <= max_chars:
            return text

        prompt = f"""Consolidate this text to approximately {max_chars} characters while preserving key insights:

Original text ({len(text)} chars):
{text}

Requirements:
- Keep essential information and insights
- Remove redundant phrases and filler words
- Use concise, professional language
- Maintain the same tone and meaning
- Target length: {max_chars} characters (strict maximum)

Return ONLY the consolidated text, no explanations or metadata:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=min(
                    250, int(max_chars * 0.4)
                ),  # Dynamic token limit (1 token ≈ 2.5 chars), capped at 250
                temperature=0.3,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert editor who consolidates verbose text into concise summaries while preserving key insights. Return only the consolidated text.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            consolidated = response.choices[0].message.content.strip()

            # Remove quotes if LLM added them
            if consolidated.startswith('"') and consolidated.endswith('"'):
                consolidated = consolidated[1:-1]
            if consolidated.startswith("'") and consolidated.endswith("'"):
                consolidated = consolidated[1:-1]

            # Fallback: if still too long, hard truncate
            if len(consolidated) > max_chars + 20:
                consolidated = consolidated[:max_chars] + "..."

            return consolidated

        except Exception as e:
            print(f"Error consolidating text: {e}")
            # Fallback: simple truncation
            return text[:max_chars] + "..." if len(text) > max_chars else text

    def _is_valid_insight(self, text: str) -> bool:
        """
        Validate that AI-generated insight is readable and not garbled.

        Args:
            text: AI-generated text to validate

        Returns:
            True if text is valid, False if garbled/corrupted
        """
        if not text or len(text) < 20:
            return False

        # Check for garbled text indicators (special characters that shouldn't be in prose)
        garbled_indicators = ["$", "{", "}", "(", ")", "[", "]", "<", ">"]
        if any(char in text for char in garbled_indicators):
            return False

        # Check for excessive non-ASCII characters (gibberish detection)
        non_ascii_count = sum(1 for c in text if ord(c) > 127)
        if non_ascii_count > len(text) * 0.3:  # More than 30% non-ASCII
            return False

        # Check for minimum word count (at least 10 words)
        words = text.split()
        if len(words) < 10:
            return False

        return True

    def _get_fallback_insight(self, dimension: str) -> str:
        """
        Get fallback text when AI generation fails or returns garbled text.

        Args:
            dimension: Technology dimension name

        Returns:
            Fallback insight text
        """
        fallback_insights = {
            "Program Technology": "Based on survey responses, your organization shows varying levels of technology integration in program delivery. Consider reviewing staff feedback to identify specific areas for enhancement.",
            "Business Systems": "Survey responses indicate opportunities to enhance business systems integration and accessibility. Focus on ensuring all stakeholders have the tools they need for effective operations.",
            "Data Management": "Staff feedback highlights both strengths and areas for improvement in data management capabilities. Consider developing a unified data strategy to address identified gaps.",
            "Infrastructure": "Technology infrastructure shows a mix of established practices and areas requiring attention. Review stakeholder input to prioritize infrastructure improvements.",
            "Organizational Culture": "Responses reflect evolving technology culture with opportunities for strategic development. Consider initiatives to build technology confidence across all team levels.",
        }

        return fallback_insights.get(
            dimension,
            "Survey responses provide valuable insights for this dimension. Review detailed feedback to identify specific improvement opportunities.",
        )

    def _validate_grounding(self, ai_text: str, source_responses: List[Dict[str, Any]], dimension: str) -> bool:
        """
        Validate that AI-generated text is grounded in actual survey responses.

        This prevents AI hallucinations by:
        1. Checking for generic phrases not supported by data
        2. Verifying AI output contains specific terms from source responses
        3. Calculating semantic overlap between AI output and source data

        Args:
            ai_text: AI-generated narrative text
            source_responses: Original survey responses that should ground the text
            dimension: Dimension name for logging

        Returns:
            True if text is well-grounded, False if too generic
        """
        if not ai_text or not source_responses:
            logger.warning(f"[GROUNDING] {dimension}: Empty input to validation")
            return False

        # Check 1: Detect generic advice phrases not grounded in data
        generic_phrases = [
            "consider", "should improve", "it's important", "may want to",
            "could benefit from", "recommend", "best practice", "typical",
            "generally", "often", "usually", "suggested", "advisable",
            "might help", "worth exploring", "good idea", "potential to"
        ]

        ai_text_lower = ai_text.lower()
        generic_count = sum(1 for phrase in generic_phrases if phrase in ai_text_lower)

        if generic_count > 2:
            logger.warning(
                f"[GROUNDING] {dimension}: High generic phrase count ({generic_count}) - "
                f"text appears ungrounded: {ai_text[:100]}"
            )
            return False

        # Check 2: Extract meaningful terms from source responses (nouns, verbs, key phrases)
        source_text = " ".join([str(r.get("text", "")) for r in source_responses]).lower()

        # Extract words longer than 4 characters (exclude common stop words)
        stop_words = {
            "the", "and", "for", "with", "this", "that", "from", "have", "been",
            "they", "their", "there", "what", "when", "where", "which", "about"
        }

        source_terms = set()
        for word in source_text.split():
            # Clean punctuation
            cleaned_word = word.strip('.,!?;:"()[]')
            if len(cleaned_word) > 4 and cleaned_word not in stop_words:
                source_terms.add(cleaned_word)

        # Check how many source terms appear in AI output
        ai_terms_found = sum(1 for term in source_terms if term in ai_text_lower)
        overlap_ratio = ai_terms_found / len(source_terms) if source_terms else 0

        # Require at least 15% overlap with source terminology
        if overlap_ratio < 0.15:
            logger.warning(
                f"[GROUNDING] {dimension}: Low semantic overlap ({overlap_ratio:.1%}) - "
                f"AI output doesn't reflect source terminology. "
                f"Found {ai_terms_found}/{len(source_terms)} source terms"
            )
            return False

        # Check 3: Verify AI output references specific feedback concepts
        # Count specific descriptive phrases vs. generic recommendations
        specific_indicators = [
            "mentioned", "noted", "indicated", "described", "reported",
            "feedback shows", "responses highlight", "staff expressed",
            "team shared", "currently", "existing", "in place"
        ]

        specific_count = sum(1 for phrase in specific_indicators if phrase in ai_text_lower)

        # Require at least one specific indicator if text is longer than 100 chars
        if len(ai_text) > 100 and specific_count == 0 and generic_count > 0:
            logger.warning(
                f"[GROUNDING] {dimension}: No specific indicators found, but {generic_count} "
                f"generic phrases present - appears to be advice rather than data summary"
            )
            return False

        # Passed all checks
        logger.info(
            f"[GROUNDING] {dimension}: Validation PASSED - "
            f"overlap: {overlap_ratio:.1%}, specific: {specific_count}, generic: {generic_count}"
        )
        return True

    def generate_dimension_insights(
        self, dimension_responses: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, str]:
        """
        Generate grantee-friendly qualitative summaries for each dimension.

        Args:
            dimension_responses: Dict mapping dimension names to lists of free text responses

        Returns:
            Dict mapping dimension names to 2-3 sentence summaries
        """
        insights = {}

        for dimension, responses in dimension_responses.items():
            if not responses:
                logger.debug(f"No responses for dimension insights: {dimension}")
                continue

            # Validate and filter responses, collect valid respondent names
            valid_responses = []
            valid_respondent_names = []

            for idx, r in enumerate(responses):
                if r is None:
                    logger.warning(
                        f"Null response at index {idx} in dimension insights for {dimension}"
                    )
                    continue
                if not isinstance(r, dict):
                    logger.warning(
                        f"Invalid response type in dimension insights for {dimension}: {type(r)}"
                    )
                    continue

                role = r.get("role")
                respondent = r.get("respondent")
                text = r.get("text")

                if role is None or respondent is None or text is None:
                    logger.warning(
                        f"Response {idx} has None values in dimension insights for {dimension}"
                    )
                    continue

                if not str(text).strip():
                    logger.warning(
                        f"Response {idx} has empty text in dimension insights for {dimension}"
                    )
                    continue

                valid_responses.append(r)
                # Collect unique respondent names for validation
                if respondent and respondent not in valid_respondent_names:
                    valid_respondent_names.append(str(respondent))

            if not valid_responses:
                logger.warning(
                    f"No valid responses after validation for dimension insights: {dimension}"
                )
                continue

            # Prepare responses text with safe string handling
            responses_text = "\n\n".join(
                [
                    f"[{str(r.get('role', 'Unknown'))} - {str(r.get('respondent', 'Unknown'))}]:\n{str(r.get('text', 'No response'))}"
                    for r in valid_responses
                ]
            )

            if not responses_text or responses_text.strip() == "":
                logger.warning(f"Empty responses text for dimension insights: {dimension}")
                continue

            # JJF-11: Enhanced prompt with explicit grounding constraints
            prompt = f"""Analyze the following survey responses for {dimension} and write a 2-3 sentence summary for the grantee organization.

Survey Responses:
{responses_text}

**CRITICAL GROUNDING REQUIREMENTS (JJF-11):**
- Base your summary ONLY on the specific responses provided above
- Do NOT use generic phrases or assumptions not present in the responses
- Quote or reference specific feedback from the responses
- If responses are insufficient to make a conclusion, say so explicitly
- Use phrases like "mentioned", "noted", "indicated" to show data grounding
- NEVER include generic advice like "consider", "should improve", "it's important" unless directly stated in responses

Write a friendly, constructive summary that:
- Highlights specific strengths mentioned in the responses
- Notes areas for improvement mentioned in the responses (in supportive tone)
- Identifies common themes FROM THE RESPONSES
- Uses "your team" or "your organization" language
- Avoids jargon and technical language where possible

Return ONLY the summary text, no JSON or formatting."""

            max_retries = 3  # JJF-11: Increased from 2 to 3 for grounding validation
            retry_count = 0
            summary = None

            while retry_count < max_retries and not summary:
                try:
                    print(
                        f"[AI] Generating dimension insight for: {dimension} (attempt {retry_count + 1}/{max_retries})"
                    )
                    response = self.client.chat.completions.create(
                        model=self.model,
                        max_tokens=200,
                        temperature=0.4,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a friendly technology consultant providing constructive feedback to nonprofit organizations. Write in a supportive, grantee-friendly tone. Use only standard English text without special characters or symbols. **CRITICAL**: You must base your analysis exclusively on the provided responses. Never use generic advice or best practices not mentioned in the responses. Always reference specific content from the survey data.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                    )
                    generated_text = response.choices[0].message.content.strip()

                    # Remove quotes if present
                    if generated_text.startswith('"') and generated_text.endswith('"'):
                        generated_text = generated_text[1:-1]
                    if generated_text.startswith("'") and generated_text.endswith("'"):
                        generated_text = generated_text[1:-1]

                    # Validate narrative text for hallucinated respondent names
                    validated_text = self._validate_narrative_text(
                        generated_text,
                        valid_respondent_names,
                        source_context=f"dimension insights: {dimension}"
                    )

                    # JJF-11: Validate grounding before checking insight quality
                    is_grounded = self._validate_grounding(validated_text, valid_responses, dimension)

                    if not is_grounded:
                        print(
                            f"[AI] WARNING: Generated text failed grounding check for {dimension}. "
                            f"Text appears too generic: {validated_text[:100]}"
                        )
                        retry_count += 1
                        if retry_count < max_retries:
                            print(f"[AI] Retrying with stronger grounding constraints for {dimension}...")
                        continue

                    # Validate the cleaned text quality
                    if self._is_valid_insight(validated_text):
                        summary = validated_text
                        print(
                            f"[AI] Successfully generated valid, grounded insight for {dimension}: {len(summary)} chars"
                        )
                    else:
                        print(
                            f"[AI] WARNING: Generated text failed quality validation for {dimension}. Text: {validated_text[:100]}"
                        )
                        retry_count += 1
                        if retry_count < max_retries:
                            print(f"[AI] Retrying generation for {dimension}...")

                except Exception as e:
                    print(
                        f"[AI] Error generating insight for {dimension} (attempt {retry_count + 1}): {e}"
                    )
                    retry_count += 1

            # Use validated summary or fallback
            if summary:
                insights[dimension] = summary
            else:
                fallback = self._get_fallback_insight(dimension)
                insights[dimension] = fallback
                print(
                    f"[AI] Using fallback insight for {dimension} after {retry_count} failed attempts"
                )

        return insights

    async def generate_organization_summary_async(
        self,
        org_name: str,
        dimension_summaries: Dict[str, Dict[str, Any]]
    ) -> str:
        """
        Generate organization-level summary from all dimension analyses.

        Synthesizes insights across all 5 dimensions to create a comprehensive
        organization-level qualitative summary.

        Args:
            org_name: Organization name
            dimension_summaries: Dict mapping dimension names to analysis results
                {
                    "Program Technology": {"summary": "...", "themes": [...], "score_modifiers": [...]},
                    "Business Systems": {...},
                    ...
                }

        Returns:
            Organization-level summary (3-5 paragraphs synthesizing all dimensions)
        """
        logger.info(f"[AI] Generating organization summary for {org_name}")

        # Build comprehensive context from all dimension analyses
        context_parts = []
        for dimension, analysis in dimension_summaries.items():
            # Defensive type checking: ensure analysis is dict, not nested data
            if not isinstance(analysis, dict):
                logger.warning(
                    f"[ORG SUMMARY] {org_name} - Invalid analysis type for {dimension}: {type(analysis)}"
                )
                continue

            # Extract data, handling potential double-nesting
            # If analysis has a 'data' key, use that; otherwise use analysis directly
            if "data" in analysis and isinstance(analysis["data"], dict):
                logger.debug(f"[ORG SUMMARY] {org_name} - {dimension}: Found nested 'data' key, extracting")
                analysis_data = analysis["data"]
            else:
                analysis_data = analysis

            # Extract fields with type safety
            summary = analysis_data.get("summary", "No analysis available")
            themes = analysis_data.get("themes", [])
            modifiers = analysis_data.get("score_modifiers", [])

            # Ensure summary is a string
            if not isinstance(summary, str):
                logger.warning(
                    f"[ORG SUMMARY] {org_name} - {dimension}: summary is {type(summary)}, converting to string"
                )
                summary = str(summary) if summary else "No analysis available"

            # Ensure themes is a list
            if not isinstance(themes, list):
                logger.warning(
                    f"[ORG SUMMARY] {org_name} - {dimension}: themes is {type(themes)}, converting to list"
                )
                themes = []

            # Ensure modifiers is a list
            if not isinstance(modifiers, list):
                logger.warning(
                    f"[ORG SUMMARY] {org_name} - {dimension}: modifiers is {type(modifiers)}, converting to list"
                )
                modifiers = []

            context_parts.append(f"**{dimension}:**")
            context_parts.append(f"Summary: {summary}")
            if themes:
                # Ensure all themes are strings
                theme_strings = [str(t) for t in themes if t]
                if theme_strings:
                    context_parts.append(f"Key Themes: {', '.join(theme_strings)}")
            if modifiers:
                modifier_count = len(modifiers)
                positive_count = sum(1 for m in modifiers if isinstance(m, dict) and m.get("value", 0) > 0)
                negative_count = sum(1 for m in modifiers if isinstance(m, dict) and m.get("value", 0) < 0)
                context_parts.append(
                    f"Insights: {modifier_count} factors identified "
                    f"({positive_count} strengths, {negative_count} gaps)"
                )
            context_parts.append("")  # Blank line between dimensions

        context_text = "\n".join(context_parts)

        prompt = f"""You are analyzing survey data for {org_name}. Based on the following dimension analyses,
create a comprehensive organization-level summary that synthesizes key themes, strengths,
and opportunities across all dimensions.

Dimension Analyses:
{context_text}

Provide a 3-5 paragraph organization summary that:
1. Highlights overall technology maturity level
2. Identifies cross-cutting themes that appear across multiple dimensions
3. Notes key organizational strengths in technology adoption
4. Identifies major gaps or challenges requiring attention
5. Provides 2-3 strategic recommendations based on the data

**CRITICAL GROUNDING REQUIREMENTS:**
- Base your summary ONLY on the dimension analyses provided above
- Reference specific dimensions when making observations
- Use phrases like "analysis indicates", "feedback shows", "across dimensions"
- Do NOT add generic advice not supported by the dimension summaries
- Keep tone supportive and grantee-friendly

Return ONLY the organization summary text (3-5 paragraphs), no JSON or formatting."""

        try:
            logger.debug(f"[AI] Calling async API for organization summary: {org_name}")
            response = await self.async_client.chat.completions.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.4,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technology consultant providing comprehensive assessment summaries to nonprofit organizations. Write in a supportive, professional tone. Base all analysis strictly on the provided dimension data."
                    },
                    {"role": "user", "content": prompt}
                ]
            )

            summary_text = response.choices[0].message.content.strip()

            # Remove quotes if present
            if summary_text.startswith('"') and summary_text.endswith('"'):
                summary_text = summary_text[1:-1]
            if summary_text.startswith("'") and summary_text.endswith("'"):
                summary_text = summary_text[1:-1]

            logger.info(f"[AI] Organization summary generated for {org_name}: {len(summary_text)} chars")
            return summary_text

        except Exception as e:
            logger.error(
                f"[AI] Error generating organization summary for {org_name}: {e}",
                exc_info=True
            )
            # Return fallback summary
            return (
                f"Technology assessment analysis for {org_name} has been completed across all five dimensions. "
                f"Review the individual dimension summaries above for detailed insights into Program Technology, "
                f"Business Systems, Data Management, Infrastructure, and Organizational Culture. "
                f"For a comprehensive strategic assessment, please consult the detailed dimension analyses."
            )

    def analyze_organization_qualitative(
        self, org_name: str, all_responses: Dict[str, List[Dict[str, Any]]], progress_callback=None
    ) -> Dict[str, Any]:
        """
        Comprehensive qualitative analysis for an organization across all dimensions.

        Args:
            org_name: Organization name
            all_responses: Dict mapping dimension names to lists of free text responses
            progress_callback: Optional callback function(progress_pct, message)

        Returns:
            Dict with dimension-level analysis and overall insights
        """
        results = {"organization": org_name, "dimensions": {}, "overall_summary": ""}

        # Analyze each dimension with progress updates
        dimensions = list(all_responses.keys())
        for i, (dimension, responses) in enumerate(all_responses.items()):
            # Update progress before each dimension analysis
            if progress_callback:
                progress = 32 + (i * 6)  # 32%, 38%, 44%, 50%, 56%
                progress_callback(
                    progress, f"AI analyzing {dimension}... ({i+1}/{len(dimensions)})"
                )

            if responses:
                results["dimensions"][dimension] = self.analyze_dimension_responses(
                    dimension, responses
                )

        # Generate overall summary
        all_texts = []
        for dimension, responses in all_responses.items():
            for r in responses:
                all_texts.append({"dimension": dimension, "organization": org_name, **r})

        if all_texts:
            results["overall_summary"] = self.summarize_all_feedback(all_texts)

        return results

    async def analyze_organization_qualitative_async(
        self, org_name: str, all_responses: Dict[str, List[Dict[str, Any]]], progress_callback=None
    ) -> Dict[str, Any]:
        """
        ASYNC CONCURRENT VERSION: Comprehensive qualitative analysis for an organization.

        Analyzes all 5 dimensions concurrently instead of serially, reducing total time
        from ~60 seconds (sum of 5 serial calls) to ~20 seconds (max of 5 parallel calls).

        Args:
            org_name: Organization name
            all_responses: Dict mapping dimension names to lists of free text responses
            progress_callback: Optional callback function(progress_pct, message)

        Returns:
            Dict with dimension-level analysis and overall insights
        """
        results = {"organization": org_name, "dimensions": {}, "overall_summary": ""}

        # Filter out dimensions with no responses
        dimensions_to_analyze = {
            dimension: responses for dimension, responses in all_responses.items() if responses
        }

        if not dimensions_to_analyze:
            logger.warning(f"No dimensions with responses for {org_name}")
            return results

        # Update progress: Starting concurrent analysis
        if progress_callback:
            num_dims = len(dimensions_to_analyze)
            progress_callback(32, f"AI analyzing {num_dims} dimensions concurrently...")

        # Create async tasks for all dimensions concurrently
        dimension_tasks = []
        dimension_names = []

        for dimension, responses in dimensions_to_analyze.items():
            dimension_names.append(dimension)
            task = self.analyze_dimension_responses_async(dimension, responses)
            dimension_tasks.append(task)

        # Execute all dimension analyses concurrently
        print(
            f"[AI] Starting concurrent analysis of {len(dimension_tasks)} dimensions for {org_name}"
        )
        start_time = asyncio.get_event_loop().time()

        # Use gather with return_exceptions to prevent one failure from cancelling others
        dimension_results = await asyncio.gather(*dimension_tasks, return_exceptions=True)

        end_time = asyncio.get_event_loop().time()
        elapsed = end_time - start_time
        print(f"[AI] Concurrent analysis completed in {elapsed:.2f}s for {org_name}")

        # Process results and handle any exceptions
        for dimension_name, result in zip(dimension_names, dimension_results):
            if isinstance(result, Exception):
                logger.error(f"Dimension analysis failed for {dimension_name}: {result}")
                results["dimensions"][dimension_name] = {
                    "modifiers": [],
                    "summary": f"Error analyzing {dimension_name}: {str(result)}",
                }
            else:
                results["dimensions"][dimension_name] = result

        # Update progress: Dimension analysis complete
        if progress_callback:
            progress_callback(62, "AI dimension analysis complete, generating summary...")

        # Generate overall summary (still synchronous for now)
        all_texts = []
        for dimension, responses in all_responses.items():
            for r in responses:
                all_texts.append({"dimension": dimension, "organization": org_name, **r})

        if all_texts:
            results["overall_summary"] = self.summarize_all_feedback(all_texts)

        # Update progress: Complete
        if progress_callback:
            progress_callback(70, "AI analysis complete")

        return results


def extract_free_text_responses(
    sheet_data: Dict[str, List[Dict[str, Any]]], org_name: str
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract all free text (non-numeric) responses for an organization.

    Args:
        sheet_data: Complete sheet data from SheetsReader
        org_name: Organization name to filter by

    Returns:
        Dict mapping dimension names to lists of free text responses
    """
    # Validate inputs
    if not sheet_data:
        logger.warning(f"extract_free_text_responses called with empty sheet_data for {org_name}")
        return {}

    if not org_name or not isinstance(org_name, str):
        logger.warning(f"extract_free_text_responses called with invalid org_name: {org_name}")
        return {}

    dimension_responses = {
        "Program Technology": [],
        "Business Systems": [],
        "Data Management": [],
        "Infrastructure": [],
        "Organizational Culture": [],
    }

    # Dimension code mapping
    dimension_codes = {
        "PT": "Program Technology",
        "BS": "Business Systems",
        "D": "Data Management",
        "I": "Infrastructure",
        "OC": "Organizational Culture",
    }

    # Check CEO, Tech, Staff tabs
    for tab_name, role in [("CEO", "CEO"), ("Tech", "Tech Lead"), ("Staff", "Staff")]:
        records = sheet_data.get(tab_name, [])

        # Validate records
        if not records:
            logger.debug(f"No records in {tab_name} tab for {org_name}")
            continue

        if not isinstance(records, list):
            logger.warning(f"Invalid records type in {tab_name} tab: {type(records)}")
            continue

        for record_idx, record in enumerate(records):
            # Validate record
            if record is None:
                logger.warning(f"Null record at index {record_idx} in {tab_name} tab")
                continue

            if not isinstance(record, dict):
                logger.warning(
                    f"Invalid record type at index {record_idx} in {tab_name} tab: {type(record)}"
                )
                continue

            # Use correct organization field for each survey type
            org_field = "CEO Organization" if tab_name == "CEO" else "Organization"
            record_org = record.get(org_field)

            # Handle None org field
            if record_org is None:
                logger.debug(f"Record {record_idx} in {tab_name} has None organization field")
                continue

            if record_org != org_name:
                continue

            # Extract free text responses (non-numeric)
            for key, value in record.items():
                # Skip None values
                if value is None:
                    continue

                # Look for question IDs that match dimension pattern
                if key.startswith(("C-", "TL-", "S-")) and value:
                    # Check if it's free text (not a number)
                    try:
                        float(str(value).strip())
                        # It's numeric, skip
                        continue
                    except (ValueError, TypeError):
                        # It's free text, extract dimension
                        parts = key.split("-")
                        if len(parts) >= 2:
                            code = parts[1]
                            dimension = dimension_codes.get(code)

                            # Validate text content
                            text_value = str(value).strip() if value is not None else ""
                            if dimension and len(text_value) > 10:  # Meaningful text
                                # Extract respondent name, handle None cases
                                respondent_name = record.get("Name")
                                if not respondent_name:
                                    respondent_name = record.get("Email")
                                if not respondent_name:
                                    respondent_name = "Unknown"

                                dimension_responses[dimension].append(
                                    {
                                        "respondent": str(respondent_name),
                                        "role": str(role),
                                        "text": text_value,
                                        "question_id": str(key),
                                    }
                                )

    # Log summary
    total_responses = sum(len(responses) for responses in dimension_responses.values())
    logger.info(f"Extracted {total_responses} free text responses for {org_name}")
    for dimension, responses in dimension_responses.items():
        if responses:
            logger.debug(f"  {dimension}: {len(responses)} responses")

    return dimension_responses


# Example usage
if __name__ == "__main__":
    analyzer = AIAnalyzer()

    # Test with sample data
    sample_responses = [
        {
            "respondent": "Jane Smith",
            "role": "CEO",
            "text": "We have strong program delivery tools but struggle with integration between systems. Staff training is a major gap.",
        },
        {
            "respondent": "John Doe",
            "role": "Tech Lead",
            "text": "Infrastructure is solid but we need better data governance policies. Current systems are not well documented.",
        },
    ]

    result = analyzer.analyze_dimension_responses("Program Technology", sample_responses)
    print(json.dumps(result, indent=2))
