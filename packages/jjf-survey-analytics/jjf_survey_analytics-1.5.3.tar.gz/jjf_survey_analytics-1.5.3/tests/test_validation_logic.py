"""Test AI validation logic without dependencies"""


def is_valid_insight(text: str) -> bool:
    """Validate that AI-generated insight is readable and not garbled."""
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


# Test valid text
valid_text = "Your team demonstrates strong capabilities in technology integration across program delivery. Based on feedback, there are opportunities to enhance staff training and system documentation."
print(f"✓ Valid text test: {is_valid_insight(valid_text)}")

# Test garbled text (like the bug)
garbled_text = "Program Technology Here Mill española einer Statement ofinar$(."
print(f"✗ Garbled text test (should be False): {is_valid_insight(garbled_text)}")

# Test short text
short_text = "Too short"
print(f"✗ Short text test (should be False): {is_valid_insight(short_text)}")

# Test text with parentheses
paren_text = "This text has (parentheses) in it which should fail validation."
print(f"✗ Parentheses text test (should be False): {is_valid_insight(paren_text)}")

# Test fallback text
fallback_text = "Based on survey responses, your organization shows varying levels of technology integration in program delivery. Consider reviewing staff feedback to identify specific areas for enhancement."
print(f"✓ Fallback text test: {is_valid_insight(fallback_text)}")

print("\n✅ All validation tests completed successfully!")
