"""
synqed.mdap.types - core data structures for the mdap/maker framework.

this module defines the core types used throughout the mdap system:
- stepinput: input to a single micro-agent step.
- stepoutput: output from a single micro-agent step.
- stepspec: specification for how to interpret/validate a step.
- modelconfig: llm model configuration and cost parameters.
- mdapconfig: configuration for the mdap execution (k, thresholds, etc.).
- votingstats: statistics collected during a voting round.
"""

from __future__ import annotations

from typing import Any, Optional
from dataclasses import dataclass, field
from pydantic import BaseModel, Field


# ============================================================================
# step-level data structures
# ============================================================================

@dataclass
class StepInput:
    """
    input to a single step in the mdap pipeline.
    
    in maximal agentic decomposition (mad), each step corresponds to
    a single logical decision. the stepinput contains all context needed
    for a micro-agent to make that decision.
    
    attributes:
        step_index: index of this step (0-indexed).
        total_steps: total number of steps in the task.
        state: task-specific state (e.g. hanoi configuration, board state).
        metadata: additional context (strategy, role, previous action, etc.).
    """
    step_index: int
    total_steps: int
    state: Any  # task-specific state representation
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def __repr__(self) -> str:
        return f"StepInput(step={self.step_index}/{self.total_steps})"


@dataclass
class StepOutput:
    """
    output from a single step in the mdap pipeline.
    
    attributes:
        action: the action/decision produced by the micro-agent.
        next_state: the resulting state after applying the action.
        raw_text: raw llm response text (for debugging/analysis).
        valid: whether the output passed red-flag validation.
        red_flags: list of red flag reasons if invalid.
        tokens_input: number of input tokens used.
        tokens_output: number of output tokens generated.
    """
    action: Any
    next_state: Any
    raw_text: str
    valid: bool = True
    red_flags: list[str] = field(default_factory=list)
    tokens_input: int = 0
    tokens_output: int = 0
    
    def __repr__(self) -> str:
        status = "valid" if self.valid else f"invalid({','.join(self.red_flags)})"
        return f"StepOutput(action={self.action}, {status})"


@dataclass
class StepSpec:
    """
    specification for how to interpret and validate a step.
    
    this is optional and task-specific. for structured tasks like hanoi,
    it defines the expected output format, required fields, validation logic, etc.
    
    attributes:
        output_schema: expected output schema (e.g. json schema, regex pattern).
        required_fields: list of required field names in the output.
        validation_fn: optional custom validation function.
        description: human-readable description of the step type.
    """
    output_schema: Optional[dict[str, Any]] = None
    required_fields: list[str] = field(default_factory=list)
    validation_fn: Optional[callable] = None
    description: str = ""


# ============================================================================
# configuration structures
# ============================================================================

class ModelConfig(BaseModel):
    """
    configuration for the base llm model used in mdap.
    
    includes cost parameters for cost estimation (eq. 18 in the paper).
    
    attributes:
        provider: llm provider ("openai", "anthropic", "together", etc.).
        model: model name (e.g. "gpt-4.1-mini", "claude-sonnet-4").
        api_key: api key for the provider.
        temperature: sampling temperature (default 0.1 for voting after first).
        max_output_tokens: maximum output tokens per call.
        cost_per_input_token: cost per input token (in dollars).
        cost_per_output_token: cost per output token (in dollars).
        avg_input_tokens: estimated average input tokens per step.
        avg_output_tokens: estimated average output tokens per step.
    """
    provider: str = Field(description="llm provider (openai, anthropic, etc.)")
    model: str = Field(description="model name")
    api_key: Optional[str] = Field(default=None, description="api key")
    temperature: float = Field(default=0.1, description="sampling temperature")
    max_output_tokens: int = Field(default=750, description="max output tokens")
    
    # cost parameters for calibration
    cost_per_input_token: float = Field(default=0.0, description="cost per input token ($)")
    cost_per_output_token: float = Field(default=0.0, description="cost per output token ($)")
    avg_input_tokens: float = Field(default=0.0, description="avg input tokens per step")
    avg_output_tokens: float = Field(default=0.0, description="avg output tokens per step")
    
    class Config:
        frozen = False


class MdapConfig(BaseModel):
    """
    configuration for the mdap execution pipeline.
    
    implements parameters for the maker framework:
    - k: vote margin for first-to-ahead-by-k voting (eq. 9, alg. 2).
    - red flag thresholds.
    - parallelism and retry limits.
    
    attributes:
        k: vote margin threshold for first-to-ahead-by-k voting.
        max_votes_per_step: maximum number of votes to collect per step.
        max_red_flag_retries: max retries when hitting red flags.
        red_flag_max_output_tokens: threshold for "too long" red flag.
        red_flag_strict_format: whether to strictly enforce output format.
        first_vote_temperature: temperature for first vote (usually 0).
        subsequent_vote_temperature: temperature for subsequent votes.
        parallelism: number of parallel llm calls (for future optimization).
    """
    k: int = Field(default=3, description="vote margin for first-to-ahead-by-k")
    max_votes_per_step: int = Field(default=20, description="max votes per step")
    max_red_flag_retries: int = Field(default=100, description="max red flag retries")
    
    # red flag thresholds
    red_flag_max_output_tokens: int = Field(default=750, description="max output length")
    red_flag_strict_format: bool = Field(default=True, description="strict format check")
    
    # temperature settings
    first_vote_temperature: float = Field(default=0.0, description="temp for first vote")
    subsequent_vote_temperature: float = Field(default=0.1, description="temp for other votes")
    
    # parallelism (future optimization)
    parallelism: int = Field(default=1, description="parallel llm calls")
    
    class Config:
        frozen = False


# ============================================================================
# statistics structures
# ============================================================================

@dataclass
class VotingStats:
    """
    statistics collected during a voting round for a single step.
    
    used for analysis and debugging of the voting process.
    
    attributes:
        step_index: index of the step.
        total_samples: total number of samples drawn (including red-flagged).
        valid_samples: number of valid samples (passed red-flag check).
        red_flagged_samples: number of red-flagged samples.
        vote_counts: mapping from candidate key to vote count.
        winner_votes: number of votes for the winning candidate.
        runnerup_votes: number of votes for the runner-up.
        rounds_to_decide: number of valid votes required to decide.
    """
    step_index: int
    total_samples: int = 0
    valid_samples: int = 0
    red_flagged_samples: int = 0
    vote_counts: dict[str, int] = field(default_factory=dict)
    winner_votes: int = 0
    runnerup_votes: int = 0
    rounds_to_decide: int = 0
    
    def __repr__(self) -> str:
        return (
            f"VotingStats(step={self.step_index}, "
            f"samples={self.total_samples}, valid={self.valid_samples}, "
            f"winner={self.winner_votes}, runnerup={self.runnerup_votes})"
        )

