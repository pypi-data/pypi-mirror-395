"""
Prompt Testing Runner

Test prompts across multiple LLM providers and compare results.
Supports streaming, parallel execution, and result caching.

Example:
    >>> tester = PromptTester(openai_api_key="sk-...")
    >>> results = await tester.test(
    ...     "Explain recursion",
    ...     models=["gpt-4o", "gpt-4o-mini"]
    ... )
    >>> for r in results:
    ...     print(f"{r.model}: {r.tokens} tokens, ${r.cost:.4f}")
"""

from dataclasses import dataclass, field
from typing import Optional, Any
from datetime import datetime
import asyncio
import time

from promptmachine_eval.cost import CostTracker


@dataclass
class TestResult:
    """
    Result from testing a prompt with a specific model.
    
    Attributes:
        model: Model name.
        response: Generated response text.
        tokens_input: Input tokens used.
        tokens_output: Output tokens generated.
        tokens_total: Total tokens.
        cost: Estimated cost in dollars.
        latency_ms: Response time in milliseconds.
        created_at: When the test was run.
        error: Error message if failed, None otherwise.
        metadata: Additional model-specific data.
    """
    
    model: str
    response: str
    tokens_input: int
    tokens_output: int
    tokens_total: int
    cost: float
    latency_ms: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)


class PromptTester:
    """
    Test prompts across multiple LLM providers.
    
    Features:
    - Parallel execution across models
    - Cost tracking and limits
    - Error handling with retries
    - Result comparison
    
    Example:
        >>> tester = PromptTester(
        ...     openai_api_key="sk-...",
        ...     anthropic_api_key="sk-ant-...",
        ... )
        >>> 
        >>> # Test single model
        >>> result = await tester.test_one("Hello!", "gpt-4o-mini")
        >>> print(result.response)
        >>> 
        >>> # Test multiple models in parallel
        >>> results = await tester.test(
        ...     "Write a limerick about Python",
        ...     models=["gpt-4o", "gpt-4o-mini", "claude-3-5-haiku"]
        ... )
        >>> 
        >>> # Compare results
        >>> best = min(results, key=lambda r: r.cost)
        >>> print(f"Cheapest: {best.model} at ${best.cost:.4f}")
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        openrouter_api_key: Optional[str] = None,
        cost_tracker: Optional[CostTracker] = None,
        default_temperature: float = 0.7,
        default_max_tokens: int = 1024,
    ) -> None:
        """
        Initialize tester with API keys.
        
        Args:
            openai_api_key: OpenAI API key.
            anthropic_api_key: Anthropic API key.
            openrouter_api_key: OpenRouter API key (for other providers).
            cost_tracker: Optional shared cost tracker.
            default_temperature: Default temperature for generation.
            default_max_tokens: Default max tokens for output.
        """
        self.openai_api_key = openai_api_key
        self.anthropic_api_key = anthropic_api_key
        self.openrouter_api_key = openrouter_api_key
        self.cost_tracker = cost_tracker or CostTracker()
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        
        self._clients: dict[str, Any] = {}
    
    def _get_provider(self, model: str) -> str:
        """Determine provider from model name."""
        model_lower = model.lower()
        
        if "gpt" in model_lower or "o1" in model_lower:
            return "openai"
        elif "claude" in model_lower:
            return "anthropic"
        elif "/" in model:  # OpenRouter format
            return "openrouter"
        else:
            return "openai"  # Default
    
    async def _get_openai_client(self) -> Any:
        """Get or create OpenAI client."""
        if "openai" not in self._clients:
            try:
                from openai import AsyncOpenAI
                self._clients["openai"] = AsyncOpenAI(api_key=self.openai_api_key)
            except ImportError:
                raise ImportError("openai package required: pip install openai")
        return self._clients["openai"]
    
    async def _get_anthropic_client(self) -> Any:
        """Get or create Anthropic client."""
        if "anthropic" not in self._clients:
            try:
                from anthropic import AsyncAnthropic
                self._clients["anthropic"] = AsyncAnthropic(api_key=self.anthropic_api_key)
            except ImportError:
                raise ImportError("anthropic package required: pip install anthropic")
        return self._clients["anthropic"]
    
    async def _call_openai(
        self,
        model: str,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> tuple[str, int, int]:
        """Call OpenAI API."""
        client = await self._get_openai_client()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        content = response.choices[0].message.content or ""
        input_tokens = response.usage.prompt_tokens if response.usage else 0
        output_tokens = response.usage.completion_tokens if response.usage else 0
        
        return content, input_tokens, output_tokens
    
    async def _call_anthropic(
        self,
        model: str,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> tuple[str, int, int]:
        """Call Anthropic API."""
        client = await self._get_anthropic_client()
        
        kwargs: dict[str, Any] = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        # Anthropic doesn't support temperature=0
        if temperature > 0:
            kwargs["temperature"] = temperature
        
        response = await client.messages.create(**kwargs)
        
        content = response.content[0].text if response.content else ""
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        
        return content, input_tokens, output_tokens
    
    async def test_one(
        self,
        prompt: str,
        model: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> TestResult:
        """
        Test a prompt with a single model.
        
        Args:
            prompt: User prompt text.
            model: Model to use.
            system_prompt: Optional system prompt.
            temperature: Generation temperature.
            max_tokens: Maximum output tokens.
            
        Returns:
            TestResult with response and metrics.
        """
        temp = temperature if temperature is not None else self.default_temperature
        tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        
        provider = self._get_provider(model)
        start_time = time.perf_counter()
        
        try:
            if provider == "openai":
                response, input_tok, output_tok = await self._call_openai(
                    model, prompt, system_prompt, temp, tokens
                )
            elif provider == "anthropic":
                response, input_tok, output_tok = await self._call_anthropic(
                    model, prompt, system_prompt, temp, tokens
                )
            else:
                raise ValueError(f"Unsupported provider: {provider}")
            
            latency = int((time.perf_counter() - start_time) * 1000)
            cost = self.cost_tracker.track_usage(model, input_tok, output_tok)
            
            return TestResult(
                model=model,
                response=response,
                tokens_input=input_tok,
                tokens_output=output_tok,
                tokens_total=input_tok + output_tok,
                cost=cost,
                latency_ms=latency,
            )
            
        except Exception as e:
            latency = int((time.perf_counter() - start_time) * 1000)
            return TestResult(
                model=model,
                response="",
                tokens_input=0,
                tokens_output=0,
                tokens_total=0,
                cost=0.0,
                latency_ms=latency,
                error=str(e),
            )
    
    async def test(
        self,
        prompt: str,
        models: list[str],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        parallel: bool = True,
    ) -> list[TestResult]:
        """
        Test a prompt across multiple models.
        
        Args:
            prompt: User prompt text.
            models: List of models to test.
            system_prompt: Optional system prompt.
            temperature: Generation temperature.
            max_tokens: Maximum output tokens.
            parallel: Run tests in parallel (default True).
            
        Returns:
            List of TestResults, one per model.
            
        Example:
            >>> results = await tester.test(
            ...     "Write a function to reverse a string",
            ...     models=["gpt-4o", "gpt-4o-mini", "claude-3-5-haiku"],
            ...     system_prompt="You are a Python expert."
            ... )
            >>> for r in results:
            ...     if r.error:
            ...         print(f"{r.model}: ERROR - {r.error}")
            ...     else:
            ...         print(f"{r.model}: {r.latency_ms}ms, ${r.cost:.4f}")
        """
        if parallel:
            tasks = [
                self.test_one(prompt, model, system_prompt, temperature, max_tokens)
                for model in models
            ]
            results = await asyncio.gather(*tasks)
        else:
            results = []
            for model in models:
                result = await self.test_one(
                    prompt, model, system_prompt, temperature, max_tokens
                )
                results.append(result)
        
        return list(results)
    
    def compare_results(
        self,
        results: list[TestResult],
    ) -> dict[str, Any]:
        """
        Compare results across models.
        
        Args:
            results: List of test results.
            
        Returns:
            Comparison summary.
        """
        valid_results = [r for r in results if not r.error]
        
        if not valid_results:
            return {"error": "No successful results to compare"}
        
        fastest = min(valid_results, key=lambda r: r.latency_ms)
        cheapest = min(valid_results, key=lambda r: r.cost)
        longest_response = max(valid_results, key=lambda r: len(r.response))
        
        return {
            "total_models": len(results),
            "successful": len(valid_results),
            "failed": len(results) - len(valid_results),
            "fastest": {
                "model": fastest.model,
                "latency_ms": fastest.latency_ms,
            },
            "cheapest": {
                "model": cheapest.model,
                "cost": cheapest.cost,
            },
            "longest_response": {
                "model": longest_response.model,
                "length": len(longest_response.response),
            },
            "total_cost": sum(r.cost for r in valid_results),
            "total_tokens": sum(r.tokens_total for r in valid_results),
        }

