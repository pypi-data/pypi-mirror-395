"""Test AI validation functions"""

from src.analytics.ai_analyzer import AIAnalyzer

# Test the validation function
analyzer = AIAnalyzer()

print("=" * 80)
print("TESTING BASIC INSIGHT VALIDATION")
print("=" * 80)

# Test valid text
valid_text = "Your team demonstrates strong capabilities in technology integration across program delivery. Based on feedback, there are opportunities to enhance staff training and system documentation."
print(f"Valid text test: {analyzer._is_valid_insight(valid_text)}")

# Test garbled text (like the bug)
garbled_text = "Program Technology Here Mill española einer Statement ofinar$(."
print(f"Garbled text test: {analyzer._is_valid_insight(garbled_text)}")

# Test short text
short_text = "Too short"
print(f"Short text test: {analyzer._is_valid_insight(short_text)}")

# Test fallback
fallback = analyzer._get_fallback_insight("Program Technology")
print(f"\nFallback text: {fallback}")
print(f"Fallback valid: {analyzer._is_valid_insight(fallback)}")

print("\n" + "=" * 80)
print("TESTING NARRATIVE TEXT VALIDATION (HALLUCINATION DETECTION)")
print("=" * 80)

# Test Case 1: Text with valid respondent names
valid_respondents = ["Alice Smith", "Bob Johnson", "Carol Davis"]
text_with_valid_names = "Alice Smith mentioned concerns about data security, while Bob Johnson highlighted the need for better training."
result = analyzer._validate_narrative_text(text_with_valid_names, valid_respondents, "test case 1")
print(f"\nTest 1 - Valid names (should remain unchanged):")
print(f"  Input: {text_with_valid_names}")
print(f"  Output: {result}")
print(f"  PASS: {result == text_with_valid_names}")

# Test Case 2: Text with hallucinated respondent names
text_with_hallucinated = "Sarah Williams mentioned privacy concerns, while John Doe highlighted security issues. Alice Smith agreed with these points."
result = analyzer._validate_narrative_text(text_with_hallucinated, valid_respondents, "test case 2")
print(f"\nTest 2 - Hallucinated names (should be removed):")
print(f"  Input: {text_with_hallucinated}")
print(f"  Output: {result}")
print(f"  Expected: Names 'Sarah Williams' and 'John Doe' replaced with '[respondent]'")
print(f"  PASS: {'Sarah Williams' not in result and 'John Doe' not in result and 'Alice Smith' in result}")

# Test Case 3: Text with common phrases that look like names
text_with_phrases = "The Tech Lead highlighted cloud security concerns, while the Program Director discussed staff training."
result = analyzer._validate_narrative_text(text_with_phrases, valid_respondents, "test case 3")
print(f"\nTest 3 - Common phrases (should remain unchanged):")
print(f"  Input: {text_with_phrases}")
print(f"  Output: {result}")
print(f"  PASS: {result == text_with_phrases}")

# Test Case 4: Mixed scenario - hallucinated names mixed with valid ones
# In real reports, names should appear standalone, not prefixed with titles
text_mixed = "Alice Smith raised concerns about cloud security, while Mary Jones and John Doe discussed training needs. Bob Johnson agreed with Carol Davis on infrastructure priorities."
result = analyzer._validate_narrative_text(text_mixed, valid_respondents, "test case 4")
print(f"\nTest 4 - Mixed (valid + hallucinated names):")
print(f"  Input: {text_mixed}")
print(f"  Output: {result}")
print(f"  Expected: 'Mary Jones' and 'John Doe' replaced, valid names kept")
print(f"  PASS: {'Mary Jones' not in result and 'John Doe' not in result and 'Alice Smith' in result and 'Bob Johnson' in result and 'Carol Davis' in result}")

# Test Case 5: No respondent names in text
text_no_names = "The organization demonstrates strong technology maturity with effective cloud infrastructure."
result = analyzer._validate_narrative_text(text_no_names, valid_respondents, "test case 5")
print(f"\nTest 5 - No names (should remain unchanged):")
print(f"  Input: {text_no_names}")
print(f"  Output: {result}")
print(f"  PASS: {result == text_no_names}")

print("\n" + "=" * 80)
print("ALL VALIDATION TESTS COMPLETED!")
print("=" * 80)
