"""
Base Benchmark Classes

Abstract base classes and common types for benchmarks.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Any
from datetime import datetime


@dataclass
class BenchmarkConfig:
    """
    Configuration for a benchmark run.
    
    Attributes:
        sample_size: Number of questions to evaluate.
        max_tokens: Max output tokens per question.
        temperature: Generation temperature.
        timeout_seconds: Timeout per question.
        retry_attempts: Number of retries on failure.
    """
    
    sample_size: int = 100
    max_tokens: int = 256
    temperature: float = 0.0
    timeout_seconds: int = 60
    retry_attempts: int = 3


@dataclass
class BenchmarkQuestion:
    """
    A single benchmark question.
    
    Attributes:
        id: Unique question ID.
        prompt: The question/prompt text.
        correct_answer: Expected answer.
        category: Question category (e.g., "math", "science").
        difficulty: Optional difficulty level.
        metadata: Additional question data.
    """
    
    id: str
    prompt: str
    correct_answer: str
    category: str = "general"
    difficulty: Optional[str] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class QuestionResult:
    """
    Result for a single question.
    
    Attributes:
        question_id: Question ID.
        model_answer: Model's response.
        is_correct: Whether the answer was correct.
        latency_ms: Response time.
        tokens_used: Tokens consumed.
    """
    
    question_id: str
    model_answer: str
    is_correct: bool
    latency_ms: int
    tokens_used: int


@dataclass
class BenchmarkResult:
    """
    Complete benchmark result for a model.
    
    Attributes:
        benchmark_name: Name of the benchmark.
        model: Model evaluated.
        score: Overall score (0-100).
        total_questions: Number of questions.
        correct_count: Number correct.
        category_scores: Scores by category.
        question_results: Individual question results.
        total_cost: Estimated cost.
        total_latency_ms: Total response time.
        evaluated_at: Timestamp.
    """
    
    benchmark_name: str
    model: str
    score: float
    total_questions: int
    correct_count: int
    category_scores: dict[str, float] = field(default_factory=dict)
    question_results: list[QuestionResult] = field(default_factory=list)
    total_cost: float = 0.0
    total_latency_ms: int = 0
    evaluated_at: datetime = field(default_factory=datetime.utcnow)


class Benchmark(ABC):
    """
    Abstract base class for benchmarks.
    
    Subclasses must implement:
    - load_questions(): Load benchmark dataset
    - evaluate_answer(): Check if answer is correct
    
    Example:
        >>> class MyBenchmark(Benchmark):
        ...     def load_questions(self):
        ...         return [BenchmarkQuestion(...), ...]
        ...     
        ...     def evaluate_answer(self, question, answer):
        ...         return answer.strip() == question.correct_answer
    """
    
    name: str = "base"
    description: str = ""
    
    def __init__(self, config: Optional[BenchmarkConfig] = None) -> None:
        """Initialize benchmark with config."""
        self.config = config or BenchmarkConfig()
        self._questions: list[BenchmarkQuestion] = []
    
    @abstractmethod
    def load_questions(self) -> list[BenchmarkQuestion]:
        """
        Load benchmark questions.
        
        Returns:
            List of BenchmarkQuestion objects.
        """
        pass
    
    @abstractmethod
    def evaluate_answer(
        self,
        question: BenchmarkQuestion,
        model_answer: str,
    ) -> bool:
        """
        Evaluate if a model answer is correct.
        
        Args:
            question: The question asked.
            model_answer: The model's response.
            
        Returns:
            True if correct, False otherwise.
        """
        pass
    
    def format_prompt(self, question: BenchmarkQuestion) -> str:
        """
        Format question into a prompt.
        
        Can be overridden for benchmark-specific formatting.
        
        Args:
            question: Question to format.
            
        Returns:
            Formatted prompt string.
        """
        return question.prompt
    
    def get_questions(self) -> list[BenchmarkQuestion]:
        """Get loaded questions, loading if needed."""
        if not self._questions:
            self._questions = self.load_questions()
        
        # Sample if needed
        if len(self._questions) > self.config.sample_size:
            import random
            return random.sample(self._questions, self.config.sample_size)
        
        return self._questions
    
    async def evaluate(
        self,
        models: list[str],
        api_keys: dict[str, str],
    ) -> dict[str, BenchmarkResult]:
        """
        Run benchmark evaluation for multiple models.
        
        Args:
            models: List of model names to evaluate.
            api_keys: Dict mapping provider to API key.
            
        Returns:
            Dict mapping model name to BenchmarkResult.
        """
        from promptmachine_eval.runner import PromptTester
        import time
        
        tester = PromptTester(
            openai_api_key=api_keys.get("openai"),
            anthropic_api_key=api_keys.get("anthropic"),
            openrouter_api_key=api_keys.get("openrouter"),
        )
        
        questions = self.get_questions()
        results: dict[str, BenchmarkResult] = {}
        
        for model in models:
            question_results: list[QuestionResult] = []
            category_correct: dict[str, int] = {}
            category_total: dict[str, int] = {}
            
            for question in questions:
                prompt = self.format_prompt(question)
                
                start = time.perf_counter()
                test_result = await tester.test_one(
                    prompt=prompt,
                    model=model,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                )
                latency = int((time.perf_counter() - start) * 1000)
                
                is_correct = False
                if not test_result.error:
                    is_correct = self.evaluate_answer(question, test_result.response)
                
                question_results.append(QuestionResult(
                    question_id=question.id,
                    model_answer=test_result.response,
                    is_correct=is_correct,
                    latency_ms=latency,
                    tokens_used=test_result.tokens_total,
                ))
                
                # Track category stats
                cat = question.category
                category_total[cat] = category_total.get(cat, 0) + 1
                if is_correct:
                    category_correct[cat] = category_correct.get(cat, 0) + 1
            
            # Calculate scores
            correct = sum(1 for qr in question_results if qr.is_correct)
            score = (correct / len(questions)) * 100 if questions else 0
            
            category_scores = {
                cat: (category_correct.get(cat, 0) / total) * 100
                for cat, total in category_total.items()
            }
            
            results[model] = BenchmarkResult(
                benchmark_name=self.name,
                model=model,
                score=score,
                total_questions=len(questions),
                correct_count=correct,
                category_scores=category_scores,
                question_results=question_results,
                total_cost=sum(tester.cost_tracker._usage_log[-len(questions):]),
                total_latency_ms=sum(qr.latency_ms for qr in question_results),
            )
        
        return results

