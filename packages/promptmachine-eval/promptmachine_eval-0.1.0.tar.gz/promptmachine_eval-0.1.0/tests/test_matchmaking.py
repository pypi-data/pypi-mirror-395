"""
Tests for matchmaking module.
"""

import pytest
from promptmachine_eval.matchmaking import (
    MatchmakingService,
    MatchmakingConfig,
    ModelInfo,
)


@pytest.fixture
def sample_models() -> list[ModelInfo]:
    """Create sample models for testing."""
    return [
        ModelInfo(id="gpt4o", rating=1200, sd=100, battles_count=50),
        ModelInfo(id="claude", rating=1180, sd=120, battles_count=40),
        ModelInfo(id="gemini", rating=1100, sd=200, battles_count=10),
        ModelInfo(id="llama", rating=1050, sd=300, battles_count=5),
        ModelInfo(id="mistral", rating=1000, sd=350, battles_count=0),
    ]


class TestMatchmakingService:
    """Tests for MatchmakingService."""
    
    def test_competitiveness_score_equal_ratings(self) -> None:
        """Equal ratings should give perfect competitiveness score."""
        service = MatchmakingService()
        model_a = ModelInfo(id="a", rating=1000, sd=100)
        model_b = ModelInfo(id="b", rating=1000, sd=100)
        
        score = service.competitiveness_score(model_a, model_b)
        assert abs(score - 1.0) < 0.01
    
    def test_competitiveness_score_different_ratings(self) -> None:
        """Different ratings should give lower competitiveness score."""
        service = MatchmakingService()
        model_a = ModelInfo(id="a", rating=1200, sd=100)
        model_b = ModelInfo(id="b", rating=1000, sd=100)
        
        score = service.competitiveness_score(model_a, model_b)
        assert score < 0.7  # Not very competitive
    
    def test_uncertainty_score_high_sd(self) -> None:
        """High uncertainty models should have higher uncertainty score."""
        service = MatchmakingService()
        model_a = ModelInfo(id="a", rating=1000, sd=350)  # Default SD
        model_b = ModelInfo(id="b", rating=1000, sd=350)
        
        score = service.uncertainty_score(model_a, model_b)
        assert score >= 0.9  # Near max
    
    def test_uncertainty_score_low_sd(self) -> None:
        """Low uncertainty should give lower score."""
        service = MatchmakingService()
        model_a = ModelInfo(id="a", rating=1000, sd=100)
        model_b = ModelInfo(id="b", rating=1000, sd=100)
        
        score = service.uncertainty_score(model_a, model_b)
        assert score < 0.5
    
    def test_select_pair_returns_two_models(self, sample_models: list[ModelInfo]) -> None:
        """Should return exactly two models."""
        service = MatchmakingService()
        model_a, model_b = service.select_pair_for_battle(sample_models)
        
        assert model_a is not None
        assert model_b is not None
        assert model_a.id != model_b.id
    
    def test_select_pair_minimum_models(self) -> None:
        """Should work with just 2 models."""
        service = MatchmakingService()
        models = [
            ModelInfo(id="a", rating=1000, sd=200),
            ModelInfo(id="b", rating=1000, sd=200),
        ]
        
        model_a, model_b = service.select_pair_for_battle(models)
        assert {model_a.id, model_b.id} == {"a", "b"}
    
    def test_select_pair_raises_with_one_model(self) -> None:
        """Should raise error with only 1 model."""
        service = MatchmakingService()
        models = [ModelInfo(id="a", rating=1000, sd=200)]
        
        with pytest.raises(ValueError):
            service.select_pair_for_battle(models)
    
    def test_select_matches_respects_count(self, sample_models: list[ModelInfo]) -> None:
        """Should return requested number of matches."""
        service = MatchmakingService()
        matches = service.select_matches(sample_models, num_matches=2)
        
        assert len(matches) == 2
    
    def test_select_matches_avoid_repeats(self, sample_models: list[ModelInfo]) -> None:
        """Each model should appear in at most one match when avoiding repeats."""
        service = MatchmakingService()
        matches = service.select_matches(sample_models, num_matches=2, avoid_repeats=True)
        
        used_ids: set[str] = set()
        for match in matches:
            assert match.model_a.id not in used_ids
            assert match.model_b.id not in used_ids
            used_ids.add(match.model_a.id)
            used_ids.add(match.model_b.id)
    
    def test_select_opponent(self, sample_models: list[ModelInfo]) -> None:
        """Should find an opponent for a specific model."""
        service = MatchmakingService()
        target = sample_models[0]
        candidates = sample_models[1:]
        
        opponent = service.select_opponent(target, candidates)
        
        assert opponent.id != target.id
        assert opponent in candidates
    
    def test_generate_all_pairs(self) -> None:
        """Should generate all unique pairs."""
        service = MatchmakingService()
        models = [
            ModelInfo(id="a", rating=1000, sd=100),
            ModelInfo(id="b", rating=1000, sd=100),
            ModelInfo(id="c", rating=1000, sd=100),
        ]
        
        pairs = service.generate_all_pairs(models)
        
        # 3 models = 3 pairs (ab, ac, bc)
        assert len(pairs) == 3
        
        # No duplicates
        pair_ids = [(p[0].id, p[1].id) for p in pairs]
        assert len(pair_ids) == len(set(pair_ids))
    
    def test_recommend_battles_count_for_converged(self) -> None:
        """Model with low SD should need 0 battles."""
        service = MatchmakingService()
        model = ModelInfo(id="a", rating=1200, sd=80)
        
        count = service.recommend_battles_count(model, target_sd=100)
        assert count == 0
    
    def test_recommend_battles_count_for_new(self) -> None:
        """New model with high SD should need battles."""
        service = MatchmakingService()
        model = ModelInfo(id="a", rating=1000, sd=350)
        
        count = service.recommend_battles_count(model, target_sd=100)
        assert count > 0
        assert count < 100  # Reasonable upper bound


class TestMatchScore:
    """Tests for match scoring."""
    
    def test_score_match_has_all_components(self, sample_models: list[ModelInfo]) -> None:
        """Score should include all components."""
        service = MatchmakingService()
        score = service.score_match(sample_models[0], sample_models[1])
        
        assert score.model_a is not None
        assert score.model_b is not None
        assert 0 <= score.competitiveness_score <= 1
        assert 0 <= score.uncertainty_score <= 1
        assert 0 <= score.exploration_score <= 1
        assert score.total_score >= 0
    
    def test_competitive_match_scores_higher(self) -> None:
        """Competitive matches should score higher overall."""
        config = MatchmakingConfig(
            competitiveness_weight=0.8,
            uncertainty_weight=0.1,
            exploration_weight=0.1,
        )
        service = MatchmakingService(config)
        
        # Very competitive
        close_a = ModelInfo(id="a", rating=1000, sd=100)
        close_b = ModelInfo(id="b", rating=1010, sd=100)
        
        # Not competitive
        far_a = ModelInfo(id="c", rating=1000, sd=100)
        far_b = ModelInfo(id="d", rating=1400, sd=100)
        
        score_close = service.score_match(close_a, close_b)
        score_far = service.score_match(far_a, far_b)
        
        # On average, close match should score higher
        # (accounting for random exploration)
        assert score_close.competitiveness_score > score_far.competitiveness_score

