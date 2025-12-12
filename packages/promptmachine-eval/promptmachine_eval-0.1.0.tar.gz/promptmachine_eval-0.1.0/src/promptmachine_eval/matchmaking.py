"""
Matchmaking Service

Implements Monte Carlo matchmaking for LLM arena battles.
Selects optimal pairings based on:
- Rating similarity (competitive matches)
- Uncertainty (prioritize models needing more data)
- Exploration (random component to avoid local optima)

The goal is to create informative matches that efficiently
improve our confidence in model rankings.

Example:
    >>> service = MatchmakingService()
    >>> models = [
    ...     ModelInfo(id="gpt4o", rating=1200, sd=100),
    ...     ModelInfo(id="claude", rating=1180, sd=120),
    ...     ModelInfo(id="gemini", rating=1100, sd=200),
    ... ]
    >>> model_a, model_b = service.select_pair_for_battle(models)
    >>> print(f"Next battle: {model_a.id} vs {model_b.id}")
"""

from dataclasses import dataclass
from typing import Optional
import random
import math


@dataclass
class MatchmakingConfig:
    """
    Configuration for matchmaking algorithm.
    
    Attributes:
        competitiveness_weight: Importance of close matches (0-1).
        uncertainty_weight: Importance of high-uncertainty models (0-1).
        exploration_weight: Random exploration factor (0-1).
            Note: These should sum to 1.0
        num_simulations: Monte Carlo simulations per pairing.
        default_rating: Starting rating for new models.
        default_sd: Starting uncertainty for new models.
    """
    
    competitiveness_weight: float = 0.6
    uncertainty_weight: float = 0.3
    exploration_weight: float = 0.1
    num_simulations: int = 1000
    default_rating: float = 1000.0
    default_sd: float = 350.0


@dataclass
class ModelInfo:
    """
    Model information for matchmaking.
    
    Attributes:
        id: Unique model identifier.
        rating: Current ELO rating.
        sd: Standard deviation (uncertainty).
        battles_count: Total battles participated.
        display_name: Human-readable name (optional).
    """
    
    id: str
    rating: float
    sd: float
    battles_count: int = 0
    display_name: str = ""


@dataclass 
class MatchScore:
    """
    Score for a potential match pairing.
    
    Attributes:
        model_a: First model.
        model_b: Second model.
        total_score: Combined match value (higher = better match).
        competitiveness_score: How close the match would be.
        uncertainty_score: Information gain from uncertainty.
        exploration_score: Random exploration component.
    """
    
    model_a: ModelInfo
    model_b: ModelInfo
    total_score: float
    competitiveness_score: float
    uncertainty_score: float
    exploration_score: float


class MatchmakingService:
    """
    Service for selecting optimal arena battle pairings.
    
    Uses multi-factor scoring to select matches that are:
    1. Competitive - close in expected outcome
    2. Informative - involve uncertain models
    3. Diverse - some randomness to explore
    
    Example:
        >>> service = MatchmakingService()
        >>> 
        >>> # Create model roster
        >>> models = [
        ...     ModelInfo(id="gpt4o", rating=1200, sd=100, battles_count=50),
        ...     ModelInfo(id="claude", rating=1180, sd=120, battles_count=40),
        ...     ModelInfo(id="new_model", rating=1000, sd=350, battles_count=0),
        ... ]
        >>> 
        >>> # Get best pairing
        >>> a, b = service.select_pair_for_battle(models)
        >>> print(f"Recommended: {a.id} vs {b.id}")
        >>> 
        >>> # Get multiple non-overlapping pairings
        >>> matches = service.select_matches(models, num_matches=2)
    """
    
    def __init__(self, config: Optional[MatchmakingConfig] = None) -> None:
        """
        Initialize matchmaking service.
        
        Args:
            config: Configuration options. Uses defaults if not provided.
        """
        self.config = config or MatchmakingConfig()
    
    def expected_score(self, rating_a: float, rating_b: float) -> float:
        """Calculate expected score for model A vs model B."""
        exponent = (rating_b - rating_a) / 400.0
        return 1.0 / (1.0 + math.pow(10, exponent))
    
    def competitiveness_score(
        self,
        model_a: ModelInfo,
        model_b: ModelInfo,
    ) -> float:
        """
        Score how competitive a match would be.
        
        Best score (1.0) when models are equal strength.
        Score decreases as rating gap increases.
        
        Args:
            model_a: First model.
            model_b: Second model.
            
        Returns:
            Score from 0.0 (blowout) to 1.0 (even match).
        """
        expected = self.expected_score(model_a.rating, model_b.rating)
        # Score = 1 - 2 * |expected - 0.5|
        # At 0.5: score = 1.0
        # At 0.0 or 1.0: score = 0.0
        return 1.0 - 2.0 * abs(expected - 0.5)
    
    def uncertainty_score(
        self,
        model_a: ModelInfo,
        model_b: ModelInfo,
    ) -> float:
        """
        Score information gain from model uncertainty.
        
        Higher score for matches involving uncertain models.
        
        Args:
            model_a: First model.
            model_b: Second model.
            
        Returns:
            Score from 0.0 to 1.0.
        """
        # Normalize SD relative to default
        norm_sd_a = model_a.sd / self.config.default_sd
        norm_sd_b = model_b.sd / self.config.default_sd
        
        # Average, capped at 1.0
        avg_uncertainty = (norm_sd_a + norm_sd_b) / 2
        return min(avg_uncertainty, 1.0)
    
    def exploration_score(self) -> float:
        """Generate random exploration component."""
        return random.random()
    
    def score_match(
        self,
        model_a: ModelInfo,
        model_b: ModelInfo,
    ) -> MatchScore:
        """
        Calculate total score for a potential match.
        
        Args:
            model_a: First model.
            model_b: Second model.
            
        Returns:
            MatchScore with breakdown of components.
        """
        comp = self.competitiveness_score(model_a, model_b)
        unc = self.uncertainty_score(model_a, model_b)
        exp = self.exploration_score()
        
        total = (
            self.config.competitiveness_weight * comp +
            self.config.uncertainty_weight * unc +
            self.config.exploration_weight * exp
        )
        
        return MatchScore(
            model_a=model_a,
            model_b=model_b,
            total_score=total,
            competitiveness_score=comp,
            uncertainty_score=unc,
            exploration_score=exp,
        )
    
    def generate_all_pairs(
        self,
        models: list[ModelInfo],
    ) -> list[tuple[ModelInfo, ModelInfo]]:
        """Generate all unique model pairs."""
        pairs = []
        for i, model_a in enumerate(models):
            for model_b in models[i + 1:]:
                pairs.append((model_a, model_b))
        return pairs
    
    def select_matches(
        self,
        models: list[ModelInfo],
        num_matches: int = 1,
        avoid_repeats: bool = True,
    ) -> list[MatchScore]:
        """
        Select optimal matches from available models.
        
        Args:
            models: List of available models.
            num_matches: Number of matches to select.
            avoid_repeats: If True, each model appears in at most one match.
            
        Returns:
            List of MatchScore objects for selected matches.
            
        Raises:
            ValueError: If fewer than 2 models provided.
            
        Example:
            >>> matches = service.select_matches(models, num_matches=3)
            >>> for m in matches:
            ...     print(f"{m.model_a.id} vs {m.model_b.id}: {m.total_score:.2f}")
        """
        if len(models) < 2:
            raise ValueError("At least 2 models required for matchmaking")
        
        # Score all pairs
        pairs = self.generate_all_pairs(models)
        scores = [self.score_match(a, b) for a, b in pairs]
        scores.sort(key=lambda x: x.total_score, reverse=True)
        
        if not avoid_repeats:
            return scores[:num_matches]
        
        # Select non-overlapping matches
        selected: list[MatchScore] = []
        used_models: set[str] = set()
        
        for score in scores:
            if len(selected) >= num_matches:
                break
            
            if score.model_a.id not in used_models and score.model_b.id not in used_models:
                selected.append(score)
                used_models.add(score.model_a.id)
                used_models.add(score.model_b.id)
        
        return selected
    
    def select_pair_for_battle(
        self,
        models: list[ModelInfo],
    ) -> tuple[ModelInfo, ModelInfo]:
        """
        Select a single optimal pair for battle.
        
        Convenience method for selecting one match.
        
        Args:
            models: List of available models.
            
        Returns:
            Tuple of (model_a, model_b).
        """
        matches = self.select_matches(models, num_matches=1)
        match = matches[0]
        return match.model_a, match.model_b
    
    def select_opponent(
        self,
        model: ModelInfo,
        candidates: list[ModelInfo],
    ) -> ModelInfo:
        """
        Select the best opponent for a specific model.
        
        Args:
            model: Model to find opponent for.
            candidates: Potential opponents.
            
        Returns:
            Best opponent from candidates.
        """
        if not candidates:
            raise ValueError("At least 1 candidate required")
        
        scores: list[tuple[float, ModelInfo]] = []
        for candidate in candidates:
            if candidate.id == model.id:
                continue
            score = self.score_match(model, candidate)
            scores.append((score.total_score, candidate))
        
        if not scores:
            raise ValueError("No valid opponents found")
        
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[0][1]
    
    def recommend_battles_count(
        self,
        model: ModelInfo,
        target_sd: float = 100.0,
    ) -> int:
        """
        Estimate battles needed to reach target uncertainty.
        
        Args:
            model: Model to evaluate.
            target_sd: Target standard deviation.
            
        Returns:
            Estimated number of battles needed.
        """
        if model.sd <= target_sd:
            return 0
        
        decay_rate = 0.9
        current_sd = model.sd
        battles = 0
        
        while current_sd > target_sd and battles < 1000:
            current_sd *= decay_rate
            battles += 1
        
        return battles

