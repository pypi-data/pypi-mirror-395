"""
Benchmark Suite

Standard benchmarks for evaluating LLMs:
- MMLU (knowledge/reasoning)
- GSM8K (math)
- HumanEval (coding)
- Custom benchmarks

Example:
    >>> from promptmachine_eval.benchmarks import MMLUBenchmark
    >>> 
    >>> mmlu = MMLUBenchmark(sample_size=100)
    >>> results = await mmlu.evaluate(["gpt-4o-mini"])
"""

from promptmachine_eval.benchmarks.base import (
    Benchmark,
    BenchmarkConfig,
    BenchmarkResult,
    BenchmarkQuestion,
)

__all__ = [
    "Benchmark",
    "BenchmarkConfig",
    "BenchmarkResult",
    "BenchmarkQuestion",
]

