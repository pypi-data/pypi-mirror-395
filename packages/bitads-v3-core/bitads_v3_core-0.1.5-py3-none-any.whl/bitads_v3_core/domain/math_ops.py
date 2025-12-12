"""
Pure mathematical operations for miner scoring.

All functions are deterministic and side-effect-free.
"""
import math
from typing import Optional

from .models import MinerWindowStats

# Constants
W_SALES = 0.15  # Weight for sales normalization in base score
W_REV = 0.85  # Weight for revenue normalization in base score
EPS = 1e-9  # Epsilon for numerical stability
SOFT_CAP_THRESHOLD = 3  # Sales threshold for soft cap application
SOFT_CAP_FACTOR = 0.30  # Multiplier for low sales


def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Clamp a value to [min_val, max_val].
    
    Args:
        value: The value to clamp
        min_val: Minimum value (default 0.0)
        max_val: Maximum value (default 1.0)
    
    Returns:
        Clamped value in [min_val, max_val]
    """
    return max(min_val, min(max_val, value))


def refund_rate(stats: MinerWindowStats) -> float:
    """
    Compute refund rate from miner statistics.
    
    Formula: min(1, refund_orders / max(1, sales))
    
    Args:
        stats: Miner window statistics
    
    Returns:
        Refund rate in [0,1]
    """
    if stats.sales == 0:
        return 0.0
    rate = stats.refund_orders / max(1, stats.sales)
    return clamp(rate, 0.0, 1.0)


def normalize_sales(sales: float, p95_sales: float, eps: float = EPS) -> float:
    """
    Normalize sales value using square root transformation.
    
    Formula: min(1, sqrt(sales) / max(sqrt(p95_sales), eps))
    
    Args:
        sales: Sales count (can be int or float)
        p95_sales: P95 sales percentile
        eps: Epsilon for numerical stability (default EPS)
    
    Returns:
        Normalized sales value in [0,1]
    """
    if sales < 0:
        raise ValueError(f"sales must be >= 0, got {sales}")
    if p95_sales < 0:
        raise ValueError(f"p95_sales must be >= 0, got {p95_sales}")
    
    sqrt_sales = math.sqrt(sales)
    sqrt_p95 = math.sqrt(p95_sales)
    denominator = max(sqrt_p95, eps)
    
    normalized = sqrt_sales / denominator
    return clamp(normalized, 0.0, 1.0)


def normalize_revenue(rev: float, p95_rev: float, eps: float = EPS) -> float:
    """
    Normalize revenue value using logarithmic transformation.
    
    Formula: min(1, ln(1+rev) / max(ln(1+p95_rev), eps))
    
    Args:
        rev: Revenue in USD
        p95_rev: P95 revenue percentile in USD
        eps: Epsilon for numerical stability (default EPS)
    
    Returns:
        Normalized revenue value in [0,1]
    """
    if rev < 0:
        raise ValueError(f"rev must be >= 0, got {rev}")
    if p95_rev < 0:
        raise ValueError(f"p95_rev must be >= 0, got {p95_rev}")
    
    log_rev = math.log1p(rev)  # ln(1 + rev)
    log_p95 = math.log1p(p95_rev)  # ln(1 + p95_rev)
    denominator = max(log_p95, eps)
    
    normalized = log_rev / denominator
    return clamp(normalized, 0.0, 1.0)


def base_score(sales_norm: float, rev_norm: float, w_sales: float = W_SALES, w_rev: float = W_REV) -> float:
    """
    Compute base score from normalized sales and revenue.
    
    Formula: w_sales * sales_norm + w_rev * rev_norm
    
    Args:
        sales_norm: Normalized sales value in [0,1]
        rev_norm: Normalized revenue value in [0,1]
        w_sales: Weight for sales (default W_SALES=0.15)
        w_rev: Weight for revenue (default W_REV=0.85)
    
    Returns:
        Base score in [0,1]
    """
    if not (0 <= sales_norm <= 1):
        raise ValueError(f"sales_norm must be in [0,1], got {sales_norm}")
    if not (0 <= rev_norm <= 1):
        raise ValueError(f"rev_norm must be in [0,1], got {rev_norm}")
    
    score = w_sales * sales_norm + w_rev * rev_norm
    return clamp(score, 0.0, 1.0)


def final_score(base: float, ref_rate: float) -> float:
    """
    Compute final score from base score and refund rate.
    
    Formula: (1 - ref_rate) * base, clamped to [0,1]
    
    Args:
        base: Base score in [0,1]
        ref_rate: Refund rate in [0,1]
    
    Returns:
        Final score in [0,1]
    """
    if not (0 <= base <= 1):
        raise ValueError(f"base must be in [0,1], got {base}")
    if not (0 <= ref_rate <= 1):
        raise ValueError(f"ref_rate must be in [0,1], got {ref_rate}")
    
    score = (1.0 - ref_rate) * base
    return clamp(score, 0.0, 1.0)


def apply_early_sales_soft_cap(score: float, sales: int, threshold: int = 3, factor: float = 0.30) -> float:
    """
    Apply soft cap to score for miners with low sales count.
    
    If sales < threshold, multiply score by factor.
    
    Args:
        score: Current score in [0,1]
        sales: Sales count
        threshold: Sales threshold (default 3)
        factor: Multiplier for low sales (default 0.30)
    
    Returns:
        Adjusted score in [0,1]
    """
    if not (0 <= score <= 1):
        raise ValueError(f"score must be in [0,1], got {score}")
    if sales < 0:
        raise ValueError(f"sales must be >= 0, got {sales}")
    
    if sales < threshold:
        score = score * factor
    
    return clamp(score, 0.0, 1.0)


