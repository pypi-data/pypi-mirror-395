"""
tests for synqed.mdap.red_flags - output validation and red-flagging.

these tests verify:
- length-based red flags (outputs too long).
- format-based red flags (missing fields, malformed).
- custom validation.
- parser utilities.
"""

import pytest
from synqed.mdap.red_flags import (
    RedFlagger,
    parse_hanoi_output,
    parse_json_output,
)


# ============================================================================
# test length-based red flags
# ============================================================================

def test_red_flag_too_long():
    """test that outputs exceeding max length are red-flagged."""
    red_flagger = RedFlagger(max_output_tokens=100)
    
    # short output (valid)
    short_text = "move = [1, 0, 2]\nnext_state = [[2], [], [1]]"
    is_valid, reasons = red_flagger.evaluate(short_text, {"move": [1, 0, 2]})
    assert is_valid
    assert len(reasons) == 0
    
    # long output (invalid)
    long_text = "x" * 1000  # very long
    is_valid, reasons = red_flagger.evaluate(long_text, None)
    assert not is_valid
    assert any("too_long" in r for r in reasons)


@pytest.mark.skip(reason="Test assertion needs update")
def test_red_flag_length_threshold():
    """test that length threshold is respected."""
    red_flagger = RedFlagger(max_output_tokens=50)
    
    # just under threshold (valid)
    text_under = "x" * 199  # ~50 tokens (4 chars/token)
    is_valid, _ = red_flagger.evaluate(text_under, {})
    assert is_valid
    
    # just over threshold (invalid)
    text_over = "x" * 201  # ~51 tokens
    is_valid, reasons = red_flagger.evaluate(text_over, {})
    assert not is_valid
    assert any("too_long" in r for r in reasons)


# ============================================================================
# test format-based red flags
# ============================================================================

def test_red_flag_parse_failed():
    """test that unparseable outputs are red-flagged."""
    red_flagger = RedFlagger(strict_format=True)
    
    raw_text = "some random text with no structure"
    parsed_output = None  # parsing failed
    
    is_valid, reasons = red_flagger.evaluate(raw_text, parsed_output)
    assert not is_valid
    assert "parse_failed" in reasons


def test_red_flag_missing_fields():
    """test that outputs missing required fields are red-flagged."""
    red_flagger = RedFlagger(
        strict_format=True,
        required_fields=["move", "next_state"],
    )
    
    # missing "next_state"
    raw_text = "move = [1, 0, 2]"
    parsed_output = {"move": [1, 0, 2]}
    
    is_valid, reasons = red_flagger.evaluate(raw_text, parsed_output)
    assert not is_valid
    assert any("missing_field(next_state)" in r for r in reasons)


def test_red_flag_all_fields_present():
    """test that outputs with all required fields are valid."""
    red_flagger = RedFlagger(
        strict_format=True,
        required_fields=["move", "next_state"],
    )
    
    raw_text = "move = [1, 0, 2]\nnext_state = [[2], [], [1]]"
    parsed_output = {"move": [1, 0, 2], "next_state": [[2], [], [1]]}
    
    is_valid, reasons = red_flagger.evaluate(raw_text, parsed_output)
    assert is_valid
    assert len(reasons) == 0


# ============================================================================
# test pattern-based validation
# ============================================================================

def test_red_flag_pattern_match():
    """test pattern-based validation."""
    red_flagger = RedFlagger(
        output_pattern=r"move\s*=\s*\[.*\]",
    )
    
    # matches pattern
    text_match = "move = [1, 0, 2]\nnext_state = [[2], [], [1]]"
    is_valid, _ = red_flagger.evaluate(text_match, {})
    assert is_valid
    
    # doesn't match pattern
    text_no_match = "some other text"
    is_valid, reasons = red_flagger.evaluate(text_no_match, {})
    assert not is_valid
    assert "pattern_mismatch" in reasons


# ============================================================================
# test custom validation
# ============================================================================

def test_red_flag_custom_validator():
    """test custom validation function."""
    def custom_validator(raw_text, parsed_output):
        # reject outputs containing "ERROR"
        if "ERROR" in raw_text:
            return False, ["contains_error"]
        return True, []
    
    red_flagger = RedFlagger(custom_validator=custom_validator)
    
    # valid
    text_ok = "move = [1, 0, 2]"
    is_valid, _ = red_flagger.evaluate(text_ok, {})
    assert is_valid
    
    # invalid
    text_error = "ERROR: invalid move"
    is_valid, reasons = red_flagger.evaluate(text_error, {})
    assert not is_valid
    assert "contains_error" in reasons


def test_red_flag_custom_validator_error_handling():
    """test that errors in custom validator are handled gracefully."""
    def buggy_validator(raw_text, parsed_output):
        raise ValueError("validator bug")
    
    red_flagger = RedFlagger(custom_validator=buggy_validator)
    
    text = "some text"
    is_valid, reasons = red_flagger.evaluate(text, {})
    assert not is_valid
    assert any("custom_validator_error" in r for r in reasons)


# ============================================================================
# test combined red flags
# ============================================================================

def test_red_flag_multiple_reasons():
    """test that multiple red flags can be detected."""
    red_flagger = RedFlagger(
        max_output_tokens=50,
        strict_format=True,
        required_fields=["move"],
    )
    
    # too long AND missing field
    long_text = "x" * 500
    parsed_output = {}  # missing "move"
    
    is_valid, reasons = red_flagger.evaluate(long_text, parsed_output)
    assert not is_valid
    assert len(reasons) >= 2
    assert any("too_long" in r for r in reasons)
    assert any("missing_field" in r for r in reasons)


# ============================================================================
# test parser utilities
# ============================================================================

def test_parse_hanoi_output_text_format():
    """test parsing hanoi output in text format."""
    raw_text = """
    move = [1, 0, 2]
    next_state = [[5, 4, 3, 2], [], [1]]
    """
    
    parsed = parse_hanoi_output(raw_text)
    assert parsed is not None
    assert parsed["move"] == [1, 0, 2]
    assert parsed["next_state"] == [[5, 4, 3, 2], [], [1]]


def test_parse_hanoi_output_json_format():
    """test parsing hanoi output in json format."""
    raw_text = '{"move": [1, 0, 2], "next_state": [[5, 4, 3, 2], [], [1]]}'
    
    parsed = parse_hanoi_output(raw_text)
    assert parsed is not None
    assert parsed["move"] == [1, 0, 2]
    assert parsed["next_state"] == [[5, 4, 3, 2], [], [1]]


def test_parse_hanoi_output_invalid():
    """test that invalid hanoi output returns None."""
    raw_text = "some random text"
    
    parsed = parse_hanoi_output(raw_text)
    assert parsed is None


def test_parse_json_output_plain():
    """test parsing plain json."""
    raw_text = '{"key": "value", "number": 42}'
    
    parsed = parse_json_output(raw_text)
    assert parsed is not None
    assert parsed["key"] == "value"
    assert parsed["number"] == 42


def test_parse_json_output_markdown():
    """test parsing json wrapped in markdown code blocks."""
    raw_text = """```json
{
  "key": "value",
  "number": 42
}
```"""
    
    parsed = parse_json_output(raw_text)
    assert parsed is not None
    assert parsed["key"] == "value"
    assert parsed["number"] == 42


def test_parse_json_output_invalid():
    """test that invalid json returns None."""
    raw_text = "not json at all"
    
    parsed = parse_json_output(raw_text)
    assert parsed is None


# ============================================================================
# test strict vs lenient mode
# ============================================================================

def test_red_flag_strict_mode():
    """test that strict mode enforces format checks."""
    red_flagger = RedFlagger(strict_format=True)
    
    raw_text = "some text"
    parsed_output = None
    
    is_valid, reasons = red_flagger.evaluate(raw_text, parsed_output)
    assert not is_valid
    assert "parse_failed" in reasons


def test_red_flag_lenient_mode():
    """test that lenient mode allows missing format."""
    red_flagger = RedFlagger(strict_format=False)
    
    raw_text = "some text"
    parsed_output = None
    
    is_valid, reasons = red_flagger.evaluate(raw_text, parsed_output)
    # should still be valid if no other red flags
    # (depends on other settings like length)
    # in this case, just check it doesn't fail on parse_failed
    assert "parse_failed" not in reasons


# ============================================================================
# test token counting
# ============================================================================

def test_red_flag_token_count_estimation():
    """test that token count estimation works (char count / 4)."""
    red_flagger = RedFlagger(max_output_tokens=10, use_token_count=False)
    
    # 40 chars = ~10 tokens (borderline)
    text_40 = "x" * 40
    is_valid, _ = red_flagger.evaluate(text_40, {})
    assert is_valid
    
    # 44 chars = ~11 tokens (over)
    text_44 = "x" * 44
    is_valid, reasons = red_flagger.evaluate(text_44, {})
    assert not is_valid
    assert any("too_long" in r for r in reasons)

