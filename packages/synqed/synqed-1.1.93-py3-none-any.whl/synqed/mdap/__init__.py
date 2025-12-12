"""
synqed.mdap - massively decomposed agentic processes (mdap/maker framework).

this module implements the maker framework from "solving a million-step llm task 
with zero errors" (meyerson et al., arxiv:2511.09030).

key components:
- maximal agentic decomposition (mad): tasks decomposed into m=1 step per agent.
- first-to-ahead-by-k voting: error correction at the subtask level via voting.
- red-flagging: discard risky outputs (too long, misformatted) instead of fixing.
- calibration: estimate per-step success rate p and cost c to choose models and k.

architecture:
- types: core data structures (stepinput, stepoutput, configs).
- red_flags: output validation / rejection logic.
- voting: first-to-ahead-by-k voting implementation.
- calibration: cost estimation and model selection.
- execution: main mdapexecutor orchestrating the full pipeline.
- step_runner: integration layer with synqed's agent system.

usage:
    from synqed.mdap import MdapExecutor, MdapConfig, ModelConfig
    from synqed.mdap import SynqedStepRunner, RedFlagger, Voter
    
    # configure
    model_config = ModelConfig(model="gpt-4.1-mini", provider="openai", ...)
    mdap_config = MdapConfig(k=3, max_votes_per_step=20, ...)
    
    # setup
    red_flagger = RedFlagger(max_output_tokens=750, ...)
    step_runner = SynqedStepRunner(model_config=model_config, ...)
    voter = Voter(step_runner=step_runner, red_flagger=red_flagger, k=mdap_config.k)
    
    # execute
    executor = MdapExecutor(mdap_config=mdap_config, voter=voter)
    results = executor.run_task(initial_state=..., num_steps=1_048_575)
"""

from synqed.mdap.types import (
    StepInput,
    StepOutput,
    StepSpec,
    ModelConfig,
    MdapConfig,
    VotingStats,
)
from synqed.mdap.red_flags import RedFlagger
from synqed.mdap.voting import Voter, VotingResult
from synqed.mdap.calibration import (
    CalibrationReport,
    estimate_p_and_cost,
    choose_k_for_target_success,
    compute_expected_cost,
)
from synqed.mdap.execution import MdapExecutor
from synqed.mdap.step_runner import StepRunnerInterface, SynqedStepRunner

__all__ = [
    # types
    "StepInput",
    "StepOutput",
    "StepSpec",
    "ModelConfig",
    "MdapConfig",
    "VotingStats",
    # red flagging
    "RedFlagger",
    # voting
    "Voter",
    "VotingResult",
    # calibration
    "CalibrationReport",
    "estimate_p_and_cost",
    "choose_k_for_target_success",
    "compute_expected_cost",
    # execution
    "MdapExecutor",
    # step runner
    "StepRunnerInterface",
    "SynqedStepRunner",
]

