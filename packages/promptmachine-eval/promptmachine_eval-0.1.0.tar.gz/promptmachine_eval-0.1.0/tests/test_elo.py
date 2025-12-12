"""
Tests for ELO calculation module.
"""

import pytest
from promptmachine_eval.elo import EloCalculator, EloConfig


class TestEloCalculator:
    """Tests for EloCalculator class."""
    
    def test_expected_score_equal_ratings(self) -> None:
        """Equal ratings should give 50% expected score."""
        calc = EloCalculator()
        score = calc.expected_score(1000, 1000)
        assert abs(score - 0.5) < 0.001
    
    def test_expected_score_higher_rated_favored(self) -> None:
        """Higher-rated model should have > 50% expected score."""
        calc = EloCalculator()
        score = calc.expected_score(1200, 1000)
        assert score > 0.5
        assert score < 1.0
    
    def test_expected_score_lower_rated_underdog(self) -> None:
        """Lower-rated model should have < 50% expected score."""
        calc = EloCalculator()
        score = calc.expected_score(1000, 1200)
        assert score < 0.5
        assert score > 0.0
    
    def test_expected_score_sum_to_one(self) -> None:
        """Expected scores for both players should sum to 1."""
        calc = EloCalculator()
        score_a = calc.expected_score(1200, 1000)
        score_b = calc.expected_score(1000, 1200)
        assert abs(score_a + score_b - 1.0) < 0.001
    
    def test_update_ratings_winner_gains(self) -> None:
        """Winner should gain rating points."""
        calc = EloCalculator()
        old_rating = 1000
        new_a, new_b = calc.update_ratings(old_rating, old_rating, score_a=1.0)
        assert new_a > old_rating
    
    def test_update_ratings_loser_loses(self) -> None:
        """Loser should lose rating points."""
        calc = EloCalculator()
        old_rating = 1000
        new_a, new_b = calc.update_ratings(old_rating, old_rating, score_a=1.0)
        assert new_b < old_rating
    
    def test_update_ratings_draw_no_change(self) -> None:
        """Equal ratings + draw should result in minimal change."""
        calc = EloCalculator()
        new_a, new_b = calc.update_ratings(1000, 1000, score_a=0.5)
        assert abs(new_a - 1000) < 1  # Very small change
        assert abs(new_b - 1000) < 1
    
    def test_update_ratings_upset_big_change(self) -> None:
        """Upset wins should cause larger rating changes."""
        calc = EloCalculator()
        # Lower-rated wins
        new_a, new_b = calc.update_ratings(1000, 1200, score_a=1.0)
        # Should gain more than expected
        change = new_a - 1000
        assert change > 16  # More than half K-factor
    
    def test_update_ratings_expected_win_small_change(self) -> None:
        """Expected wins should cause smaller rating changes."""
        calc = EloCalculator()
        # Higher-rated wins (expected)
        new_a, new_b = calc.update_ratings(1200, 1000, score_a=1.0)
        change = new_a - 1200
        assert change < 16  # Less than half K-factor
    
    def test_update_ratings_zero_sum(self) -> None:
        """Rating changes should sum to zero."""
        calc = EloCalculator()
        new_a, new_b = calc.update_ratings(1100, 900, score_a=1.0)
        change_a = new_a - 1100
        change_b = new_b - 900
        assert abs(change_a + change_b) < 0.001
    
    def test_custom_k_factor(self) -> None:
        """Custom K-factor should affect change magnitude."""
        config_low = EloConfig(k_factor=16)
        config_high = EloConfig(k_factor=64)
        
        calc_low = EloCalculator(config_low)
        calc_high = EloCalculator(config_high)
        
        new_low_a, _ = calc_low.update_ratings(1000, 1000, score_a=1.0)
        new_high_a, _ = calc_high.update_ratings(1000, 1000, score_a=1.0)
        
        change_low = new_low_a - 1000
        change_high = new_high_a - 1000
        
        assert change_high > change_low * 2  # Roughly 4x
    
    def test_update_sd_decreases(self) -> None:
        """SD should decrease after each battle."""
        calc = EloCalculator()
        new_sd = calc.update_sd(350.0)
        assert new_sd < 350.0
    
    def test_update_sd_respects_minimum(self) -> None:
        """SD should not go below minimum."""
        config = EloConfig(min_sd=100.0, sd_decay_rate=0.5)
        calc = EloCalculator(config)
        
        # After many updates, should hit minimum
        sd = 350.0
        for _ in range(100):
            sd = calc.update_sd(sd)
        
        assert sd >= 100.0
    
    def test_confidence_interval(self) -> None:
        """Confidence interval should contain rating."""
        calc = EloCalculator()
        low, high = calc.confidence_interval(1200, 100, 0.95)
        
        assert low < 1200
        assert high > 1200
        assert high - low > 100  # Reasonable spread
    
    def test_update_after_battle_returns_all_fields(self) -> None:
        """Full update should return all fields."""
        calc = EloCalculator()
        result = calc.update_after_battle(
            rating_a=1200,
            rating_b=1000,
            sd_a=200,
            sd_b=300,
            score_a=1.0,
        )
        
        assert result.new_rating_a > 1200
        assert result.new_rating_b < 1000
        assert result.rating_change_a > 0
        assert result.rating_change_b < 0
        assert result.expected_score_a > 0.5
        assert result.new_sd_a < 200
        assert result.new_sd_b < 300


class TestWinProbability:
    """Tests for Monte Carlo win probability."""
    
    def test_equal_ratings_near_50_percent(self) -> None:
        """Equal ratings should give ~50% win probability."""
        calc = EloCalculator()
        prob = calc.win_probability(1000, 1000)
        assert 0.45 < prob < 0.55
    
    def test_higher_rated_higher_probability(self) -> None:
        """Higher rated should have higher win probability."""
        calc = EloCalculator()
        prob = calc.win_probability(1200, 1000)
        assert prob > 0.6
    
    def test_uncertainty_affects_probability(self) -> None:
        """High uncertainty should bring probability closer to 50%."""
        calc = EloCalculator()
        
        # No uncertainty
        prob_certain = calc.win_probability(1200, 1000, sd_a=0, sd_b=0)
        
        # High uncertainty
        prob_uncertain = calc.win_probability(1200, 1000, sd_a=200, sd_b=200)
        
        # With uncertainty, probabilities should be closer to 0.5
        assert abs(prob_uncertain - 0.5) < abs(prob_certain - 0.5)

