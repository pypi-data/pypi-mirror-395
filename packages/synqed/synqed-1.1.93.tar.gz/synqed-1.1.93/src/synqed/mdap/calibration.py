"""
synqed.mdap.calibration - cost estimation and model selection.

this module implements the calibration and cost estimation logic from
section 4.2-4.3 of the paper:
- estimate per-step success rate p from a sample of steps.
- use scaling laws (eq. 14, 17, 18) to project cost for full task.
- choose optimal k for a target success probability.
- select the most cost-effective model.

key equations:
- eq. 14: k_min = ceil(ln(t^(-m/s) - 1) / ln((1-p)/p))
  where t is target success probability, s is total steps, m is steps per subtask.
- eq. 18: E[cost] = Theta(p^(-1) * c * s * ln(s)) for m=1 (mad).

this allows us to:
1. run calibration on a small sample (e.g. 10k random steps).
2. estimate p and cost per sample.
3. project total cost for the full task (e.g. 1M steps).
4. choose the most cost-effective model and k value.
"""

from __future__ import annotations

import math
import logging
from typing import Any, Optional, Callable
from dataclasses import dataclass, field

from synqed.mdap.types import ModelConfig, StepInput, StepOutput

logger = logging.getLogger(__name__)


@dataclass
class CalibrationReport:
    """
    calibration report: results of estimating p and cost on a sample.
    
    attributes:
        model_name: name of the model calibrated.
        num_samples: number of steps sampled.
        p_estimate: estimated per-step success probability.
        p_std: standard error of p estimate.
        avg_input_tokens: average input tokens per step.
        avg_output_tokens: average output tokens per step.
        cost_per_sample: estimated cost per sample (input + output).
        k_min: recommended k for target success probability.
        projected_cost: projected total cost for full task.
        projected_samples: projected total samples (including red-flagged).
    """
    model_name: str
    num_samples: int
    p_estimate: float
    p_std: float = 0.0
    avg_input_tokens: float = 0.0
    avg_output_tokens: float = 0.0
    cost_per_sample: float = 0.0
    k_min: int = 1
    projected_cost: float = 0.0
    projected_samples: int = 0
    
    def __repr__(self) -> str:
        return (
            f"CalibrationReport(model={self.model_name}, p={self.p_estimate:.4f}, "
            f"k_min={self.k_min}, cost=${self.projected_cost:.2f})"
        )


def estimate_p_and_cost(
    model_config: ModelConfig,
    task_sampler: Callable[[int], StepInput],
    ground_truth_fn: Callable[[StepInput], Any],
    step_runner: Any,
    num_samples: int = 1000,
    target_success_prob: float = 0.95,
    total_steps: int = 1_000_000,
) -> CalibrationReport:
    """
    estimate per-step success rate p and projected cost for a model.
    
    this function:
    1. samples num_samples random steps using task_sampler.
    2. for each step, runs step_runner.sample_once() and compares to ground truth.
    3. computes empirical success rate p.
    4. computes average token usage and cost per sample.
    5. uses eq. 14 to compute k_min for target_success_prob.
    6. uses eq. 18 to project total cost for total_steps.
    
    args:
        model_config: model configuration with cost parameters.
        task_sampler: function that generates a random step input given an index.
        ground_truth_fn: function that returns the correct action for a step input.
        step_runner: step runner to sample outputs.
        num_samples: number of steps to sample for calibration.
        target_success_prob: target probability of full task success (default 0.95).
        total_steps: total number of steps in the full task.
    
    returns:
        calibrationreport with estimated p, k_min, and projected cost.
    """
    logger.info(
        f"calibrating {model_config.model} on {num_samples} samples "
        f"(target_p={target_success_prob}, total_steps={total_steps})"
    )
    
    correct_count = 0
    total_input_tokens = 0
    total_output_tokens = 0
    
    for i in range(num_samples):
        step_input = task_sampler(i)
        output = step_runner.sample_once(step_input)
        
        # only count valid samples
        if not output.valid:
            continue
        
        ground_truth = ground_truth_fn(step_input)
        
        # check if correct
        if _compare_actions(output.action, ground_truth):
            correct_count += 1
        
        total_input_tokens += output.tokens_input
        total_output_tokens += output.tokens_output
    
    # compute estimates
    p_estimate = correct_count / num_samples if num_samples > 0 else 0.0
    p_std = math.sqrt(p_estimate * (1 - p_estimate) / num_samples) if num_samples > 0 else 0.0
    
    avg_input_tokens = total_input_tokens / num_samples if num_samples > 0 else 0.0
    avg_output_tokens = total_output_tokens / num_samples if num_samples > 0 else 0.0
    
    cost_per_sample = (
        avg_input_tokens * model_config.cost_per_input_token +
        avg_output_tokens * model_config.cost_per_output_token
    )
    
    # compute k_min for target success probability
    k_min = choose_k_for_target_success(
        p=p_estimate,
        s=total_steps,
        target_success_prob=target_success_prob,
        m=1,  # mad
    )
    
    # project total cost
    projected_cost = compute_expected_cost(
        p=p_estimate,
        k=k_min,
        s=total_steps,
        c=cost_per_sample,
        m=1,  # mad
    )
    
    # project total samples (eq. 16)
    projected_samples = compute_expected_samples(
        p=p_estimate,
        k=k_min,
        s=total_steps,
        m=1,
    )
    
    report = CalibrationReport(
        model_name=model_config.model,
        num_samples=num_samples,
        p_estimate=p_estimate,
        p_std=p_std,
        avg_input_tokens=avg_input_tokens,
        avg_output_tokens=avg_output_tokens,
        cost_per_sample=cost_per_sample,
        k_min=k_min,
        projected_cost=projected_cost,
        projected_samples=projected_samples,
    )
    
    logger.info(f"calibration complete: {report}")
    return report


def choose_k_for_target_success(
    p: float,
    s: int,
    target_success_prob: float = 0.95,
    m: int = 1,
) -> int:
    """
    compute minimum k to achieve target success probability.
    
    from eq. 14 in the paper:
        k_min = ceil(ln(t^(-m/s) - 1) / ln((1-p)/p))
    
    where:
    - t: target success probability.
    - s: total steps.
    - m: steps per subtask.
    - p: per-step success probability.
    
    args:
        p: per-step success probability (must be > 0.5).
        s: total number of steps.
        target_success_prob: target probability of full task success.
        m: steps per subtask (default 1 for mad).
    
    returns:
        minimum k value.
    """
    if p <= 0.5:
        logger.warning(f"p={p} <= 0.5; voting will not converge!")
        return 1000  # effectively infeasible
    
    if target_success_prob <= 0 or target_success_prob >= 1:
        raise ValueError(f"target_success_prob must be in (0, 1), got {target_success_prob}")
    
    # eq. 14: k_min = ceil(ln(t^(-m/s) - 1) / ln((1-p)/p))
    num_subtasks = s / m
    numerator = math.log(target_success_prob ** (-1.0 / num_subtasks) - 1)
    denominator = math.log((1 - p) / p)
    
    k_min = math.ceil(numerator / denominator)
    return max(1, k_min)


def compute_expected_cost(
    p: float,
    k: int,
    s: int,
    c: float,
    m: int = 1,
) -> float:
    """
    compute expected cost of running mdap with given parameters.
    
    from eq. 17 in the paper:
        E[cost] ≈ (c * s * k) / (p^(m-1) * (2*p - 1))
    
    for m=1 (mad), this simplifies to (eq. 18):
        E[cost] = Theta(c * s * ln(s) / p)
    
    where k = Theta(ln(s)) from eq. 14.
    
    args:
        p: per-step success probability.
        k: vote margin.
        s: total steps.
        c: cost per sample.
        m: steps per subtask (default 1 for mad).
    
    returns:
        expected total cost.
    """
    if p <= 0.5:
        return float('inf')
    
    # eq. 17 (approximate)
    numerator = c * s * k
    denominator = (p ** (m - 1)) * (2 * p - 1)
    
    return numerator / denominator


def compute_expected_samples(
    p: float,
    k: int,
    s: int,
    m: int = 1,
) -> int:
    """
    compute expected total samples (including red-flagged) for full task.
    
    from eq. 16 in the paper:
        E[samples per subtask] = k * (2*p_sub - 1)^(-1)
    
    where p_sub is from eq. 12.
    
    args:
        p: per-step success probability.
        k: vote margin.
        s: total steps.
        m: steps per subtask.
    
    returns:
        expected total samples.
    """
    if p <= 0.5:
        return int(1e12)  # effectively infinite
    
    # p_sub from eq. 12
    p_sub = 1.0 / (1.0 + ((1.0 - p) / p) ** k)
    
    # samples per subtask
    samples_per_subtask = k * (2 * p_sub - 1) ** (-1)
    
    # total subtasks
    num_subtasks = s / m
    
    return int(samples_per_subtask * num_subtasks)


def _compare_actions(action1: Any, action2: Any) -> bool:
    """
    compare two actions for equality.
    
    handles structured types (list, dict, tuple) and primitives.
    """
    import json
    
    # normalize to comparable form
    def normalize(action):
        if isinstance(action, (dict, list, tuple)):
            return json.dumps(action, sort_keys=True)
        else:
            return str(action)
    
    return normalize(action1) == normalize(action2)


# ============================================================================
# multi-model comparison
# ============================================================================

def compare_models(
    model_configs: list[ModelConfig],
    task_sampler: Callable[[int], StepInput],
    ground_truth_fn: Callable[[StepInput], Any],
    step_runner_factory: Callable[[ModelConfig], Any],
    num_samples: int = 1000,
    target_success_prob: float = 0.95,
    total_steps: int = 1_000_000,
) -> list[CalibrationReport]:
    """
    compare multiple models and return calibration reports sorted by cost.
    
    this function:
    1. runs estimate_p_and_cost for each model.
    2. sorts models by projected cost (lowest to highest).
    3. returns list of calibrationreports.
    
    args:
        model_configs: list of model configurations to compare.
        task_sampler: function that generates random step inputs.
        ground_truth_fn: function that returns correct action for a step.
        step_runner_factory: function that creates step runner for a model config.
        num_samples: number of samples for calibration.
        target_success_prob: target success probability.
        total_steps: total steps in full task.
    
    returns:
        list of calibrationreports sorted by projected cost.
    """
    reports = []
    
    for model_config in model_configs:
        logger.info(f"calibrating model: {model_config.model}")
        
        step_runner = step_runner_factory(model_config)
        
        try:
            report = estimate_p_and_cost(
                model_config=model_config,
                task_sampler=task_sampler,
                ground_truth_fn=ground_truth_fn,
                step_runner=step_runner,
                num_samples=num_samples,
                target_success_prob=target_success_prob,
                total_steps=total_steps,
            )
            reports.append(report)
        except Exception as e:
            logger.error(f"error calibrating {model_config.model}: {e}")
    
    # sort by projected cost
    reports.sort(key=lambda r: r.projected_cost)
    
    return reports

