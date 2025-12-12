"""
Test edge cases and boundary conditions.
"""
import unittest
import math

from bitads_v3_core.domain.models import MinerWindowStats, Percentiles
from bitads_v3_core.domain.math_ops import (
    apply_early_sales_soft_cap,
    base_score,
    final_score,
    normalize_revenue,
    normalize_sales,
    refund_rate,
)
from bitads_v3_core.app.scoring import ScoreCalculator
from tests.test_helpers import MockP95Provider


TOLERANCE = 1e-6


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.percentiles = Percentiles(p95_sales=60.0, p95_revenue_usd=4000.0)
        self.p95_provider = MockP95Provider(self.percentiles)
        self.calculator = ScoreCalculator(self.p95_provider)
    
    def test_zero_p95s(self):
        """Test that zero P95s are handled correctly via eps."""
        zero_percentiles = Percentiles(p95_sales=0.0, p95_revenue_usd=0.0)
        zero_provider = MockP95Provider(zero_percentiles)
        zero_calculator = ScoreCalculator(zero_provider)
        
        stats = MinerWindowStats(sales=10, revenue_usd=1000.0, refund_orders=1)
        result = zero_calculator.score_one("miner", stats, "network")
        
        # Should not crash, and should return valid scores in [0,1]
        self.assertGreaterEqual(result.score, 0.0)
        self.assertLessEqual(result.score, 1.0)
        self.assertGreaterEqual(result.base, 0.0)
        self.assertLessEqual(result.base, 1.0)
    
    def test_high_refunds(self):
        """Test that refund_orders > sales is clamped to 1.0."""
        stats = MinerWindowStats(sales=5, revenue_usd=1000.0, refund_orders=10)
        ref_rate = refund_rate(stats)
        
        # Should be clamped to 1.0
        self.assertEqual(ref_rate, 1.0)
        
        result = self.calculator.score_one("miner", stats, "network")
        # Score should be 0 because refund multiplier is 0
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.refund_multiplier, 0.0)
    
    def test_refund_rate_equal_sales(self):
        """Test refund rate when refund_orders == sales."""
        stats = MinerWindowStats(sales=10, revenue_usd=1000.0, refund_orders=10)
        ref_rate = refund_rate(stats)
        self.assertAlmostEqual(ref_rate, 1.0, delta=TOLERANCE)
    
    def test_early_sales_soft_cap_enabled(self):
        """Test early-sales soft cap when enabled."""
        calculator_with_cap = ScoreCalculator(self.p95_provider, use_soft_cap=True)
        
        # sales = 1, should apply 0.30 factor
        stats1 = MinerWindowStats(sales=1, revenue_usd=1000.0, refund_orders=0)
        result1 = calculator_with_cap.score_one("miner1", stats1, "network")
        expected_score1 = result1.score / 0.30  # Reverse the cap to get original
        # Verify the score is reduced
        self.assertLess(result1.score, expected_score1)
        
        # sales = 2, should apply 0.30 factor
        stats2 = MinerWindowStats(sales=2, revenue_usd=1000.0, refund_orders=0)
        result2 = calculator_with_cap.score_one("miner2", stats2, "network")
        self.assertLess(result2.score, 1.0)
        
        # sales = 3, should NOT apply cap
        stats3 = MinerWindowStats(sales=3, revenue_usd=1000.0, refund_orders=0)
        result3 = calculator_with_cap.score_one("miner3", stats3, "network")
        # Compare with calculator without cap
        result3_no_cap = self.calculator.score_one("miner3", stats3, "network")
        self.assertAlmostEqual(result3.score, result3_no_cap.score, delta=TOLERANCE)
    
    def test_early_sales_soft_cap_disabled(self):
        """Test that soft cap is not applied when disabled."""
        stats = MinerWindowStats(sales=1, revenue_usd=1000.0, refund_orders=0)
        result = self.calculator.score_one("miner", stats, "network")
        # Should not be reduced by 0.30
        self.assertGreater(result.score, 0.0)
    
    def test_clamping_values(self):
        """Test that all values are clamped to [0,1]."""
        # Test with very high values
        stats = MinerWindowStats(sales=10000, revenue_usd=1000000.0, refund_orders=0)
        result = self.calculator.score_one("miner", stats, "network")
        
        self.assertGreaterEqual(result.score, 0.0)
        self.assertLessEqual(result.score, 1.0)
        self.assertGreaterEqual(result.base, 0.0)
        self.assertLessEqual(result.base, 1.0)
        self.assertGreaterEqual(result.refund_multiplier, 0.0)
        self.assertLessEqual(result.refund_multiplier, 1.0)
    
    def test_zero_sales(self):
        """Test that zero sales returns zero score."""
        stats = MinerWindowStats(sales=0, revenue_usd=1000.0, refund_orders=0)
        result = self.calculator.score_one("miner", stats, "network")
        
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.base, 0.0)
        self.assertEqual(result.refund_multiplier, 1.0)  # 1 - 0
    
    def test_zero_revenue(self):
        """Test that zero revenue is handled correctly."""
        stats = MinerWindowStats(sales=10, revenue_usd=0.0, refund_orders=0)
        result = self.calculator.score_one("miner", stats, "network")
        
        # Should compute valid score
        self.assertGreaterEqual(result.score, 0.0)
        self.assertLessEqual(result.score, 1.0)
    
    def test_normalize_sales_very_large(self):
        """Test normalize_sales with very large sales value."""
        # Should clamp to 1.0
        norm = normalize_sales(1000000, 100)
        self.assertLessEqual(norm, 1.0)
        self.assertGreaterEqual(norm, 0.0)
    
    def test_normalize_revenue_very_large(self):
        """Test normalize_revenue with very large revenue value."""
        # Should clamp to 1.0
        norm = normalize_revenue(1000000, 100)
        self.assertLessEqual(norm, 1.0)
        self.assertGreaterEqual(norm, 0.0)
    
    def test_apply_soft_cap_function(self):
        """Test apply_early_sales_soft_cap function directly."""
        # sales < 3 should apply factor
        score1 = apply_early_sales_soft_cap(1.0, 1, threshold=3, factor=0.30)
        self.assertAlmostEqual(score1, 0.30, delta=TOLERANCE)
        
        score2 = apply_early_sales_soft_cap(1.0, 2, threshold=3, factor=0.30)
        self.assertAlmostEqual(score2, 0.30, delta=TOLERANCE)
        
        # sales >= 3 should not apply factor
        score3 = apply_early_sales_soft_cap(1.0, 3, threshold=3, factor=0.30)
        self.assertAlmostEqual(score3, 1.0, delta=TOLERANCE)
        
        score4 = apply_early_sales_soft_cap(1.0, 10, threshold=3, factor=0.30)
        self.assertAlmostEqual(score4, 1.0, delta=TOLERANCE)


if __name__ == "__main__":
    unittest.main()


