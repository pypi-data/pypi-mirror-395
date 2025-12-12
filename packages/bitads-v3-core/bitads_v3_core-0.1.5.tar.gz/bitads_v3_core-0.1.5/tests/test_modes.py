"""
Test P95 mode behavior (manual vs auto).
"""
import unittest

from bitads_v3_core.domain.models import MinerWindowStats, Percentiles, P95Config, P95Mode
from bitads_v3_core.domain.percentiles import compute_auto_p95
from bitads_v3_core.app.ports import IP95Provider
from bitads_v3_core.app.scoring import ScoreCalculator


TOLERANCE = 1e-6


class ManualP95Provider(IP95Provider):
    """P95 provider that returns manual constants."""
    
    def __init__(self, config: P95Config):
        """
        Initialize with P95Config.
        
        Args:
            config: P95Config with manual mode and values
        """
        if config.mode != P95Mode.MANUAL:
            raise ValueError("ManualP95Provider requires MANUAL mode")
        self.config = config
    
    def get_effective_p95(self, scope: str) -> Percentiles:
        """Return manual constants from config."""
        return Percentiles(
            p95_sales=self.config.manual_p95_sales,
            p95_revenue_usd=self.config.manual_p95_revenue_usd
        )


class AutoP95Provider(IP95Provider):
    """P95 provider that computes P95 from miner stats."""
    
    def __init__(self, miner_stats: list[MinerWindowStats], config: P95Config):
        """
        Initialize with miner stats and config.
        
        Args:
            miner_stats: List of all miner statistics
            config: P95Config with AUTO mode
        """
        if config.mode != P95Mode.AUTO:
            raise ValueError("AutoP95Provider requires AUTO mode")
        self.miner_stats = miner_stats
        self.config = config
        self.prev = None
        self.use_flooring = False  # Can be set externally
    
    def get_effective_p95(self, scope: str) -> Percentiles:
        """Compute P95 from miner stats."""
        return compute_auto_p95(
            self.miner_stats,
            prev=self.prev,
            alpha=self.config.ema_alpha,
            use_flooring=self.use_flooring
        )


class TestModes(unittest.TestCase):
    """Test manual vs auto mode behavior."""
    
    def test_manual_mode_returns_constants(self):
        """Test that manual mode returns manual constants regardless of inputs."""
        config = P95Config(
            mode=P95Mode.MANUAL,
            manual_p95_sales=60.0,
            manual_p95_revenue_usd=4000.0,
            scope="network"
        )
        provider = ManualP95Provider(config)
        calculator = ScoreCalculator(provider)
        
        # Use different stats, but P95 should still be manual constants
        stats = MinerWindowStats(sales=100, revenue_usd=10000.0, refund_orders=0)
        result = calculator.score_one("miner", stats, "network")
        
        # Verify the score was computed using manual P95s (60, 4000)
        # not auto-computed ones
        p95 = provider.get_effective_p95("network")
        self.assertEqual(p95.p95_sales, 60.0)
        self.assertEqual(p95.p95_revenue_usd, 4000.0)
        
        # Result should be valid
        self.assertGreaterEqual(result.score, 0.0)
        self.assertLessEqual(result.score, 1.0)
    
    def test_auto_mode_computes_from_stats(self):
        """Test that auto mode computes P95 from given sample set."""
        miner_stats = [
            MinerWindowStats(sales=10, revenue_usd=1000.0, refund_orders=0),
            MinerWindowStats(sales=20, revenue_usd=2000.0, refund_orders=1),
            MinerWindowStats(sales=30, revenue_usd=3000.0, refund_orders=2),
            MinerWindowStats(sales=40, revenue_usd=4000.0, refund_orders=3),
            MinerWindowStats(sales=50, revenue_usd=5000.0, refund_orders=4),
        ]
        
        config = P95Config(
            mode=P95Mode.AUTO,
            scope="network"
        )
        provider = AutoP95Provider(miner_stats, config)
        calculator = ScoreCalculator(provider)
        
        # Get P95 - should be computed from stats
        p95 = provider.get_effective_p95("network")
        self.assertEqual(p95.p95_sales, 50.0)  # P95 of [10,20,30,40,50]
        self.assertEqual(p95.p95_revenue_usd, 5000.0)  # P95 of [1000,2000,3000,4000,5000]
        
        # Score a miner using these auto-computed P95s
        stats = MinerWindowStats(sales=25, revenue_usd=2500.0, refund_orders=1)
        result = calculator.score_one("miner", stats, "network")
        
        self.assertGreaterEqual(result.score, 0.0)
        self.assertLessEqual(result.score, 1.0)
    
    def test_auto_mode_with_ema(self):
        """Test auto mode with EMA smoothing."""
        miner_stats = [
            MinerWindowStats(sales=20, revenue_usd=2000.0, refund_orders=0),
        ]
        
        prev = Percentiles(p95_sales=10.0, p95_revenue_usd=1000.0)
        config = P95Config(
            mode=P95Mode.AUTO,
            ema_alpha=0.5,
            scope="network"
        )
        provider = AutoP95Provider(miner_stats, config)
        provider.prev = prev
        
        p95 = provider.get_effective_p95("network")
        
        # Raw P95 would be 20, but EMA with alpha=0.5: 0.5*20 + 0.5*10 = 15
        from bitads_v3_core.domain.percentiles import ema
        expected_sales = ema(10.0, 20.0, 0.5)
        self.assertAlmostEqual(p95.p95_sales, expected_sales, delta=TOLERANCE)
    
    def test_auto_mode_with_flooring_flag(self):
        """Test that flooring is only applied when flag is True."""
        miner_stats = [
            MinerWindowStats(sales=1, revenue_usd=100.0, refund_orders=0),
            MinerWindowStats(sales=2, revenue_usd=200.0, refund_orders=0),
        ]
        
        config = P95Config(mode=P95Mode.AUTO, scope="network")
        
        # Without flooring
        provider_no_floor = AutoP95Provider(miner_stats, config)
        p95_no_floor = provider_no_floor.get_effective_p95("network")
        
        # With flooring
        provider_with_floor = AutoP95Provider(miner_stats, config)
        provider_with_floor.use_flooring = True
        p95_with_floor = provider_with_floor.get_effective_p95("network")
        
        # With flooring, P95 should be >= without flooring
        self.assertGreaterEqual(p95_with_floor.p95_sales, p95_no_floor.p95_sales)
        self.assertGreaterEqual(p95_with_floor.p95_revenue_usd, p95_no_floor.p95_revenue_usd)
    
    def test_manual_mode_validation(self):
        """Test that manual mode requires manual values."""
        # Should raise error if manual values are None
        with self.assertRaises(ValueError):
            P95Config(
                mode=P95Mode.MANUAL,
                manual_p95_sales=None,
                manual_p95_revenue_usd=4000.0
            )
        
        with self.assertRaises(ValueError):
            P95Config(
                mode=P95Mode.MANUAL,
                manual_p95_sales=60.0,
                manual_p95_revenue_usd=None
            )
    
    def test_auto_mode_works_without_ema(self):
        """Test that auto mode works without EMA (alpha=None)."""
        miner_stats = [
            MinerWindowStats(sales=10, revenue_usd=1000.0, refund_orders=0),
            MinerWindowStats(sales=20, revenue_usd=2000.0, refund_orders=1),
        ]
        
        config = P95Config(mode=P95Mode.AUTO, scope="network")
        provider = AutoP95Provider(miner_stats, config)
        
        p95 = provider.get_effective_p95("network")
        # Should compute directly without EMA
        self.assertEqual(p95.p95_sales, 20.0)
        self.assertEqual(p95.p95_revenue_usd, 2000.0)


if __name__ == "__main__":
    unittest.main()


