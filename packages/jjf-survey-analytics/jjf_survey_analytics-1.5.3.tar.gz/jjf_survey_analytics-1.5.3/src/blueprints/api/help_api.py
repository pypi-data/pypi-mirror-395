"""
Help Chatbot API for JJF Survey Analytics.

Provides RAG-based help system using the same OpenAI-compatible LLM as report generation.
"""

import json
import logging
import os
from pathlib import Path

from flask import Blueprint, jsonify, request
from openai import OpenAI

from src.blueprints.auth_blueprint import require_auth

logger = logging.getLogger(__name__)

# Create blueprint
help_api = Blueprint("help_api", __name__)


class HelpChatbot:
    """RAG-based help chatbot using OpenRouter Claude 3.5 Sonnet."""

    def __init__(self):
        """Initialize OpenRouter client for Claude Sonnet 3.5 (same as report generation)."""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            timeout=30.0,
        )

        self.model = "anthropic/claude-3.5-sonnet"
        logger.info(f"[HELP CHATBOT] Using OpenRouter with Claude 3.5 Sonnet: {self.model}")

        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self) -> dict:
        """Load RAG knowledge base from JSON file."""
        kb_path = Path(__file__).parent.parent.parent / "services" / "help_knowledge_base.json"

        try:
            with open(kb_path, "r") as f:
                kb = json.load(f)
                logger.info(
                    f"[HELP CHATBOT] Loaded knowledge base: "
                    f"{len(kb.get('application_features', []))} features, "
                    f"{len(kb.get('technical_terms', {}))} terms"
                )
                return kb
        except FileNotFoundError:
            logger.error(f"[HELP CHATBOT] Knowledge base not found at {kb_path}")
            return {"application_features": [], "technical_terms": {}}
        except json.JSONDecodeError as e:
            logger.error(f"[HELP CHATBOT] Failed to parse knowledge base: {e}")
            return {"application_features": [], "technical_terms": {}}

    def _search_knowledge_base(self, query: str) -> list:
        """
        Search knowledge base for relevant Q&A entries.

        Simple keyword matching for RAG retrieval. Returns top 5 most relevant entries.

        Args:
            query: User's question

        Returns:
            List of relevant knowledge base entries
        """
        query_lower = query.lower()
        features = self.knowledge_base.get("application_features", [])

        # Score each entry by keyword matches
        scored_entries = []
        for entry in features:
            score = 0

            # Check question field
            if any(word in entry.get("question", "").lower() for word in query_lower.split()):
                score += 3

            # Check answer field
            if any(word in entry.get("answer", "").lower() for word in query_lower.split()):
                score += 2

            # Check category and topic
            if any(word in entry.get("category", "").lower() for word in query_lower.split()):
                score += 1
            if any(word in entry.get("topic", "").lower() for word in query_lower.split()):
                score += 1

            if score > 0:
                scored_entries.append((score, entry))

        # Sort by score and return top 5
        scored_entries.sort(reverse=True, key=lambda x: x[0])
        return [entry for _, entry in scored_entries[:5]]

    def _build_context_prompt(self, query: str, relevant_entries: list) -> str:
        """
        Build RAG context prompt with retrieved knowledge base entries.

        Args:
            query: User's question
            relevant_entries: Retrieved knowledge base entries

        Returns:
            Context string for LLM prompt
        """
        if not relevant_entries:
            return "No specific documentation found for this query."

        context_parts = ["Here is relevant documentation from the knowledge base:\n"]

        for entry in relevant_entries:
            category = entry.get("category", "General")
            topic = entry.get("topic", "Unknown")
            question = entry.get("question", "")
            answer = entry.get("answer", "")

            context_parts.append(f"\n**{category} - {topic}**")
            context_parts.append(f"Q: {question}")
            context_parts.append(f"A: {answer}\n")

        # Add technical terms if any keywords match
        query_lower = query.lower()
        terms = self.knowledge_base.get("technical_terms", {})
        relevant_terms = {
            term: definition
            for term, definition in terms.items()
            if term.lower() in query_lower
        }

        if relevant_terms:
            context_parts.append("\n**Technical Terms:**")
            for term, definition in relevant_terms.items():
                context_parts.append(f"- **{term}**: {definition}")

        return "\n".join(context_parts)

    def get_response(self, user_message: str) -> dict:
        """
        Generate chatbot response using RAG with OpenRouter Claude 3.5 Sonnet.

        Args:
            user_message: User's question

        Returns:
            Dict with 'response' and 'sources' keys
        """
        logger.info(f"[HELP CHATBOT] Processing query: {user_message[:100]}")

        # Step 1: Retrieve relevant knowledge base entries
        relevant_entries = self._search_knowledge_base(user_message)
        logger.debug(f"[HELP CHATBOT] Found {len(relevant_entries)} relevant entries")

        # Step 2: Build context prompt
        context = self._build_context_prompt(user_message, relevant_entries)

        # Step 3: Build full prompt for LLM
        system_prompt = """You are a helpful assistant for the JJF Survey Analytics application.

Your role is to:
1. Answer user questions about application features and functionality
2. Provide clear, concise explanations based on the documentation
3. Guide users to the right features for their needs
4. Explain technical terms when relevant

Guidelines:
- Base your answers on the provided documentation context
- Be friendly and supportive
- Use simple language and avoid unnecessary jargon
- If you don't have information to answer a question, say so clearly
- Keep responses concise (2-3 paragraphs maximum)
- Reference specific features or pages when relevant"""

        user_prompt = f"""User question: {user_message}

{context}

Please provide a helpful answer based on the documentation above. If the documentation doesn't cover the user's question, let them know and suggest they contact support or check the application directly."""

        try:
            # Step 4: Call OpenRouter API (same as report generation)
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=500,
                temperature=0.4,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )

            answer = response.choices[0].message.content.strip()

            # Extract sources (categories and topics from relevant entries)
            sources = []
            for entry in relevant_entries:
                source = f"{entry.get('category', 'General')} - {entry.get('topic', 'Unknown')}"
                if source not in sources:
                    sources.append(source)

            logger.info(f"[HELP CHATBOT] Generated response: {len(answer)} chars, {len(sources)} sources")

            return {
                "response": answer,
                "sources": sources[:3],  # Top 3 sources
            }

        except Exception as e:
            logger.error(f"[HELP CHATBOT] Error generating response: {e}", exc_info=True)
            return {
                "response": "I apologize, but I'm having trouble processing your question right now. Please try again or contact support.",
                "sources": [],
            }


# Singleton instance
_chatbot_instance = None


def get_chatbot() -> HelpChatbot:
    """Get or create singleton chatbot instance."""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = HelpChatbot()
    return _chatbot_instance


@help_api.route("/api/help/chat", methods=["POST"])
@require_auth
def chat():
    """
    Handle help chatbot queries.

    Expects JSON body:
        {
            "message": "User's question"
        }

    Returns:
        {
            "response": "Chatbot's answer",
            "sources": ["Category - Topic", ...]
        }
    """
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400

        user_message = data["message"].strip()

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Get chatbot instance and generate response
        chatbot = get_chatbot()
        result = chatbot.get_response(user_message)

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"[HELP API] Error handling chat request: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@help_api.route("/api/help/context", methods=["POST"])
@require_auth
def help_context():
    """
    Context-aware help endpoint for Interactive Guide (Phase 2).

    Accepts:
        message (str): User's question
        context (dict): Page context
            - page (str): Current page identifier
            - org_name (str, optional): Organization name
            - user_role (str): User role (admin/viewer/guest)
            - timestamp (int): Context timestamp

    Returns:
        answer (str): Context-aware response
        suggestions (list): Contextual follow-up suggestions
        actions (list): Suggested guide actions
    """
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400

        message = data.get("message", "").strip()
        context = data.get("context", {})

        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Get base answer from knowledge base
        chatbot = get_chatbot()
        base_result = chatbot.get_response(message)
        answer = base_result.get("response", "")

        # Enhance with context-aware suggestions and actions
        page = context.get("page", "unknown")
        org_name = context.get("org_name")
        user_role = context.get("user_role", "guest")

        suggestions = []
        actions = []

        # Page-specific enhancements
        if page == "home":
            suggestions.extend([
                "Would you like to know how to view organization reports?",
                "Want to understand the completion status indicators?",
                "Need help with auto-sync functionality?"
            ])

        elif page == "data":
            suggestions.extend([
                "Would you like to see how to check completion status?",
                "Want to know about auto-sync frequency?",
                "Need help understanding response rates?"
            ])
            actions.append({
                "type": "highlight",
                "selector": ".organization-status-table, table",
                "message": "This table shows completion status for all organizations"
            })

        elif page == "organization_report" and org_name:
            suggestions.extend([
                f"Would you like help interpreting {org_name}'s scores?",
                "Want to understand the variance indicators?",
                "Need to know how to edit this report?"
            ])
            actions.append({
                "type": "highlight",
                "selector": '[data-guide-id="view-build-review-btn"], .btn-primary',
                "message": "Click here to edit this organization's report"
            })

        elif page == "build_review":
            suggestions.extend([
                "Need help editing dimension summaries?",
                "Want to know how to save changes?",
                "Confused about the card status indicators?",
                "How do score modifiers work?"
            ])
            actions.append({
                "type": "highlight",
                "selector": '[data-guide-id="save-all-changes-btn"], #save-all-btn',
                "message": "Click here to save all your changes to the database"
            })

        elif page == "reports_list":
            suggestions.extend([
                "Want to generate an aggregate report?",
                "Need help understanding report types?",
                "Confused about report caching?"
            ])

        elif page == "admin" and user_role == "admin":
            suggestions.extend([
                "Need help with auto-sync configuration?",
                "Want to understand database management?",
                "Need to check system health?"
            ])

        # Limit suggestions to top 3
        suggestions = suggestions[:3]

        logger.info(
            f"[HELP API CONTEXT] Response generated for page={page}, "
            f"org={org_name}, suggestions={len(suggestions)}, actions={len(actions)}"
        )

        return jsonify({
            "answer": answer,
            "suggestions": suggestions,
            "actions": actions,
            "context": {
                "page": page,
                "org_name": org_name,
                "user_role": user_role
            }
        }), 200

    except Exception as e:
        logger.error(f"[HELP API CONTEXT] Error handling context request: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
