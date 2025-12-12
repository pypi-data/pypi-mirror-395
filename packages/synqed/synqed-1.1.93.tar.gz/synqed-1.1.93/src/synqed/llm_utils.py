"""
llm utilities for parsing and repairing llm output.

provides robust json extraction, format repair, and depth validation
for the multi-agent interaction pipeline.
"""

import json
import re
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)


def extract_json_from_llm_output(raw: str) -> dict:
    """
    parse llm output into json, attempting to recover if there is extra text.
    
    tries multiple strategies:
    1. direct json.loads
    2. extract from markdown code blocks
    3. find largest {...} block via regex
    
    args:
        raw: raw string output from llm
        
    returns:
        parsed json dict
        
    raises:
        ValueError: if no valid json can be extracted
    """
    if not raw or not raw.strip():
        raise ValueError("empty llm output")
    
    raw = raw.strip()
    
    # strategy 1: try direct parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    
    # strategy 2: extract from markdown code blocks (```json ... ``` or ``` ... ```)
    code_block_pattern = r"```(?:json)?\s*\n?(.*?)\n?```"
    matches = re.findall(code_block_pattern, raw, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue
    
    # strategy 3: find the largest balanced {...} block
    # use a simple bracket-counting approach for robustness
    best_json = None
    best_length = 0
    
    i = 0
    while i < len(raw):
        if raw[i] == '{':
            depth = 0
            start = i
            in_string = False
            escape_next = False
            
            j = i
            while j < len(raw):
                char = raw[j]
                
                if escape_next:
                    escape_next = False
                    j += 1
                    continue
                
                if char == '\\' and in_string:
                    escape_next = True
                    j += 1
                    continue
                    
                if char == '"' and not escape_next:
                    in_string = not in_string
                elif not in_string:
                    if char == '{':
                        depth += 1
                    elif char == '}':
                        depth -= 1
                        if depth == 0:
                            candidate = raw[start:j+1]
                            try:
                                parsed = json.loads(candidate)
                                if len(candidate) > best_length:
                                    best_json = parsed
                                    best_length = len(candidate)
                            except json.JSONDecodeError:
                                pass
                            break
                j += 1
        i += 1
    
    if best_json is not None:
        return best_json
    
    # strategy 4: try a greedy regex as last resort
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    raise ValueError("no valid json object found in llm output")


def validate_visible_reasoning(text: str) -> list[str]:
    """
    validate that visible_reasoning field contains sufficient depth.
    
    checks:
    - minimum length (250 chars)
    - contains paragraph breaks (at least 1 newline)
    - mentions uncertainty/assumption/dependency/risk/alternative
    
    args:
        text: the visible_reasoning content
        
    returns:
        list of validation issues (empty if valid)
    """
    problems: list[str] = []
    cleaned = (text or "").strip()
    
    if len(cleaned) < 250:
        problems.append("reasoning too short (< 250 characters)")
    
    # check for paragraph structure
    if cleaned.count("\n") < 1 and len(cleaned) > 100:
        problems.append("reasoning should span at least two paragraphs")
    
    # check for depth indicators
    keywords = ["uncertainty", "uncertain", "assumption", "assume", "dependency", 
                "depend", "risk", "alternative", "unknown", "unclear", "question"]
    lower = cleaned.lower()
    if not any(k in lower for k in keywords):
        problems.append("missing explicit uncertainty/assumption/dependency/risk/alternative")
    
    return problems


def create_format_repair_prompt(raw_output: str) -> str:
    """
    create a repair prompt to ask the llm to reformat invalid output.
    
    args:
        raw_output: the original malformed output
        
    returns:
        system prompt for repair request
    """
    return f"""you previously responded with invalid formatting. 
re-output the same content as a single valid json object with exactly these fields:

{{
  "send_to": "<recipient>",
  "visible_reasoning": "<your multi-paragraph reasoning>",
  "collaboration": "<requests to teammates or empty string>",
  "content": "<your main deliverable content>"
}}

do not add any text before or after the json.
do not use code fences or markdown.
respond with exactly one json object.

your previous response was:
{raw_output[:2000]}"""


def create_depth_challenge_prompt(issues: list[str]) -> str:
    """
    create a challenge prompt to ask the agent to deepen their reasoning.
    
    args:
        issues: list of validation issues to address
        
    returns:
        system prompt for depth challenge
    """
    issues_str = "; ".join(issues)
    return f"""your visible_reasoning is too shallow. issues: {issues_str}

please rewrite your response with deeper analysis:
- explicitly address uncertainty, assumptions, or dependencies
- span at least 2-3 paragraphs of structured thinking
- show your actual reasoning process, not just conclusions

return the full json response again with improved visible_reasoning."""


def create_fallback_response(agent_name: str, raw_output: str, error_msg: str) -> dict:
    """
    create a fallback response when parsing completely fails.
    
    tries to salvage content from truncated json before falling back to raw.
    
    args:
        agent_name: name of the agent
        raw_output: the raw llm output that couldn't be parsed
        error_msg: description of what went wrong
        
    returns:
        structured response dict for frontend display
    """
    # try to extract fields from truncated json
    extracted_content = None
    extracted_reasoning = ""
    extracted_collab = ""
    
    if raw_output and '"content"' in raw_output:
        # try to extract the content field from truncated json
        import re
        content_match = re.search(r'"content"\s*:\s*"((?:[^"\\]|\\.)*)(?:"|$)', raw_output, re.DOTALL)
        if content_match:
            extracted_content = content_match.group(1)
            # unescape json escapes
            extracted_content = extracted_content.replace('\\n', '\n').replace('\\"', '"')
    
    if raw_output and '"visible_reasoning"' in raw_output:
        reasoning_match = re.search(r'"visible_reasoning"\s*:\s*"((?:[^"\\]|\\.)*)(?:"|$)', raw_output, re.DOTALL)
        if reasoning_match:
            extracted_reasoning = reasoning_match.group(1).replace('\\n', '\n').replace('\\"', '"')
    
    if raw_output and '"collaboration"' in raw_output:
        collab_match = re.search(r'"collaboration"\s*:\s*"((?:[^"\\]|\\.)*)(?:"|$)', raw_output, re.DOTALL)
        if collab_match:
            extracted_collab = collab_match.group(1).replace('\\n', '\n').replace('\\"', '"')
    
    # use extracted content if found, otherwise clean up raw output
    if extracted_content:
        display_content = extracted_content
    else:
        # try to strip json wrapper if present
        display_content = raw_output[:3000] if raw_output else "(no content)"
        # remove json cruft if it looks like raw json
        if display_content.strip().startswith('{'):
            # try to find meaningful text
            lines = display_content.split('\\n')
            clean_lines = [l for l in lines if not l.strip().startswith('"') and not l.strip().startswith('{')]
            if clean_lines:
                display_content = '\n'.join(clean_lines)
    
    return {
        "send_to": "planner",
        "visible_reasoning": extracted_reasoning or f"(partial output recovered - {error_msg})",
        "collaboration": extracted_collab,
        "content": display_content,
        "action_intent": "provide_info",
        "requires_tool": False,
        "_format_error": True,
        "_error_message": error_msg,
        "_raw_output": raw_output,
    }


def extract_agent_status(response: dict) -> str:
    """
    determine agent status from response.
    
    args:
        response: the parsed agent response
        
    returns:
        status string: "completed", "error", or "working"
    """
    if response.get("_format_error"):
        return "error"
    
    action_intent = response.get("action_intent", "")
    if action_intent == "error":
        return "error"
    elif action_intent == "complete":
        return "completed"
    
    return "completed"

