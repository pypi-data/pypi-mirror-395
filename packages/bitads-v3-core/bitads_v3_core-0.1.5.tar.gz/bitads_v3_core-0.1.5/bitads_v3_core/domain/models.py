"""
Domain models for BitAds Miner Scoring.

All models are pure data classes with no side effects.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class P95Mode(str, Enum):
    """Enumeration for P95 computation mode."""
    MANUAL = "manual"
    AUTO = "auto"


@dataclass(frozen=True)
class MinerWindowStats:
    """Statistics for a miner over a rolling window (e.g., 30 days)."""
    sales: int  # >= 0
    revenue_usd: float  # >= 0
    refund_orders: int  # >= 0

    def __post_init__(self):
        """Validate that all values are non-negative."""
        if self.sales < 0:
            raise ValueError(f"sales must be >= 0, got {self.sales}")
        if self.revenue_usd < 0:
            raise ValueError(f"revenue_usd must be >= 0, got {self.revenue_usd}")
        if self.refund_orders < 0:
            raise ValueError(f"refund_orders must be >= 0, got {self.refund_orders}")


@dataclass(frozen=True)
class Percentiles:
    """P95 percentiles for sales and revenue."""
    p95_sales: float  # >= 0
    p95_revenue_usd: float  # >= 0

    def __post_init__(self):
        """Validate that all values are non-negative."""
        if self.p95_sales < 0:
            raise ValueError(f"p95_sales must be >= 0, got {self.p95_sales}")
        if self.p95_revenue_usd < 0:
            raise ValueError(f"p95_revenue_usd must be >= 0, got {self.p95_revenue_usd}")


@dataclass(frozen=True)
class ScoreResult:
    """Result of scoring a single miner."""
    miner_id: str  # Opaque identifier
    base: float  # Base score in [0,1]
    refund_multiplier: float  # Refund multiplier in [0,1]
    score: float  # Final score in [0,1]

    def __post_init__(self):
        """Validate that all values are in [0,1]."""
        if not (0 <= self.base <= 1):
            raise ValueError(f"base must be in [0,1], got {self.base}")
        if not (0 <= self.refund_multiplier <= 1):
            raise ValueError(f"refund_multiplier must be in [0,1], got {self.refund_multiplier}")
        if not (0 <= self.score <= 1):
            raise ValueError(f"score must be in [0,1], got {self.score}")


@dataclass(frozen=True)
class P95Config:
    """Configuration for P95 computation mode and parameters."""
    mode: P95Mode
    manual_p95_sales: Optional[float] = None  # Required if mode == MANUAL
    manual_p95_revenue_usd: Optional[float] = None  # Required if mode == MANUAL
    ema_alpha: Optional[float] = None  # Optional EMA smoothing factor in [0,1] for AUTO mode
    scope: str = "network"  # Opaque scope identifier (e.g., "network", "campaign:123")

    def __post_init__(self):
        """Validate configuration based on mode."""
        if self.mode == P95Mode.MANUAL:
            if self.manual_p95_sales is None or self.manual_p95_sales < 0:
                raise ValueError(f"manual_p95_sales must be >= 0 for MANUAL mode, got {self.manual_p95_sales}")
            if self.manual_p95_revenue_usd is None or self.manual_p95_revenue_usd < 0:
                raise ValueError(f"manual_p95_revenue_usd must be >= 0 for MANUAL mode, got {self.manual_p95_revenue_usd}")
        if self.ema_alpha is not None:
            if not (0 <= self.ema_alpha <= 1):
                raise ValueError(f"ema_alpha must be in [0,1], got {self.ema_alpha}")


