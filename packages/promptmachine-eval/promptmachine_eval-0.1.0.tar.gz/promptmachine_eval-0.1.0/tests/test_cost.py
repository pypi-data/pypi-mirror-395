"""
Tests for cost tracking module.
"""

import pytest
from promptmachine_eval.cost import CostTracker, MODEL_PRICING


class TestCostTracker:
    """Tests for CostTracker class."""
    
    def test_count_tokens_basic(self) -> None:
        """Should estimate token count."""
        tracker = CostTracker()
        
        # ~4 chars per token
        count = tracker.count_tokens("Hello world")  # 11 chars
        assert 2 <= count <= 5
    
    def test_count_tokens_long_text(self) -> None:
        """Long text should have more tokens."""
        tracker = CostTracker()
        
        short = tracker.count_tokens("Hi")
        long = tracker.count_tokens("Hello world, this is a longer piece of text.")
        
        assert long > short
    
    def test_get_pricing_known_model(self) -> None:
        """Should return correct pricing for known models."""
        tracker = CostTracker()
        pricing = tracker.get_pricing("gpt-4o-mini")
        
        assert "input" in pricing
        assert "output" in pricing
        assert pricing["input"] > 0
        assert pricing["output"] > 0
    
    def test_get_pricing_alias(self) -> None:
        """Should resolve model aliases."""
        tracker = CostTracker()
        pricing = tracker.get_pricing("claude-3-5-sonnet")
        
        assert "input" in pricing
        assert pricing["input"] > 0
    
    def test_get_pricing_unknown_model(self) -> None:
        """Unknown models should get default pricing."""
        tracker = CostTracker()
        pricing = tracker.get_pricing("unknown-model-xyz")
        
        assert "input" in pricing
        assert "output" in pricing
    
    def test_estimate_returns_all_fields(self) -> None:
        """Estimate should include all cost fields."""
        tracker = CostTracker()
        estimate = tracker.estimate("Hello world", "gpt-4o-mini")
        
        assert estimate.model == "gpt-4o-mini"
        assert estimate.input_tokens > 0
        assert estimate.output_tokens > 0  # Default 500
        assert estimate.input_cost >= 0
        assert estimate.output_cost >= 0
        assert estimate.total == estimate.input_cost + estimate.output_cost
    
    def test_estimate_custom_output_tokens(self) -> None:
        """Should respect custom output token estimate."""
        tracker = CostTracker()
        estimate = tracker.estimate(
            "Hello",
            "gpt-4o-mini",
            expected_output_tokens=1000,
        )
        
        assert estimate.output_tokens == 1000
    
    def test_calculate_cost_matches_estimate(self) -> None:
        """Calculate should give same result as estimate for same tokens."""
        tracker = CostTracker()
        
        estimate = tracker.estimate(
            "Test prompt",
            "gpt-4o-mini",
            expected_output_tokens=100,
        )
        
        calculated = tracker.calculate_cost(
            "gpt-4o-mini",
            estimate.input_tokens,
            100,
        )
        
        assert abs(calculated - estimate.total) < 0.0001
    
    def test_track_usage_accumulates(self) -> None:
        """Session cost should accumulate."""
        tracker = CostTracker()
        
        assert tracker.session_cost == 0
        
        tracker.track_usage("gpt-4o-mini", 100, 200)
        first_cost = tracker.session_cost
        
        tracker.track_usage("gpt-4o-mini", 100, 200)
        second_cost = tracker.session_cost
        
        assert second_cost > first_cost
        assert abs(second_cost - 2 * first_cost) < 0.0001
    
    def test_track_usage_counts_tokens(self) -> None:
        """Should track total tokens."""
        tracker = CostTracker()
        
        tracker.track_usage("gpt-4o-mini", 100, 200)
        assert tracker.session_tokens == 300
        
        tracker.track_usage("gpt-4o-mini", 50, 100)
        assert tracker.session_tokens == 450
    
    def test_check_budget_under_limit(self) -> None:
        """Should return True when under budget."""
        tracker = CostTracker(session_budget=1.00)
        
        assert tracker.check_budget(0.50)
    
    def test_check_budget_over_limit(self) -> None:
        """Should return False when over budget."""
        tracker = CostTracker(session_budget=0.10)
        
        # Use up most of budget
        tracker.session_cost = 0.08
        
        # This would exceed
        assert not tracker.check_budget(0.05)
    
    def test_get_summary(self) -> None:
        """Summary should include key stats."""
        tracker = CostTracker(session_budget=5.00)
        
        tracker.track_usage("gpt-4o-mini", 100, 200)
        tracker.track_usage("gpt-4o", 50, 100)
        
        summary = tracker.get_summary()
        
        assert "total_cost" in summary
        assert "total_tokens" in summary
        assert "num_calls" in summary
        assert summary["num_calls"] == 2
        assert summary["total_tokens"] == 450
    
    def test_reset_session(self) -> None:
        """Reset should clear all session data."""
        tracker = CostTracker()
        
        tracker.track_usage("gpt-4o-mini", 100, 200)
        assert tracker.session_cost > 0
        
        tracker.reset_session()
        
        assert tracker.session_cost == 0
        assert tracker.session_tokens == 0


class TestModelPricing:
    """Tests for model pricing data."""
    
    def test_pricing_has_major_models(self) -> None:
        """Should include pricing for major models."""
        assert "gpt-4o" in MODEL_PRICING
        assert "gpt-4o-mini" in MODEL_PRICING
        assert "claude-3-5-sonnet-latest" in MODEL_PRICING
    
    def test_pricing_values_reasonable(self) -> None:
        """Pricing should be positive and reasonable."""
        for model, pricing in MODEL_PRICING.items():
            assert pricing["input"] > 0, f"{model} input price invalid"
            assert pricing["output"] > 0, f"{model} output price invalid"
            # Output usually costs more than input
            assert pricing["output"] >= pricing["input"] * 0.5, f"{model} pricing ratio odd"

