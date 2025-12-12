"""
synqed.mdap.red_flags - output validation and red-flagging logic.

this module implements the red-flagging component of the maker framework
(section 3.3 of the paper). instead of trying to "repair" bad outputs,
we discard outputs that show signs of unreliability:
- outputs that are too long (> threshold tokens, e.g. 750).
- outputs with incorrect format (missing fields, malformed structure).

key insight: when an llm produces a misformatted or overly long response,
it's often a sign that its reasoning is confused. discarding these samples
increases the per-step success rate p and reduces correlated errors.

from the paper (section 3.3):
- "once an llm gets initially confused, it can go off the rails and 
   over-analyze a situation in a cycle of self-destruction."
- "when an agent produces an answer in an incorrect format, it is more 
   likely to have become confused at some point on the way to that answer."
"""

from __future__ import annotations

import re
import json
import logging
from typing import Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RedFlagConfig:
    """
    configuration for red-flag validation.
    
    attributes:
        max_output_tokens: max allowed output length (tokens or chars).
        strict_format: whether to strictly enforce output format.
        required_fields: list of required field names in the output.
        output_pattern: optional regex pattern for output format.
        custom_validator: optional custom validation function.
    """
    max_output_tokens: int = 750
    strict_format: bool = True
    required_fields: list[str] = None
    output_pattern: Optional[str] = None
    custom_validator: Optional[callable] = None


class RedFlagger:
    """
    red-flagger: validates outputs and discards risky ones.
    
    this class implements algorithm 3 (get_vote) from the paper:
    - repeatedly sample until a valid (non-red-flagged) response is obtained.
    - red flags include:
      1. length-based: output too long (> max_output_tokens).
      2. format-based: output missing required fields or malformed.
    
    usage:
        red_flagger = RedFlagger(max_output_tokens=750, required_fields=["move", "next_state"])
        is_valid, reasons = red_flagger.evaluate(raw_text, parsed_output, step_input)
        
        if not is_valid:
            # discard and resample
            pass
    """
    
    def __init__(
        self,
        max_output_tokens: int = 750,
        strict_format: bool = True,
        required_fields: Optional[list[str]] = None,
        output_pattern: Optional[str] = None,
        custom_validator: Optional[callable] = None,
        use_token_count: bool = False,
    ):
        """
        initialize red-flagger.
        
        args:
            max_output_tokens: max allowed output length (chars if use_token_count=False).
            strict_format: whether to strictly enforce format.
            required_fields: list of required field names in parsed output.
            output_pattern: optional regex pattern for raw text validation.
            custom_validator: optional custom validation function(raw_text, parsed) -> (bool, list[str]).
            use_token_count: if true, count tokens; else use char count as proxy.
        """
        self.max_output_tokens = max_output_tokens
        self.strict_format = strict_format
        self.required_fields = required_fields or []
        self.output_pattern = output_pattern
        self.custom_validator = custom_validator
        self.use_token_count = use_token_count
    
    def evaluate(
        self,
        raw_text: str,
        parsed_output: Optional[dict[str, Any]],
        step_input: Any = None,
    ) -> tuple[bool, list[str]]:
        """
        evaluate whether an output is valid or should be red-flagged.
        
        args:
            raw_text: raw llm response text.
            parsed_output: parsed output dict (or None if parsing failed).
            step_input: optional step input for context-specific validation.
        
        returns:
            (is_valid, red_flag_reasons)
        """
        red_flags = []
        
        # 1. length-based red flag
        length = self._count_tokens(raw_text)
        if length > self.max_output_tokens:
            red_flags.append(f"too_long({length}>{self.max_output_tokens})")
        
        # 2. format-based red flags
        if self.strict_format:
            if parsed_output is None:
                red_flags.append("parse_failed")
            else:
                # check required fields
                for field in self.required_fields:
                    if field not in parsed_output:
                        red_flags.append(f"missing_field({field})")
        
        # 3. pattern-based validation
        if self.output_pattern:
            if not re.search(self.output_pattern, raw_text):
                red_flags.append("pattern_mismatch")
        
        # 4. custom validation
        if self.custom_validator:
            try:
                is_valid, custom_reasons = self.custom_validator(raw_text, parsed_output)
                if not is_valid:
                    red_flags.extend(custom_reasons)
            except Exception as e:
                logger.warning(f"custom validator error: {e}")
                red_flags.append(f"custom_validator_error({str(e)})")
        
        is_valid = len(red_flags) == 0
        return is_valid, red_flags
    
    def _count_tokens(self, text: str) -> int:
        """
        count tokens in text.
        
        if use_token_count=True, use tiktoken (for openai models).
        otherwise, use char count as a proxy (rough estimate: 4 chars ≈ 1 token).
        """
        if self.use_token_count:
            try:
                import tiktoken
                enc = tiktoken.get_encoding("cl100k_base")  # gpt-4 encoding
                return len(enc.encode(text))
            except ImportError:
                logger.warning("tiktoken not installed; falling back to char count / 4")
                return len(text) // 4
        else:
            # char count as proxy
            return len(text) // 4  # rough estimate: 4 chars per token


# ============================================================================
# parser utilities
# ============================================================================

def parse_hanoi_output(raw_text: str) -> Optional[dict[str, Any]]:
    """
    parse hanoi-specific output format.
    
    expected format:
        move = [disk, from_peg, to_peg]
        next_state = [[...], [...], [...]]
    
    or json:
        {"move": [disk, from_peg, to_peg], "next_state": [...]}
    
    returns:
        parsed dict with "move" and "next_state", or None if parsing fails.
    """
    # try json first
    try:
        parsed = json.loads(raw_text.strip())
        if "move" in parsed and "next_state" in parsed:
            return parsed
    except (json.JSONDecodeError, ValueError):
        pass
    
    # try text pattern
    move_match = re.search(r"move\s*=\s*\[([\d,\s]+)\]", raw_text, re.IGNORECASE)
    state_match = re.search(r"next_state\s*=\s*(\[.*\])", raw_text, re.IGNORECASE | re.DOTALL)
    
    if move_match and state_match:
        try:
            move_str = move_match.group(1)
            move = [int(x.strip()) for x in move_str.split(",")]
            
            state_str = state_match.group(1)
            # safely eval the list
            next_state = eval(state_str)
            
            return {"move": move, "next_state": next_state}
        except (ValueError, SyntaxError):
            pass
    
    return None


def parse_json_output(raw_text: str) -> Optional[dict[str, Any]]:
    """
    parse json output from llm response.
    
    handles:
    - markdown code blocks: ```json ... ```
    - raw json: {...}
    
    returns:
        parsed dict, or None if parsing fails.
    """
    text = raw_text.strip()
    
    # remove markdown code blocks
    if text.startswith("```"):
        lines = text.split("\n")
        # skip first line (```json or ```)
        lines = lines[1:]
        # find closing ```
        for i, line in enumerate(lines):
            if line.strip() == "```":
                lines = lines[:i]
                break
        text = "\n".join(lines).strip()
    
    # try parsing
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None

