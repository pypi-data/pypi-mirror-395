"""
Arena Battle Runner

Run head-to-head LLM comparisons with LLM-as-judge evaluation.
Supports blind battles where model identities are hidden.

Example:
    >>> runner = BattleRunner(openai_api_key="sk-...")
    >>> result = await runner.battle(
    ...     "Write a haiku about Python",
    ...     model_a="gpt-4o",
    ...     model_b="gpt-4o-mini",
    ...     judge_model="gpt-4o-mini"
    ... )
    >>> print(f"Winner: {result.winner}")
    >>> print(f"Reasoning: {result.judgement.reasoning}")
"""

from dataclasses import dataclass, field
from typing import Optional, Any, Literal
from datetime import datetime
import asyncio
import random

from promptmachine_eval.runner import PromptTester, TestResult
from promptmachine_eval.elo import EloCalculator, EloConfig, EloUpdateResult
from promptmachine_eval.cost import CostTracker


@dataclass
class Judgement:
    """
    Judgement from LLM-as-judge or human evaluator.
    
    Attributes:
        winner: "A", "B", or "draw".
        reasoning: Explanation for the decision.
        criteria_scores: Optional breakdown by criteria.
        confidence: Judge's confidence (0-1).
        judge_model: Model used as judge (if LLM).
    """
    
    winner: Literal["A", "B", "draw"]
    reasoning: str
    criteria_scores: dict[str, dict[str, float]] = field(default_factory=dict)
    confidence: float = 0.0
    judge_model: Optional[str] = None


@dataclass
class BattleResult:
    """
    Complete result of a head-to-head battle.
    
    Attributes:
        battle_id: Unique battle identifier.
        prompt: The prompt used for the battle.
        model_a: First model name.
        model_b: Second model name.
        response_a: Response from model A.
        response_b: Response from model B.
        winner: Winning model name, or "draw".
        judgement: Full judgement details.
        elo_update: Optional ELO rating changes.
        result_a: Full test result for model A.
        result_b: Full test result for model B.
        total_cost: Total cost of battle (both responses + judge).
        created_at: When battle was conducted.
    """
    
    battle_id: str
    prompt: str
    model_a: str
    model_b: str
    response_a: str
    response_b: str
    winner: str
    judgement: Judgement
    elo_update: Optional[EloUpdateResult] = None
    result_a: Optional[TestResult] = None
    result_b: Optional[TestResult] = None
    total_cost: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)


# Default judge prompt template
DEFAULT_JUDGE_PROMPT = """You are an impartial judge evaluating two AI responses.

**Evaluation Task:**
Compare Response A and Response B to the given prompt. Consider:
1. **Accuracy** - Is the information correct?
2. **Relevance** - Does it address the prompt?
3. **Clarity** - Is it well-written and easy to understand?
4. **Completeness** - Does it fully answer the question?
5. **Helpfulness** - Would a user find this useful?

**Prompt:**
{prompt}

**Response A:**
{response_a}

**Response B:**
{response_b}

**Instructions:**
- Evaluate both responses fairly
- Declare a winner: "A", "B", or "draw" (if truly equal)
- Explain your reasoning in 2-3 sentences
- Be objective - don't favor longer responses automatically

**Your verdict:**
Winner: [A/B/draw]
Reasoning: [Your explanation]"""


class BattleRunner:
    """
    Run arena-style battles between LLMs.
    
    Features:
    - Blind comparisons (randomized ordering)
    - LLM-as-judge evaluation
    - Position bias mitigation
    - ELO rating integration
    - Cost tracking
    
    Example:
        >>> runner = BattleRunner(
        ...     openai_api_key="sk-...",
        ...     anthropic_api_key="sk-ant-...",
        ... )
        >>> 
        >>> # Simple battle
        >>> result = await runner.battle(
        ...     "Explain quantum computing",
        ...     model_a="gpt-4o",
        ...     model_b="claude-3-5-sonnet"
        ... )
        >>> print(f"Winner: {result.winner}")
        >>> 
        >>> # Battle with custom judge
        >>> result = await runner.battle(
        ...     "Write a poem",
        ...     model_a="gpt-4o-mini",
        ...     model_b="claude-3-5-haiku",
        ...     judge_model="gpt-4o",  # Use stronger model as judge
        ...     system_prompt="Be creative and poetic."
        ... )
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        openrouter_api_key: Optional[str] = None,
        elo_config: Optional[EloConfig] = None,
        default_judge_model: str = "gpt-4o-mini",
        judge_prompt_template: str = DEFAULT_JUDGE_PROMPT,
    ) -> None:
        """
        Initialize battle runner.
        
        Args:
            openai_api_key: OpenAI API key.
            anthropic_api_key: Anthropic API key.
            openrouter_api_key: OpenRouter API key.
            elo_config: ELO calculator configuration.
            default_judge_model: Default model for judging.
            judge_prompt_template: Template for judge prompt.
        """
        self.tester = PromptTester(
            openai_api_key=openai_api_key,
            anthropic_api_key=anthropic_api_key,
            openrouter_api_key=openrouter_api_key,
        )
        self.elo = EloCalculator(elo_config)
        self.cost_tracker = CostTracker()
        self.default_judge_model = default_judge_model
        self.judge_prompt_template = judge_prompt_template
        
        self._battle_count = 0
    
    def _generate_battle_id(self) -> str:
        """Generate unique battle ID."""
        self._battle_count += 1
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"battle_{timestamp}_{self._battle_count:04d}"
    
    def _parse_judgement(
        self,
        judge_response: str,
        judge_model: str,
    ) -> Judgement:
        """
        Parse judge response into Judgement object.
        
        Args:
            judge_response: Raw response from judge model.
            judge_model: Model used as judge.
            
        Returns:
            Parsed Judgement.
        """
        response_lower = judge_response.lower()
        
        # Determine winner from response
        if "winner: a" in response_lower or "winner:a" in response_lower:
            winner: Literal["A", "B", "draw"] = "A"
        elif "winner: b" in response_lower or "winner:b" in response_lower:
            winner = "B"
        elif "winner: draw" in response_lower or "it's a draw" in response_lower:
            winner = "draw"
        else:
            # Fallback: look for mentions
            a_mentions = response_lower.count("response a") + response_lower.count("a is")
            b_mentions = response_lower.count("response b") + response_lower.count("b is")
            if a_mentions > b_mentions:
                winner = "A"
            elif b_mentions > a_mentions:
                winner = "B"
            else:
                winner = "draw"
        
        # Extract reasoning (everything after "Reasoning:")
        reasoning = judge_response
        if "reasoning:" in response_lower:
            idx = response_lower.index("reasoning:")
            reasoning = judge_response[idx + 10:].strip()
        
        return Judgement(
            winner=winner,
            reasoning=reasoning,
            judge_model=judge_model,
        )
    
    async def battle(
        self,
        prompt: str,
        model_a: str,
        model_b: str,
        judge_model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        randomize_order: bool = True,
        rating_a: Optional[float] = None,
        rating_b: Optional[float] = None,
        sd_a: float = 350.0,
        sd_b: float = 350.0,
    ) -> BattleResult:
        """
        Run a battle between two models.
        
        Args:
            prompt: The prompt for both models.
            model_a: First model.
            model_b: Second model.
            judge_model: Model to use as judge (default: gpt-4o-mini).
            system_prompt: Optional system prompt for contestants.
            temperature: Generation temperature.
            max_tokens: Max output tokens for contestants.
            randomize_order: Shuffle A/B when presenting to judge.
            rating_a: Optional current ELO rating for model A.
            rating_b: Optional current ELO rating for model B.
            sd_a: Standard deviation for model A.
            sd_b: Standard deviation for model B.
            
        Returns:
            BattleResult with winner and details.
        """
        battle_id = self._generate_battle_id()
        judge = judge_model or self.default_judge_model
        
        # Get responses from both models in parallel
        results = await self.tester.test(
            prompt=prompt,
            models=[model_a, model_b],
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            parallel=True,
        )
        
        result_a = results[0]
        result_b = results[1]
        
        # Handle errors
        if result_a.error and result_b.error:
            return BattleResult(
                battle_id=battle_id,
                prompt=prompt,
                model_a=model_a,
                model_b=model_b,
                response_a="ERROR: " + (result_a.error or ""),
                response_b="ERROR: " + (result_b.error or ""),
                winner="draw",
                judgement=Judgement(
                    winner="draw",
                    reasoning="Both models failed to respond.",
                ),
                result_a=result_a,
                result_b=result_b,
                total_cost=result_a.cost + result_b.cost,
            )
        elif result_a.error:
            return BattleResult(
                battle_id=battle_id,
                prompt=prompt,
                model_a=model_a,
                model_b=model_b,
                response_a="ERROR: " + (result_a.error or ""),
                response_b=result_b.response,
                winner=model_b,
                judgement=Judgement(
                    winner="B",
                    reasoning=f"Model A ({model_a}) failed to respond.",
                ),
                result_a=result_a,
                result_b=result_b,
                total_cost=result_a.cost + result_b.cost,
            )
        elif result_b.error:
            return BattleResult(
                battle_id=battle_id,
                prompt=prompt,
                model_a=model_a,
                model_b=model_b,
                response_a=result_a.response,
                response_b="ERROR: " + (result_b.error or ""),
                winner=model_a,
                judgement=Judgement(
                    winner="A",
                    reasoning=f"Model B ({model_b}) failed to respond.",
                ),
                result_a=result_a,
                result_b=result_b,
                total_cost=result_a.cost + result_b.cost,
            )
        
        # Optionally randomize order to prevent position bias
        if randomize_order and random.random() < 0.5:
            displayed_a, displayed_b = result_b.response, result_a.response
            swapped = True
        else:
            displayed_a, displayed_b = result_a.response, result_b.response
            swapped = False
        
        # Build judge prompt
        judge_prompt = self.judge_prompt_template.format(
            prompt=prompt,
            response_a=displayed_a,
            response_b=displayed_b,
        )
        
        # Get judgement
        judge_result = await self.tester.test_one(
            prompt=judge_prompt,
            model=judge,
            temperature=0.0,  # Deterministic judge
            max_tokens=512,
        )
        
        judgement = self._parse_judgement(judge_result.response, judge)
        
        # Account for swapped positions
        if swapped:
            if judgement.winner == "A":
                judgement.winner = "B"
            elif judgement.winner == "B":
                judgement.winner = "A"
        
        # Determine winning model
        if judgement.winner == "A":
            winner = model_a
            score_a = 1.0
        elif judgement.winner == "B":
            winner = model_b
            score_a = 0.0
        else:
            winner = "draw"
            score_a = 0.5
        
        # Calculate ELO update if ratings provided
        elo_update = None
        if rating_a is not None and rating_b is not None:
            elo_update = self.elo.update_after_battle(
                rating_a=rating_a,
                rating_b=rating_b,
                sd_a=sd_a,
                sd_b=sd_b,
                score_a=score_a,
            )
        
        total_cost = result_a.cost + result_b.cost + judge_result.cost
        
        return BattleResult(
            battle_id=battle_id,
            prompt=prompt,
            model_a=model_a,
            model_b=model_b,
            response_a=result_a.response,
            response_b=result_b.response,
            winner=winner,
            judgement=judgement,
            elo_update=elo_update,
            result_a=result_a,
            result_b=result_b,
            total_cost=total_cost,
        )
    
    async def run_tournament(
        self,
        prompt: str,
        models: list[str],
        judge_model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        rounds_per_pair: int = 1,
    ) -> list[BattleResult]:
        """
        Run a round-robin tournament between models.
        
        Args:
            prompt: Prompt for all battles.
            models: List of models to compete.
            judge_model: Judge model to use.
            system_prompt: System prompt for contestants.
            rounds_per_pair: Battles per pair (for variance).
            
        Returns:
            List of all battle results.
        """
        results: list[BattleResult] = []
        
        # Generate all pairs
        pairs = []
        for i, model_a in enumerate(models):
            for model_b in models[i + 1:]:
                for _ in range(rounds_per_pair):
                    pairs.append((model_a, model_b))
        
        # Run all battles
        for model_a, model_b in pairs:
            result = await self.battle(
                prompt=prompt,
                model_a=model_a,
                model_b=model_b,
                judge_model=judge_model,
                system_prompt=system_prompt,
            )
            results.append(result)
        
        return results
    
    def calculate_standings(
        self,
        results: list[BattleResult],
    ) -> dict[str, dict]:
        """
        Calculate tournament standings from results.
        
        Args:
            results: List of battle results.
            
        Returns:
            Dict mapping model names to their stats.
        """
        standings: dict[str, dict] = {}
        
        for result in results:
            for model in [result.model_a, result.model_b]:
                if model not in standings:
                    standings[model] = {
                        "wins": 0,
                        "losses": 0,
                        "draws": 0,
                        "battles": 0,
                    }
            
            standings[result.model_a]["battles"] += 1
            standings[result.model_b]["battles"] += 1
            
            if result.winner == result.model_a:
                standings[result.model_a]["wins"] += 1
                standings[result.model_b]["losses"] += 1
            elif result.winner == result.model_b:
                standings[result.model_b]["wins"] += 1
                standings[result.model_a]["losses"] += 1
            else:  # draw
                standings[result.model_a]["draws"] += 1
                standings[result.model_b]["draws"] += 1
        
        # Calculate win rate
        for model, stats in standings.items():
            if stats["battles"] > 0:
                stats["win_rate"] = (stats["wins"] + 0.5 * stats["draws"]) / stats["battles"]
            else:
                stats["win_rate"] = 0.0
        
        return standings

