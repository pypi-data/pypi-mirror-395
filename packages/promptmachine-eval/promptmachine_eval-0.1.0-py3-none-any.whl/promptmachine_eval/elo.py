"""
ELO Rating System

Implements ELO rating calculations for LLM arena battles.
Based on the original chess ELO system with extensions for
handling uncertainty (standard deviation) and batch updates.

The ELO system provides:
- Fair comparison between models of different strengths
- Convergent ratings after many games
- Intuitive win probability calculations

Mathematical foundation:
- Expected score: E_A = 1 / (1 + 10^((R_B - R_A) / 400))
- New rating: R'_A = R_A + K * (S_A - E_A)

Example:
    >>> elo = EloCalculator()
    >>> 
    >>> # Equal players, A wins
    >>> new_a, new_b = elo.update_ratings(1000, 1000, score_a=1.0)
    >>> print(f"A: {new_a:.0f}, B: {new_b:.0f}")
    A: 1016, B: 984
    
    >>> # Expected win probability
    >>> prob = elo.expected_score(1200, 1000)
    >>> print(f"1200-rated has {prob:.1%} win chance")
    1200-rated has 75.9% win chance
"""

from dataclasses import dataclass
from typing import Optional
import math
import random


@dataclass
class EloConfig:
    """
    Configuration for ELO calculations.
    
    Attributes:
        k_factor: Base K-factor for rating changes. Higher = more volatile.
            - 32: Standard (good for most cases)
            - 16: Conservative (for established ratings)
            - 64: Aggressive (for rapid initial calibration)
        initial_rating: Starting rating for new models.
        initial_sd: Initial standard deviation (uncertainty).
        min_sd: Minimum SD after many games.
        sd_decay_rate: How fast SD decreases per game (0.9 = 10% per game).
        scale_factor: Divisor in ELO formula (400 is standard).
    """
    
    k_factor: float = 32.0
    initial_rating: float = 1000.0
    initial_sd: float = 350.0
    min_sd: float = 100.0
    sd_decay_rate: float = 0.9
    scale_factor: float = 400.0


@dataclass
class EloUpdateResult:
    """
    Result of an ELO rating update after a battle.
    
    Attributes:
        new_rating_a: Updated rating for model A.
        new_rating_b: Updated rating for model B.
        rating_change_a: Points gained/lost by model A.
        rating_change_b: Points gained/lost by model B.
        expected_score_a: Pre-battle expected score for A (0-1).
        new_sd_a: Updated uncertainty for model A.
        new_sd_b: Updated uncertainty for model B.
    """
    
    new_rating_a: float
    new_rating_b: float
    rating_change_a: int
    rating_change_b: int
    expected_score_a: float
    new_sd_a: Optional[float] = None
    new_sd_b: Optional[float] = None


class EloCalculator:
    """
    Calculator for ELO ratings.
    
    Provides methods for:
    - Calculating expected scores between models
    - Updating ratings after battles
    - Estimating win probabilities with uncertainty
    - Managing rating confidence (standard deviation)
    
    Example:
        >>> calc = EloCalculator()
        >>> 
        >>> # Simple rating update
        >>> new_a, new_b = calc.update_ratings(1200, 1000, score_a=1.0)
        >>> 
        >>> # Full update with uncertainty
        >>> result = calc.update_after_battle(
        ...     rating_a=1200, rating_b=1000,
        ...     sd_a=150, sd_b=200,
        ...     score_a=1.0
        ... )
        >>> print(f"A: {result.new_rating_a:.0f} ({result.rating_change_a:+d})")
    """
    
    def __init__(self, config: Optional[EloConfig] = None) -> None:
        """
        Initialize calculator with configuration.
        
        Args:
            config: ELO configuration. Uses defaults if not provided.
        """
        self.config = config or EloConfig()
    
    def expected_score(self, rating_a: float, rating_b: float) -> float:
        """
        Calculate expected score for model A against model B.
        
        The expected score represents the probability of winning
        plus half the probability of drawing.
        
        Formula: E_A = 1 / (1 + 10^((R_B - R_A) / 400))
        
        Args:
            rating_a: ELO rating of model A.
            rating_b: ELO rating of model B.
            
        Returns:
            Expected score between 0 and 1.
            - 0.5 = equal strength
            - > 0.5 = A is favored
            - < 0.5 = B is favored
            
        Example:
            >>> calc = EloCalculator()
            >>> calc.expected_score(1200, 1000)
            0.759...
            >>> calc.expected_score(1000, 1000)
            0.5
        """
        exponent = (rating_b - rating_a) / self.config.scale_factor
        return 1.0 / (1.0 + math.pow(10, exponent))
    
    def update_ratings(
        self,
        rating_a: float,
        rating_b: float,
        score_a: float,
        k_factor: Optional[float] = None,
    ) -> tuple[float, float]:
        """
        Update ratings for two models after a battle.
        
        Args:
            rating_a: Current rating of model A.
            rating_b: Current rating of model B.
            score_a: Actual score for model A.
                - 1.0 = A wins
                - 0.5 = Draw
                - 0.0 = A loses (B wins)
            k_factor: Optional K-factor override.
            
        Returns:
            Tuple of (new_rating_a, new_rating_b).
            
        Example:
            >>> calc = EloCalculator()
            >>> # Upset win: lower-rated beats higher-rated
            >>> new_a, new_b = calc.update_ratings(1000, 1200, score_a=1.0)
            >>> print(f"Underdog gained: {new_a - 1000:.0f} points")
        """
        k = k_factor if k_factor is not None else self.config.k_factor
        
        expected_a = self.expected_score(rating_a, rating_b)
        expected_b = 1.0 - expected_a
        score_b = 1.0 - score_a
        
        new_rating_a = rating_a + k * (score_a - expected_a)
        new_rating_b = rating_b + k * (score_b - expected_b)
        
        return new_rating_a, new_rating_b
    
    def update_sd(self, current_sd: float) -> float:
        """
        Update standard deviation after a battle.
        
        SD decreases with each game, representing increased
        confidence in the rating estimate.
        
        Args:
            current_sd: Current standard deviation.
            
        Returns:
            New SD (never below min_sd).
        """
        new_sd = current_sd * self.config.sd_decay_rate
        return max(new_sd, self.config.min_sd)
    
    def update_after_battle(
        self,
        rating_a: float,
        rating_b: float,
        sd_a: float,
        sd_b: float,
        score_a: float,
        k_factor: Optional[float] = None,
    ) -> EloUpdateResult:
        """
        Full update after a battle including uncertainty.
        
        This is the recommended method for production use.
        Applies adaptive K-factor based on uncertainty and
        updates both ratings and standard deviations.
        
        Args:
            rating_a: Current rating of model A.
            rating_b: Current rating of model B.
            sd_a: Standard deviation (uncertainty) for A.
            sd_b: Standard deviation (uncertainty) for B.
            score_a: Score for A (1.0=win, 0.5=draw, 0.0=loss).
            k_factor: Optional K-factor override.
            
        Returns:
            EloUpdateResult with all updated values.
            
        Example:
            >>> calc = EloCalculator()
            >>> result = calc.update_after_battle(
            ...     rating_a=1200, rating_b=1000,
            ...     sd_a=100, sd_b=250,  # B is more uncertain
            ...     score_a=0.0  # B wins upset
            ... )
            >>> print(f"B gained {-result.rating_change_b} points")
        """
        # Adaptive K-factor: higher uncertainty = bigger updates
        k = k_factor if k_factor is not None else self.config.k_factor
        avg_sd = (sd_a + sd_b) / 2
        uncertainty_factor = avg_sd / self.config.initial_sd
        effective_k = k * uncertainty_factor
        
        expected_a = self.expected_score(rating_a, rating_b)
        new_rating_a, new_rating_b = self.update_ratings(
            rating_a, rating_b, score_a, effective_k
        )
        
        new_sd_a = self.update_sd(sd_a)
        new_sd_b = self.update_sd(sd_b)
        
        return EloUpdateResult(
            new_rating_a=new_rating_a,
            new_rating_b=new_rating_b,
            rating_change_a=round(new_rating_a - rating_a),
            rating_change_b=round(new_rating_b - rating_b),
            expected_score_a=expected_a,
            new_sd_a=new_sd_a,
            new_sd_b=new_sd_b,
        )
    
    def win_probability(
        self,
        rating_a: float,
        rating_b: float,
        sd_a: float = 0.0,
        sd_b: float = 0.0,
        num_simulations: int = 10000,
    ) -> float:
        """
        Estimate win probability using Monte Carlo simulation.
        
        When uncertainty (SD) is provided, simulates many games
        by sampling from rating distributions.
        
        Args:
            rating_a: Rating of model A.
            rating_b: Rating of model B.
            sd_a: Uncertainty for A (0 = point estimate).
            sd_b: Uncertainty for B (0 = point estimate).
            num_simulations: Number of Monte Carlo samples.
            
        Returns:
            Probability that A wins (0.0 to 1.0).
            
        Example:
            >>> calc = EloCalculator()
            >>> # Point estimate (no uncertainty)
            >>> p = calc.win_probability(1200, 1000)
            >>> print(f"{p:.1%}")  # ~76%
            >>> 
            >>> # With uncertainty - less confident
            >>> p = calc.win_probability(1200, 1000, sd_a=100, sd_b=300)
            >>> print(f"{p:.1%}")  # Closer to 50% due to B's uncertainty
        """
        if sd_a == 0 and sd_b == 0:
            return self.expected_score(rating_a, rating_b)
        
        wins_a = 0
        for _ in range(num_simulations):
            sampled_a = random.gauss(rating_a, sd_a) if sd_a > 0 else rating_a
            sampled_b = random.gauss(rating_b, sd_b) if sd_b > 0 else rating_b
            
            p_a_wins = self.expected_score(sampled_a, sampled_b)
            if random.random() < p_a_wins:
                wins_a += 1
        
        return wins_a / num_simulations
    
    def confidence_interval(
        self,
        rating: float,
        sd: float,
        confidence: float = 0.95,
    ) -> tuple[float, float]:
        """
        Calculate confidence interval for a rating.
        
        Args:
            rating: Point estimate rating.
            sd: Standard deviation.
            confidence: Confidence level (default 95%).
            
        Returns:
            Tuple of (lower_bound, upper_bound).
            
        Example:
            >>> calc = EloCalculator()
            >>> low, high = calc.confidence_interval(1200, 100, 0.95)
            >>> print(f"95% CI: [{low:.0f}, {high:.0f}]")
            95% CI: [1004, 1396]
        """
        # Z-score for confidence level (approximation)
        z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_scores.get(confidence, 1.96)
        
        margin = z * sd
        return rating - margin, rating + margin
    
    def rating_to_percentile(
        self,
        rating: float,
        population_ratings: list[float],
    ) -> float:
        """
        Calculate percentile rank within a population.
        
        Args:
            rating: Rating to evaluate.
            population_ratings: All ratings in population.
            
        Returns:
            Percentile (0-100).
        """
        if not population_ratings:
            return 50.0
        
        count_below = sum(1 for r in population_ratings if r < rating)
        return (count_below / len(population_ratings)) * 100

