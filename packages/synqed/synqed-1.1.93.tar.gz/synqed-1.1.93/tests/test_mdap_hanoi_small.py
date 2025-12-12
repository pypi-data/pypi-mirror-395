"""
integration tests for hanoi with small disk counts using mdap/maker.

these tests verify end-to-end functionality:
- small hanoi problems (5-7 disks) can be solved with zero errors.
- voting converges correctly on real llm-like tasks.
- red-flagging works in practice.
- final state is correct.

note: these tests use mock step runners (not real llms) to avoid
external dependencies and api costs in test suite.
"""

import pytest
from typing import Any

from synqed.mdap import (
    MdapExecutor,
    MdapConfig,
    RedFlagger,
    Voter,
    StepInput,
    StepOutput,
)


# ============================================================================
# hanoi domain (simplified)
# ============================================================================

class SimpleHanoiState:
    """simplified hanoi state for testing."""
    
    def __init__(self, num_disks: int):
        self.num_disks = num_disks
        self.pegs = [list(range(num_disks, 0, -1)), [], []]
    
    def copy(self):
        new_state = SimpleHanoiState(self.num_disks)
        new_state.pegs = [peg[:] for peg in self.pegs]
        return new_state
    
    def move(self, disk: int, from_peg: int, to_peg: int):
        """apply a move."""
        self.pegs[from_peg].remove(disk)
        self.pegs[to_peg].append(disk)
    
    def is_solved(self) -> bool:
        return len(self.pegs[2]) == self.num_disks
    
    def to_list(self):
        return [peg[:] for peg in self.pegs]
    
    @classmethod
    def from_list(cls, pegs):
        num_disks = sum(len(peg) for peg in pegs)
        state = cls(num_disks)
        state.pegs = [peg[:] for peg in pegs]
        return state


def solve_hanoi_optimal(num_disks: int) -> list[tuple[int, int, int]]:
    """
    generate optimal hanoi solution (for even number of disks).
    
    returns list of (disk, from_peg, to_peg) moves.
    """
    moves = []
    
    def hanoi_recursive(n, source, target, auxiliary):
        if n == 1:
            moves.append((1, source, target))
        else:
            hanoi_recursive(n - 1, source, auxiliary, target)
            moves.append((n, source, target))
            hanoi_recursive(n - 1, auxiliary, target, source)
    
    hanoi_recursive(num_disks, 0, 2, 1)
    return moves


# ============================================================================
# mock step runner with known solution
# ============================================================================

class HanoiMockStepRunner:
    """
    mock step runner that knows the optimal hanoi solution.
    
    simulates an llm with:
    - probability p of returning correct move.
    - probability (1-p) of returning a plausible but wrong move.
    """
    
    def __init__(self, num_disks: int, p: float = 0.9):
        self.num_disks = num_disks
        self.p = p
        self.optimal_solution = solve_hanoi_optimal(num_disks)
        self.step_count = 0
    
    def sample_once(self, step_input: StepInput) -> StepOutput:
        """sample a candidate move."""
        import random
        
        current_state = SimpleHanoiState.from_list(step_input.state)
        step_idx = step_input.step_index
        
        # get correct move
        if step_idx < len(self.optimal_solution):
            correct_move = list(self.optimal_solution[step_idx])
        else:
            correct_move = None
        
        # sample with probability p
        if random.random() < self.p and correct_move:
            action = correct_move
        else:
            # generate a random legal move (usually wrong)
            action = self._random_legal_move(current_state)
        
        # compute next state
        if action:
            next_state = current_state.copy()
            try:
                next_state.move(action[0], action[1], action[2])
                next_state_list = next_state.to_list()
            except:
                next_state_list = current_state.to_list()
        else:
            next_state_list = current_state.to_list()
        
        # occasionally return overly long output (for red-flag testing)
        if random.random() < 0.1:
            raw_text = "x" * 1000  # too long
            valid = False
            red_flags = ["too_long"]
        else:
            raw_text = f"move = {action}"
            valid = True
            red_flags = []
        
        return StepOutput(
            action=action,
            next_state=next_state_list,
            raw_text=raw_text,
            valid=valid,
            red_flags=red_flags,
        )
    
    def _random_legal_move(self, state: SimpleHanoiState) -> list[int]:
        """generate a random legal move."""
        import random
        
        legal_moves = []
        for from_peg_idx in range(3):
            if not state.pegs[from_peg_idx]:
                continue
            
            disk = state.pegs[from_peg_idx][-1]
            
            for to_peg_idx in range(3):
                if to_peg_idx == from_peg_idx:
                    continue
                
                to_peg = state.pegs[to_peg_idx]
                if not to_peg or to_peg[-1] > disk:
                    legal_moves.append([disk, from_peg_idx, to_peg_idx])
        
        if legal_moves:
            return random.choice(legal_moves)
        else:
            return None


# ============================================================================
# integration tests
# ============================================================================

def test_hanoi_3_disks_with_voting():
    """test solving hanoi with 3 disks using voting."""
    num_disks = 3
    total_steps = 2 ** num_disks - 1  # 7 steps
    p = 0.8
    k = 3
    
    # setup
    step_runner = HanoiMockStepRunner(num_disks=num_disks, p=p)
    red_flagger = RedFlagger(max_output_tokens=500)
    voter = Voter(
        step_runner=step_runner,
        red_flagger=red_flagger,
        k=k,
    )
    
    mdap_config = MdapConfig(k=k)
    executor = MdapExecutor(mdap_config=mdap_config, voter=voter)
    
    # initial state
    initial_state = SimpleHanoiState(num_disks).to_list()
    
    # run
    result = executor.run_task(
        initial_state=initial_state,
        num_steps=total_steps,
        verbose=False,
    )
    
    # verify
    assert result.success
    assert len(result.actions) == total_steps
    
    # check final state (all disks on peg 2)
    final_state = SimpleHanoiState.from_list(result.final_state)
    assert final_state.is_solved()


def test_hanoi_5_disks_with_voting():
    """test solving hanoi with 5 disks using voting."""
    num_disks = 5
    total_steps = 2 ** num_disks - 1  # 31 steps
    p = 0.75
    k = 3
    
    # setup
    step_runner = HanoiMockStepRunner(num_disks=num_disks, p=p)
    red_flagger = RedFlagger(max_output_tokens=500)
    voter = Voter(
        step_runner=step_runner,
        red_flagger=red_flagger,
        k=k,
    )
    
    mdap_config = MdapConfig(k=k)
    executor = MdapExecutor(mdap_config=mdap_config, voter=voter)
    
    # initial state
    initial_state = SimpleHanoiState(num_disks).to_list()
    
    # run
    result = executor.run_task(
        initial_state=initial_state,
        num_steps=total_steps,
        verbose=False,
    )
    
    # verify
    assert result.success
    assert len(result.actions) == total_steps
    
    final_state = SimpleHanoiState.from_list(result.final_state)
    assert final_state.is_solved()


@pytest.mark.slow
def test_hanoi_7_disks_with_voting():
    """test solving hanoi with 7 disks using voting (slower test)."""
    num_disks = 7
    total_steps = 2 ** num_disks - 1  # 127 steps
    p = 0.7
    k = 3
    
    # setup
    step_runner = HanoiMockStepRunner(num_disks=num_disks, p=p)
    red_flagger = RedFlagger(max_output_tokens=500)
    voter = Voter(
        step_runner=step_runner,
        red_flagger=red_flagger,
        k=k,
    )
    
    mdap_config = MdapConfig(k=k)
    executor = MdapExecutor(mdap_config=mdap_config, voter=voter)
    
    # initial state
    initial_state = SimpleHanoiState(num_disks).to_list()
    
    # run
    result = executor.run_task(
        initial_state=initial_state,
        num_steps=total_steps,
        verbose=False,
    )
    
    # verify
    assert result.success
    assert len(result.actions) == total_steps
    
    final_state = SimpleHanoiState.from_list(result.final_state)
    assert final_state.is_solved()


def test_hanoi_with_red_flagging():
    """test that red-flagging discards bad samples."""
    num_disks = 3
    total_steps = 2 ** num_disks - 1
    p = 0.8
    k = 3
    
    # setup
    step_runner = HanoiMockStepRunner(num_disks=num_disks, p=p)
    red_flagger = RedFlagger(max_output_tokens=500)
    voter = Voter(
        step_runner=step_runner,
        red_flagger=red_flagger,
        k=k,
    )
    
    mdap_config = MdapConfig(k=k)
    executor = MdapExecutor(mdap_config=mdap_config, voter=voter)
    
    # initial state
    initial_state = SimpleHanoiState(num_disks).to_list()
    
    # run
    result = executor.run_task(
        initial_state=initial_state,
        num_steps=total_steps,
        verbose=False,
    )
    
    # verify red-flagging occurred
    assert result.total_red_flagged > 0
    assert result.total_samples > result.total_valid_samples
    
    # but task still succeeded
    assert result.success
    final_state = SimpleHanoiState.from_list(result.final_state)
    assert final_state.is_solved()


def test_hanoi_statistics_collection():
    """test that execution statistics are collected correctly."""
    num_disks = 3
    total_steps = 2 ** num_disks - 1
    p = 0.8
    k = 3
    
    # setup
    step_runner = HanoiMockStepRunner(num_disks=num_disks, p=p)
    red_flagger = RedFlagger(max_output_tokens=500)
    voter = Voter(
        step_runner=step_runner,
        red_flagger=red_flagger,
        k=k,
    )
    
    mdap_config = MdapConfig(k=k)
    executor = MdapExecutor(mdap_config=mdap_config, voter=voter)
    
    # initial state
    initial_state = SimpleHanoiState(num_disks).to_list()
    
    # run
    result = executor.run_task(
        initial_state=initial_state,
        num_steps=total_steps,
        verbose=False,
    )
    
    # check stats
    assert len(result.voting_stats) == total_steps
    assert result.total_samples > 0
    assert result.total_valid_samples > 0
    
    # each step should have stats
    for stats in result.voting_stats:
        assert stats.winner_votes >= k
        assert stats.total_samples >= stats.valid_samples


def test_hanoi_first_to_k_variant():
    """test first-to-k voting (simpler variant)."""
    num_disks = 3
    total_steps = 2 ** num_disks - 1
    p = 0.85
    k = 5
    
    # setup with first_to_k=True
    step_runner = HanoiMockStepRunner(num_disks=num_disks, p=p)
    red_flagger = RedFlagger(max_output_tokens=500)
    voter = Voter(
        step_runner=step_runner,
        red_flagger=red_flagger,
        k=k,
        first_to_k=True,
    )
    
    mdap_config = MdapConfig(k=k)
    executor = MdapExecutor(mdap_config=mdap_config, voter=voter)
    
    # initial state
    initial_state = SimpleHanoiState(num_disks).to_list()
    
    # run
    result = executor.run_task(
        initial_state=initial_state,
        num_steps=total_steps,
        verbose=False,
    )
    
    # verify
    assert result.success
    final_state = SimpleHanoiState.from_list(result.final_state)
    assert final_state.is_solved()
    
    # in first-to-k, winner should have at least k votes
    for stats in result.voting_stats:
        assert stats.winner_votes >= k

