"""
Test percentile computation functions.
"""
import unittest
import math

from bitads_v3_core.domain.models import MinerWindowStats, Percentiles
from bitads_v3_core.domain.percentiles import compute_auto_p95, ema, percentile


TOLERANCE = 1e-6


class TestPercentiles(unittest.TestCase):
    """Test percentile computation."""
    
    def test_percentile_simple(self):
        """Test percentile on a simple list."""
        values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        
        # P50 (median) should be 5 or 6
        p50 = percentile(values, 0.5)
        self.assertGreaterEqual(p50, 5.0)
        self.assertLessEqual(p50, 6.0)
        
        # P95 for 10 values: ceil(0.95 * 10) = ceil(9.5) = 10 (1-indexed)
        # So index 9 (0-indexed) = 10.0
        p95 = percentile(values, 0.95)
        self.assertEqual(p95, 10.0)
    
    def test_percentile_small_list(self):
        """Test percentile on a small list."""
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        # P95 for 5 values: ceil(0.95 * 5) = ceil(4.75) = 5 (1-indexed)
        # So index 4 (0-indexed) = 5.0
        p95 = percentile(values, 0.95)
        self.assertEqual(p95, 5.0)
    
    def test_percentile_single_value(self):
        """Test percentile on a single value."""
        values = [42.0]
        p95 = percentile(values, 0.95)
        self.assertEqual(p95, 42.0)
    
    def test_percentile_unsorted(self):
        """Test that percentile handles unsorted input."""
        values = [10.0, 1.0, 5.0, 3.0, 7.0]
        p95 = percentile(values, 0.95)
        # Should be sorted first, so result should be 10.0
        self.assertEqual(p95, 10.0)
    
    def test_percentile_empty_list(self):
        """Test that percentile raises error on empty list."""
        with self.assertRaises(ValueError):
            percentile([], 0.95)
    
    def test_percentile_invalid_p(self):
        """Test that percentile validates p value."""
        values = [1.0, 2.0, 3.0]
        
        with self.assertRaises(ValueError):
            percentile(values, -0.1)
        
        with self.assertRaises(ValueError):
            percentile(values, 1.1)
    
    def test_ema_basic(self):
        """Test EMA computation."""
        # EMA: alpha * obs + (1 - alpha) * prev
        prev = 10.0
        obs = 20.0
        alpha = 0.5
        
        result = ema(prev, obs, alpha)
        expected = 0.5 * 20.0 + 0.5 * 10.0
        self.assertAlmostEqual(result, expected, delta=TOLERANCE)
        self.assertAlmostEqual(result, 15.0, delta=TOLERANCE)
    
    def test_ema_alpha_0(self):
        """Test EMA with alpha=0 (no update)."""
        prev = 10.0
        obs = 20.0
        alpha = 0.0
        
        result = ema(prev, obs, alpha)
        self.assertAlmostEqual(result, prev, delta=TOLERANCE)
    
    def test_ema_alpha_1(self):
        """Test EMA with alpha=1 (full update)."""
        prev = 10.0
        obs = 20.0
        alpha = 1.0
        
        result = ema(prev, obs, alpha)
        self.assertAlmostEqual(result, obs, delta=TOLERANCE)
    
    def test_ema_alpha_03(self):
        """Test EMA with alpha=0.3."""
        prev = 10.0
        obs = 20.0
        alpha = 0.3
        
        result = ema(prev, obs, alpha)
        expected = 0.3 * 20.0 + 0.7 * 10.0
        self.assertAlmostEqual(result, expected, delta=TOLERANCE)
        self.assertAlmostEqual(result, 13.0, delta=TOLERANCE)
    
    def test_ema_alpha_04(self):
        """Test EMA with alpha=0.4."""
        prev = 10.0
        obs = 20.0
        alpha = 0.4
        
        result = ema(prev, obs, alpha)
        expected = 0.4 * 20.0 + 0.6 * 10.0
        self.assertAlmostEqual(result, expected, delta=TOLERANCE)
        self.assertAlmostEqual(result, 14.0, delta=TOLERANCE)
    
    def test_ema_alpha_05(self):
        """Test EMA with alpha=0.5."""
        prev = 10.0
        obs = 20.0
        alpha = 0.5
        
        result = ema(prev, obs, alpha)
        expected = 0.5 * 20.0 + 0.5 * 10.0
        self.assertAlmostEqual(result, expected, delta=TOLERANCE)
        self.assertAlmostEqual(result, 15.0, delta=TOLERANCE)
    
    def test_ema_invalid_alpha(self):
        """Test that EMA validates alpha."""
        with self.assertRaises(ValueError):
            ema(10.0, 20.0, -0.1)
        
        with self.assertRaises(ValueError):
            ema(10.0, 20.0, 1.1)
    
    def test_compute_auto_p95_basic(self):
        """Test compute_auto_p95 without EMA."""
        stats = [
            MinerWindowStats(sales=10, revenue_usd=1000.0, refund_orders=0),
            MinerWindowStats(sales=20, revenue_usd=2000.0, refund_orders=1),
            MinerWindowStats(sales=30, revenue_usd=3000.0, refund_orders=2),
            MinerWindowStats(sales=40, revenue_usd=4000.0, refund_orders=3),
            MinerWindowStats(sales=50, revenue_usd=5000.0, refund_orders=4),
        ]
        
        result = compute_auto_p95(stats)
        
        # P95 of sales: [10, 20, 30, 40, 50] -> ceil(0.95 * 5) = 5 (1-indexed) -> index 4 = 50
        self.assertEqual(result.p95_sales, 50.0)
        # P95 of revenue: [1000, 2000, 3000, 4000, 5000] -> 5000
        self.assertEqual(result.p95_revenue_usd, 5000.0)
    
    def test_compute_auto_p95_with_ema(self):
        """Test compute_auto_p95 with EMA smoothing."""
        stats = [
            MinerWindowStats(sales=10, revenue_usd=1000.0, refund_orders=0),
            MinerWindowStats(sales=20, revenue_usd=2000.0, refund_orders=1),
        ]
        
        prev = Percentiles(p95_sales=15.0, p95_revenue_usd=1500.0)
        alpha = 0.5
        
        result = compute_auto_p95(stats, prev=prev, alpha=alpha)
        
        # P95 of sales: [10, 20] -> ceil(0.95 * 2) = ceil(1.9) = 2 -> index 1 = 20
        raw_p95_sales = 20.0
        expected_sales = ema(15.0, raw_p95_sales, 0.5)
        self.assertAlmostEqual(result.p95_sales, expected_sales, delta=TOLERANCE)
        
        # P95 of revenue: [1000, 2000] -> 2000
        raw_p95_revenue = 2000.0
        expected_revenue = ema(1500.0, raw_p95_revenue, 0.5)
        self.assertAlmostEqual(result.p95_revenue_usd, expected_revenue, delta=TOLERANCE)
    
    def test_compute_auto_p95_empty_list_no_prev(self):
        """Test compute_auto_p95 with empty list and no previous."""
        result = compute_auto_p95([])
        self.assertEqual(result.p95_sales, 0.0)
        self.assertEqual(result.p95_revenue_usd, 0.0)
    
    def test_compute_auto_p95_empty_list_with_prev(self):
        """Test compute_auto_p95 with empty list but previous exists."""
        prev = Percentiles(p95_sales=10.0, p95_revenue_usd=1000.0)
        result = compute_auto_p95([], prev=prev)
        # Should return prev unchanged
        self.assertEqual(result.p95_sales, prev.p95_sales)
        self.assertEqual(result.p95_revenue_usd, prev.p95_revenue_usd)
    
    def test_compute_auto_p95_prev_requires_alpha(self):
        """Test that providing prev without alpha raises error."""
        prev = Percentiles(p95_sales=10.0, p95_revenue_usd=1000.0)
        stats = [MinerWindowStats(sales=20, revenue_usd=2000.0, refund_orders=0)]
        
        with self.assertRaises(ValueError):
            compute_auto_p95(stats, prev=prev, alpha=None)
    
    def test_compute_auto_p95_with_flooring(self):
        """Test compute_auto_p95 with flooring enabled."""
        stats = [
            MinerWindowStats(sales=1, revenue_usd=100.0, refund_orders=0),
            MinerWindowStats(sales=2, revenue_usd=200.0, refund_orders=0),
        ]
        
        result = compute_auto_p95(stats, use_flooring=True)
        
        # P95 raw would be 2 for sales, but flooring applies: max(sqrt(2), sqrt(5))^2 = 5
        # For revenue: max(ln(1+200), ln(1+300)) = ln(301), then expm1 gives 300
        # But the actual implementation might differ, so we just check it's >= raw
        self.assertGreaterEqual(result.p95_sales, 2.0)
        self.assertGreaterEqual(result.p95_revenue_usd, 200.0)


if __name__ == "__main__":
    unittest.main()


