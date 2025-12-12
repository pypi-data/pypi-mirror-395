"""
synqed.mdap.voting - first-to-ahead-by-k voting for error correction.

this module implements algorithm 2 (do_voting) from the paper:
- repeatedly sample candidate outputs for a step.
- maintain vote counts for each unique candidate.
- accept a candidate when its votes exceed the runner-up by at least k.

key equations:
- eq. 9: probability of correct candidate winning in first-to-ahead-by-k:
    p(correct) = p^k / (p^k + (1-p)^k) = 1 / (1 + ((1-p)/p)^k)
- eq. 12-13: extends to subtasks with m steps and full task with s/m subtasks.

this voting mechanism is a generalization of the gambler's ruin problem
and is motivated by the sequential probability ratio test (sprt).
"""

from __future__ import annotations

import logging
from typing import Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict

from synqed.mdap.types import StepInput, StepOutput, VotingStats

logger = logging.getLogger(__name__)


@dataclass
class VotingResult:
    """
    result of a voting round for a single step.
    
    attributes:
        step_input: the input to the step.
        winner: the winning stepoutput.
        stats: statistics collected during voting.
    """
    step_input: StepInput
    winner: StepOutput
    stats: VotingStats


class Voter:
    """
    voter: implements first-to-ahead-by-k voting for error correction.
    
    this class orchestrates the voting process:
    1. repeatedly call step_runner to sample candidates.
    2. use red_flagger to discard invalid samples.
    3. maintain vote counts for valid candidates.
    4. accept a candidate when lead >= k.
    
    usage:
        from synqed.mdap import Voter, RedFlagger, SynqedStepRunner
        
        red_flagger = RedFlagger(max_output_tokens=750, ...)
        step_runner = SynqedStepRunner(...)
        voter = Voter(step_runner=step_runner, red_flagger=red_flagger, k=3)
        
        result = voter.vote_until_decided(step_input)
        winning_output = result.winner
    """
    
    def __init__(
        self,
        step_runner: Any,  # StepRunnerInterface
        red_flagger: Any,  # RedFlagger
        k: int = 3,
        max_votes: int = 20,
        max_samples: int = 100,
        first_to_k: bool = False,
        normalize_fn: Optional[callable] = None,
    ):
        """
        initialize voter.
        
        args:
            step_runner: step runner that produces candidate stepoutputs.
            red_flagger: red flagger that validates outputs.
            k: vote margin threshold for first-to-ahead-by-k.
            max_votes: maximum number of valid votes per step.
            max_samples: maximum total samples (including red-flagged).
            first_to_k: if true, use simpler first-to-k instead of first-to-ahead-by-k.
            normalize_fn: optional function to normalize candidate outputs for comparison.
        """
        self.step_runner = step_runner
        self.red_flagger = red_flagger
        self.k = k
        self.max_votes = max_votes
        self.max_samples = max_samples
        self.first_to_k = first_to_k
        self.normalize_fn = normalize_fn or self._default_normalize
    
    def vote_until_decided(self, step_input: StepInput) -> VotingResult:
        """
        run voting until a candidate is decided (lead >= k).
        
        implements algorithm 2 from the paper:
        - v[y] = vote count for candidate y.
        - while true:
            - sample y from step_runner.
            - if y is valid (not red-flagged):
                - v[y] += 1.
                - if v[y] >= k + max(v[y'] for y' != y), return y.
        
        args:
            step_input: input to the step.
        
        returns:
            votingresult with winning output and statistics.
        """
        vote_counts: dict[str, int] = defaultdict(int)
        candidate_outputs: dict[str, StepOutput] = {}  # map from key to first occurrence
        
        stats = VotingStats(step_index=step_input.step_index)
        
        sample_count = 0
        valid_count = 0
        
        while sample_count < self.max_samples and valid_count < self.max_votes:
            # sample a candidate
            sample_count += 1
            output = self.step_runner.sample_once(step_input)
            
            # check red flags
            if not output.valid:
                stats.red_flagged_samples += 1
                continue
            
            # valid sample
            valid_count += 1
            
            # normalize candidate for comparison
            candidate_key = self.normalize_fn(output)
            
            # record first occurrence of this candidate
            if candidate_key not in candidate_outputs:
                candidate_outputs[candidate_key] = output
            
            # increment vote count
            vote_counts[candidate_key] += 1
            
            # check if we have a winner
            if self._check_winner(vote_counts, candidate_key):
                winner = candidate_outputs[candidate_key]
                
                # fill stats
                stats.total_samples = sample_count
                stats.valid_samples = valid_count
                stats.vote_counts = dict(vote_counts)
                stats.winner_votes = vote_counts[candidate_key]
                
                # find runner-up
                sorted_votes = sorted(vote_counts.values(), reverse=True)
                stats.runnerup_votes = sorted_votes[1] if len(sorted_votes) > 1 else 0
                stats.rounds_to_decide = valid_count
                
                logger.debug(
                    f"step {step_input.step_index}: decided in {valid_count} votes "
                    f"({sample_count} samples), winner={stats.winner_votes}, "
                    f"runnerup={stats.runnerup_votes}"
                )
                
                return VotingResult(
                    step_input=step_input,
                    winner=winner,
                    stats=stats,
                )
        
        # if we reach here, we exhausted max votes/samples without deciding
        # fallback: return candidate with most votes
        if not vote_counts:
            raise RuntimeError(
                f"step {step_input.step_index}: no valid samples after {sample_count} attempts"
            )
        
        best_key = max(vote_counts, key=vote_counts.get)
        winner = candidate_outputs[best_key]
        
        stats.total_samples = sample_count
        stats.valid_samples = valid_count
        stats.vote_counts = dict(vote_counts)
        stats.winner_votes = vote_counts[best_key]
        sorted_votes = sorted(vote_counts.values(), reverse=True)
        stats.runnerup_votes = sorted_votes[1] if len(sorted_votes) > 1 else 0
        stats.rounds_to_decide = valid_count
        
        logger.warning(
            f"step {step_input.step_index}: voting did not converge after "
            f"{sample_count} samples; returning best candidate with {stats.winner_votes} votes"
        )
        
        return VotingResult(
            step_input=step_input,
            winner=winner,
            stats=stats,
        )
    
    def _check_winner(self, vote_counts: dict[str, int], candidate_key: str) -> bool:
        """
        check if candidate_key is a winner according to voting rule.
        
        first-to-ahead-by-k: v[y] >= k + max(v[y'] for y' != y).
        first-to-k: v[y] >= k.
        """
        lead_votes = vote_counts[candidate_key]
        
        if self.first_to_k:
            # simpler: first to k votes wins
            return lead_votes >= self.k
        else:
            # first-to-ahead-by-k: lead must exceed runner-up by k
            runnerup_votes = 0
            for key, count in vote_counts.items():
                if key != candidate_key:
                    runnerup_votes = max(runnerup_votes, count)
            
            return lead_votes >= self.k + runnerup_votes
    
    def _default_normalize(self, output: StepOutput) -> str:
        """
        default normalization: convert action to a canonical string key.
        
        for structured outputs (dict, list, tuple), use json serialization.
        for others, use string representation.
        """
        action = output.action
        
        if isinstance(action, (dict, list, tuple)):
            import json
            return json.dumps(action, sort_keys=True)
        else:
            return str(action)


# ============================================================================
# utility functions for voting analysis
# ============================================================================

def compute_vote_success_probability(p: float, k: int) -> float:
    """
    compute probability of correct candidate winning in first-to-ahead-by-k voting.
    
    from eq. 9 in the paper:
        p_success = p^k / (p^k + (1-p)^k) = 1 / (1 + ((1-p)/p)^k)
    
    args:
        p: per-step success probability (0.5 < p < 1).
        k: vote margin.
    
    returns:
        probability that correct candidate wins.
    """
    if p <= 0.5:
        raise ValueError(f"p must be > 0.5 for voting to converge (got p={p})")
    
    return 1.0 / (1.0 + ((1.0 - p) / p) ** k)


def compute_full_task_success_probability(p: float, k: int, s: int, m: int = 1) -> float:
    """
    compute probability of successfully completing full task with voting.
    
    from eq. 13 in the paper:
        p_full = (1 / (1 + ((1-p)/p)^k))^(s/m)
    
    where:
    - p: per-step success probability.
    - k: vote margin.
    - s: total number of steps.
    - m: steps per subtask (usually m=1 for mad).
    
    args:
        p: per-step success probability.
        k: vote margin.
        s: total steps.
        m: steps per subtask (default 1 for mad).
    
    returns:
        probability of completing full task with zero errors.
    """
    p_sub = compute_vote_success_probability(p, k)
    num_subtasks = s / m
    return p_sub ** num_subtasks

