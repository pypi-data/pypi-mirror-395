"""
synqed.mdap.step_runner - integration layer between mdap and synqed agents.

this module provides the step runner interface that connects the mdap
voting/execution pipeline with synqed's agent system.

key responsibilities:
- convert stepinput → agent prompt/context.
- call llm via synqed's abstractions or directly.
- parse llm response → stepoutput.
- apply red-flagging validation.

the step runner is intentionally stateless: each call represents a
single micro-agent invocation with minimal context (mad principle).
"""

from __future__ import annotations

import logging
import asyncio
from typing import Any, Optional, Callable
from abc import ABC, abstractmethod

from synqed.mdap.types import StepInput, StepOutput, ModelConfig
from synqed.mdap.red_flags import RedFlagger

logger = logging.getLogger(__name__)


# ============================================================================
# step runner interface
# ============================================================================

class StepRunnerInterface(ABC):
    """
    abstract interface for step runners.
    
    a step runner takes a stepinput and produces a stepoutput by:
    1. constructing a prompt from the step input.
    2. calling an llm.
    3. parsing the response.
    4. validating with red-flagger.
    """
    
    @abstractmethod
    def sample_once(self, step_input: StepInput) -> StepOutput:
        """
        sample a single output for the given step.
        
        args:
            step_input: input to the step.
        
        returns:
            stepoutput (may be invalid if red-flagged).
        """
        pass


# ============================================================================
# synqed-integrated step runner
# ============================================================================

class SynqedStepRunner(StepRunnerInterface):
    """
    step runner that integrates with synqed's agent system.
    
    this runner:
    - uses synqed's agent abstractions where possible.
    - supports both async and sync execution.
    - applies red-flagging to validate outputs.
    
    usage:
        model_config = ModelConfig(model="gpt-4.1-mini", provider="openai", ...)
        red_flagger = RedFlagger(max_output_tokens=750, ...)
        
        step_runner = SynqedStepRunner(
            model_config=model_config,
            red_flagger=red_flagger,
            prompt_builder=build_hanoi_prompt,
            response_parser=parse_hanoi_response,
        )
        
        output = step_runner.sample_once(step_input)
    """
    
    def __init__(
        self,
        model_config: ModelConfig,
        red_flagger: RedFlagger,
        prompt_builder: Callable[[StepInput], str],
        response_parser: Callable[[str], tuple[Any, Any]],
        system_prompt: Optional[str] = None,
        use_async: bool = False,
    ):
        """
        initialize synqed step runner.
        
        args:
            model_config: model configuration.
            red_flagger: red flagger for validation.
            prompt_builder: function that builds prompt from step input.
            response_parser: function that parses llm response to (action, next_state).
            system_prompt: optional system prompt (strategy, instructions, etc.).
            use_async: whether to use async llm calls.
        """
        self.model_config = model_config
        self.red_flagger = red_flagger
        self.prompt_builder = prompt_builder
        self.response_parser = response_parser
        self.system_prompt = system_prompt or ""
        self.use_async = use_async
        
        # initialize llm client
        self._init_llm_client()
    
    def _init_llm_client(self):
        """initialize llm client based on provider."""
        provider = self.model_config.provider
        api_key = self.model_config.api_key
        
        if provider == "openai":
            try:
                from openai import OpenAI, AsyncOpenAI
                if self.use_async:
                    self.client = AsyncOpenAI(api_key=api_key)
                else:
                    self.client = OpenAI(api_key=api_key)
            except ImportError:
                raise ImportError("openai package required: pip install openai")
        
        elif provider == "anthropic":
            try:
                from anthropic import Anthropic, AsyncAnthropic
                if self.use_async:
                    self.client = AsyncAnthropic(api_key=api_key)
                else:
                    self.client = Anthropic(api_key=api_key)
            except ImportError:
                raise ImportError("anthropic package required: pip install anthropic")
        
        else:
            raise ValueError(f"unsupported provider: {provider}")
    
    def sample_once(self, step_input: StepInput) -> StepOutput:
        """
        sample a single output for the given step (sync).
        
        args:
            step_input: input to the step.
        
        returns:
            stepoutput (may be invalid if red-flagged).
        """
        if self.use_async:
            # run async in sync context
            return asyncio.run(self._sample_once_async(step_input))
        else:
            return self._sample_once_sync(step_input)
    
    def _sample_once_sync(self, step_input: StepInput) -> StepOutput:
        """synchronous sampling."""
        # build prompt
        prompt = self.prompt_builder(step_input)
        
        # determine temperature
        temperature = (
            self.model_config.temperature
            if step_input.step_index > 0
            else 0.0  # first vote uses temp=0
        )
        
        # call llm
        provider = self.model_config.provider
        model = self.model_config.model
        max_tokens = self.model_config.max_output_tokens
        
        try:
            if provider == "openai":
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                raw_text = response.choices[0].message.content
                tokens_input = response.usage.prompt_tokens
                tokens_output = response.usage.completion_tokens
            
            elif provider == "anthropic":
                response = self.client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=self.system_prompt,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw_text = response.content[0].text
                tokens_input = response.usage.input_tokens
                tokens_output = response.usage.output_tokens
            
            else:
                raise ValueError(f"unsupported provider: {provider}")
        
        except Exception as e:
            logger.error(f"llm call error: {e}")
            return StepOutput(
                action=None,
                next_state=None,
                raw_text=str(e),
                valid=False,
                red_flags=["llm_error"],
                tokens_input=0,
                tokens_output=0,
            )
        
        # parse response
        try:
            action, next_state = self.response_parser(raw_text)
            parsed_output = {"action": action, "next_state": next_state}
        except Exception as e:
            logger.debug(f"parse error: {e}")
            action = None
            next_state = None
            parsed_output = None
        
        # red-flag validation
        is_valid, red_flags = self.red_flagger.evaluate(
            raw_text=raw_text,
            parsed_output=parsed_output,
            step_input=step_input,
        )
        
        return StepOutput(
            action=action,
            next_state=next_state,
            raw_text=raw_text,
            valid=is_valid,
            red_flags=red_flags,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
        )
    
    async def _sample_once_async(self, step_input: StepInput) -> StepOutput:
        """asynchronous sampling."""
        # build prompt
        prompt = self.prompt_builder(step_input)
        
        # determine temperature
        temperature = (
            self.model_config.temperature
            if step_input.step_index > 0
            else 0.0
        )
        
        # call llm
        provider = self.model_config.provider
        model = self.model_config.model
        max_tokens = self.model_config.max_output_tokens
        
        try:
            if provider == "openai":
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                raw_text = response.choices[0].message.content
                tokens_input = response.usage.prompt_tokens
                tokens_output = response.usage.completion_tokens
            
            elif provider == "anthropic":
                response = await self.client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=self.system_prompt,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw_text = response.content[0].text
                tokens_input = response.usage.input_tokens
                tokens_output = response.usage.output_tokens
            
            else:
                raise ValueError(f"unsupported provider: {provider}")
        
        except Exception as e:
            logger.error(f"llm call error: {e}")
            return StepOutput(
                action=None,
                next_state=None,
                raw_text=str(e),
                valid=False,
                red_flags=["llm_error"],
                tokens_input=0,
                tokens_output=0,
            )
        
        # parse response
        try:
            action, next_state = self.response_parser(raw_text)
            parsed_output = {"action": action, "next_state": next_state}
        except Exception as e:
            logger.debug(f"parse error: {e}")
            action = None
            next_state = None
            parsed_output = None
        
        # red-flag validation
        is_valid, red_flags = self.red_flagger.evaluate(
            raw_text=raw_text,
            parsed_output=parsed_output,
            step_input=step_input,
        )
        
        return StepOutput(
            action=action,
            next_state=next_state,
            raw_text=raw_text,
            valid=is_valid,
            red_flags=red_flags,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
        )

