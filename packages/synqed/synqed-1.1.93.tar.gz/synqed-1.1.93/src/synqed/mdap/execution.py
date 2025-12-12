"""
synqed.mdap.execution - main executor for massively decomposed agentic processes.

this module implements the main execution loop for the mdap/maker framework:
- algorithm 1 (generate_solution): orchestrate s steps with voting.
- maximal agentic decomposition (mad): each step is handled by a micro-agent.
- first-to-ahead-by-k voting at each step.
- red-flagging to discard risky outputs.

the executor is the top-level interface to the mdap system. it coordinates
the voter, step runner, and red-flagger to produce a sequence of actions
that solves the task with zero errors.
"""

from __future__ import annotations

import logging
from typing import Any, Optional, Callable
from dataclasses import dataclass, field

from synqed.mdap.types import StepInput, StepOutput, MdapConfig, VotingStats
from synqed.mdap.voting import Voter, VotingResult

logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """
    result of executing a full mdap task.
    
    attributes:
        initial_state: initial task state.
        final_state: final task state after all steps.
        actions: list of actions taken at each step.
        step_outputs: list of stepoutputs from each step.
        voting_stats: list of votingstats from each step.
        total_samples: total llm calls (including red-flagged).
        total_valid_samples: total valid llm calls.
        total_red_flagged: total red-flagged samples.
        success: whether the task completed successfully.
        error_message: error message if not successful.
    """
    initial_state: Any
    final_state: Any
    actions: list[Any] = field(default_factory=list)
    step_outputs: list[StepOutput] = field(default_factory=list)
    voting_stats: list[VotingStats] = field(default_factory=list)
    total_samples: int = 0
    total_valid_samples: int = 0
    total_red_flagged: int = 0
    success: bool = True
    error_message: str = ""
    
    def __repr__(self) -> str:
        status = "success" if self.success else f"failed: {self.error_message}"
        return (
            f"ExecutionResult({status}, steps={len(self.actions)}, "
            f"samples={self.total_samples}, valid={self.total_valid_samples})"
        )


class MdapExecutor:
    """
    main executor for massively decomposed agentic processes.
    
    implements algorithm 1 (generate_solution) from the paper:
    - initialize action list a = [].
    - initialize state x = x0.
    - for s steps:
        - a_i, x = do_voting(x, m, k).
        - append a_i to a.
    - return a.
    
    usage:
        from synqed.mdap import MdapExecutor, MdapConfig, Voter
        from synqed.mdap import RedFlagger, SynqedStepRunner
        
        # setup
        red_flagger = RedFlagger(...)
        step_runner = SynqedStepRunner(...)
        voter = Voter(step_runner=step_runner, red_flagger=red_flagger, k=3)
        
        # execute
        executor = MdapExecutor(mdap_config=MdapConfig(k=3), voter=voter)
        result = executor.run_task(
            initial_state=hanoi_initial_state,
            num_steps=1_048_575,
        )
        
        if result.success:
            print(f"task completed with {len(result.actions)} steps!")
    """
    
    def __init__(
        self,
        mdap_config: MdapConfig,
        voter: Voter,
        state_builder: Optional[Callable[[Any], dict]] = None,
        validator: Optional[Callable[[Any, list[Any]], tuple[bool, str]]] = None,
    ):
        """
        initialize mdap executor.
        
        args:
            mdap_config: mdap configuration (k, thresholds, etc.).
            voter: voter for first-to-ahead-by-k voting.
            state_builder: optional function to build metadata dict from current state.
            validator: optional function to validate final result (state, actions) -> (is_valid, message).
        """
        self.mdap_config = mdap_config
        self.voter = voter
        self.state_builder = state_builder or (lambda s: {})
        self.validator = validator
    
    def run_task(
        self,
        initial_state: Any,
        num_steps: int,
        verbose: bool = True,
    ) -> ExecutionResult:
        """
        run the full task with maximal agentic decomposition and voting.
        
        this is the main entry point to the mdap system. it executes
        num_steps steps, each with first-to-ahead-by-k voting.
        
        args:
            initial_state: initial task state.
            num_steps: total number of steps to execute.
            verbose: whether to log progress.
        
        returns:
            executionresult with actions, stats, and final state.
        """
        logger.info(f"starting mdap execution: {num_steps} steps, k={self.mdap_config.k}")
        
        # initialize
        current_state = initial_state
        actions = []
        step_outputs = []
        voting_stats = []
        
        total_samples = 0
        total_valid_samples = 0
        total_red_flagged = 0
        
        # execute steps
        for step_idx in range(num_steps):
            # build step input
            step_input = StepInput(
                step_index=step_idx,
                total_steps=num_steps,
                state=current_state,
                metadata=self.state_builder(current_state),
            )
            
            # run voting for this step
            try:
                voting_result = self.voter.vote_until_decided(step_input)
            except Exception as e:
                logger.error(f"voting failed at step {step_idx}: {e}")
                return ExecutionResult(
                    initial_state=initial_state,
                    final_state=current_state,
                    actions=actions,
                    step_outputs=step_outputs,
                    voting_stats=voting_stats,
                    total_samples=total_samples,
                    total_valid_samples=total_valid_samples,
                    total_red_flagged=total_red_flagged,
                    success=False,
                    error_message=str(e),
                )
            
            # extract winner
            winner = voting_result.winner
            stats = voting_result.stats
            
            # update state
            current_state = winner.next_state
            actions.append(winner.action)
            step_outputs.append(winner)
            voting_stats.append(stats)
            
            # update totals
            total_samples += stats.total_samples
            total_valid_samples += stats.valid_samples
            total_red_flagged += stats.red_flagged_samples
            
            # log progress
            if verbose and (step_idx + 1) % 1000 == 0:
                logger.info(
                    f"step {step_idx + 1}/{num_steps}: "
                    f"samples={stats.total_samples}, valid={stats.valid_samples}, "
                    f"winner_votes={stats.winner_votes}"
                )
        
        # validate final result
        if self.validator:
            is_valid, error_msg = self.validator(current_state, actions)
            if not is_valid:
                logger.error(f"validation failed: {error_msg}")
                return ExecutionResult(
                    initial_state=initial_state,
                    final_state=current_state,
                    actions=actions,
                    step_outputs=step_outputs,
                    voting_stats=voting_stats,
                    total_samples=total_samples,
                    total_valid_samples=total_valid_samples,
                    total_red_flagged=total_red_flagged,
                    success=False,
                    error_message=error_msg,
                )
        
        logger.info(
            f"mdap execution complete: {num_steps} steps, "
            f"{total_samples} total samples, {total_valid_samples} valid"
        )
        
        return ExecutionResult(
            initial_state=initial_state,
            final_state=current_state,
            actions=actions,
            step_outputs=step_outputs,
            voting_stats=voting_stats,
            total_samples=total_samples,
            total_valid_samples=total_valid_samples,
            total_red_flagged=total_red_flagged,
            success=True,
        )
    
    def run_step(self, step_input: StepInput) -> VotingResult:
        """
        run a single step with voting.
        
        this is useful for:
        - calibration (sampling random steps).
        - debugging (running specific steps).
        
        args:
            step_input: input to the step.
        
        returns:
            votingresult with winning output and stats.
        """
        return self.voter.vote_until_decided(step_input)


# ============================================================================
# execution statistics and analysis
# ============================================================================

def analyze_execution_result(result: ExecutionResult) -> dict[str, Any]:
    """
    analyze execution result and return statistics.
    
    computes:
    - total/valid/red-flagged samples.
    - average samples per step.
    - distribution of votes required (histogram).
    - steps that required > k rounds.
    - collision rate (steps with multiple votes for incorrect candidates).
    
    args:
        result: execution result.
    
    returns:
        dict of statistics.
    """
    num_steps = len(result.actions)
    
    # basic stats
    stats = {
        "num_steps": num_steps,
        "total_samples": result.total_samples,
        "total_valid_samples": result.total_valid_samples,
        "total_red_flagged": result.total_red_flagged,
        "avg_samples_per_step": result.total_samples / num_steps if num_steps > 0 else 0,
        "avg_valid_per_step": result.total_valid_samples / num_steps if num_steps > 0 else 0,
        "red_flag_rate": result.total_red_flagged / result.total_samples if result.total_samples > 0 else 0,
    }
    
    # voting distribution
    rounds_histogram = {}
    for vs in result.voting_stats:
        rounds = vs.rounds_to_decide
        rounds_histogram[rounds] = rounds_histogram.get(rounds, 0) + 1
    
    stats["rounds_histogram"] = rounds_histogram
    
    # steps requiring > k rounds
    k = result.voting_stats[0].winner_votes - result.voting_stats[0].runnerup_votes if result.voting_stats else 0
    high_rounds_steps = [
        vs.step_index for vs in result.voting_stats if vs.rounds_to_decide > k + 2
    ]
    stats["high_rounds_steps"] = high_rounds_steps
    stats["num_high_rounds_steps"] = len(high_rounds_steps)
    
    return stats


def print_execution_summary(result: ExecutionResult):
    """print a human-readable summary of execution result."""
    print(f"\n{'='*60}")
    print(f"MDAP Execution Summary")
    print(f"{'='*60}")
    print(f"Status: {'✓ SUCCESS' if result.success else '✗ FAILED'}")
    if not result.success:
        print(f"Error: {result.error_message}")
    print(f"Steps: {len(result.actions)}")
    print(f"Total samples: {result.total_samples}")
    print(f"Valid samples: {result.total_valid_samples}")
    print(f"Red-flagged: {result.total_red_flagged} ({result.total_red_flagged / result.total_samples * 100:.2f}%)")
    print(f"Avg samples/step: {result.total_samples / len(result.actions):.2f}")
    print(f"{'='*60}\n")
    
    # analyze
    stats = analyze_execution_result(result)
    print(f"Voting rounds distribution:")
    for rounds, count in sorted(stats["rounds_histogram"].items()):
        print(f"  {rounds} rounds: {count} steps")
    
    if stats["num_high_rounds_steps"] > 0:
        print(f"\nSteps requiring many rounds: {stats['num_high_rounds_steps']}")
        print(f"  (indices: {stats['high_rounds_steps'][:10]}...)")

