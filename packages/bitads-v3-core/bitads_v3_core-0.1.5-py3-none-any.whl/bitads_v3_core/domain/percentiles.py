"""
Pure percentile computation functions.

All functions are deterministic and side-effect-free.
"""
import math
from typing import List, Optional

from .models import MinerWindowStats, Percentiles


def percentile(values: List[float], p: float) -> float:
    """
    Compute percentile value from a list of values.
    
    P95 = value at index ceil(0.95 * N) using ascending sort, 1-indexed.
    
    Args:
        values: List of numeric values
        p: Percentile value in [0,1] (e.g., 0.95 for P95)
    
    Returns:
        Percentile value
    
    Raises:
        ValueError: If values list is empty or p is not in [0,1]
    """
    if not values:
        raise ValueError("values list cannot be empty")
    if not (0 <= p <= 1):
        raise ValueError(f"p must be in [0,1], got {p}")
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    # 1-indexed: ceil(0.95 * N) means index = ceil(0.95 * N) - 1 (0-indexed)
    # But we want the value at position ceil(0.95 * N) in 1-indexed terms
    # So 0-indexed position is ceil(p * n) - 1, but we need to handle edge cases
    index_1_indexed = math.ceil(p * n)
    # Convert to 0-indexed (subtract 1), but ensure we don't go below 0
    index_0_indexed = max(0, min(index_1_indexed - 1, n - 1))
    
    return sorted_values[index_0_indexed]


def ema(prev: float, obs: float, alpha: float) -> float:
    """
    Compute Exponential Moving Average (EMA).
    
    Formula: alpha * obs + (1 - alpha) * prev
    
    Args:
        prev: Previous EMA value
        obs: Current observation
        alpha: Smoothing factor in [0,1]
    
    Returns:
        Updated EMA value
    """
    if not (0 <= alpha <= 1):
        raise ValueError(f"alpha must be in [0,1], got {alpha}")
    
    return alpha * obs + (1.0 - alpha) * prev


def compute_auto_p95(
    miner_stats: List[MinerWindowStats],
    prev: Optional[Percentiles] = None,
    alpha: Optional[float] = None,
    use_flooring: bool = False
) -> Percentiles:
    """
    Compute P95 percentiles from miner statistics.
    
    If prev and alpha are provided, applies EMA smoothing.
    If use_flooring is True, applies normalization floors:
    - max(sqrt(P95_sales), sqrt(5))
    - max(ln(1+P95_rev), ln(1+300))
    
    Args:
        miner_stats: List of miner statistics
        prev: Previous Percentiles for EMA (optional)
        alpha: EMA smoothing factor (optional, required if prev is provided)
        use_flooring: Whether to apply normalization floors (default False)
    
    Returns:
        Percentiles with p95_sales and p95_revenue_usd
    
    Raises:
        ValueError: If prev is provided but alpha is not when computing from stats, or if alpha is not in [0,1]
    """
    if alpha is not None and not (0 <= alpha <= 1):
        raise ValueError(f"alpha must be in [0,1], got {alpha}")
    
    if not miner_stats:
        # If no stats and no prev, return zeros
        if prev is None:
            return Percentiles(p95_sales=0.0, p95_revenue_usd=0.0)
        # If no stats but prev exists, return prev (no update, no alpha needed)
        return prev
    
    # If we have stats and prev is provided, alpha is required for EMA
    if prev is not None and alpha is None:
        raise ValueError("alpha must be provided when prev is provided and computing from stats")
    
    # Extract sales and revenue values
    sales_values = [stats.sales for stats in miner_stats]
    revenue_values = [stats.revenue_usd for stats in miner_stats]
    
    # Compute current P95 values
    p95_sales_raw = percentile(sales_values, 0.95)
    p95_revenue_raw = percentile(revenue_values, 0.95)
    
    # Apply flooring if requested
    # Flooring ensures: sqrt(P95_sales) >= sqrt(5) and ln(1+P95_rev) >= ln(1+300)
    # This means: P95_sales >= 5 and P95_revenue >= 300
    if use_flooring:
        p95_sales_raw = max(p95_sales_raw, 5.0)
        p95_revenue_raw = max(p95_revenue_raw, 300.0)
    
    # Apply EMA smoothing if prev and alpha are provided
    if prev is not None and alpha is not None:
        p95_sales = ema(prev.p95_sales, p95_sales_raw, alpha)
        p95_revenue = ema(prev.p95_revenue_usd, p95_revenue_raw, alpha)
    else:
        p95_sales = p95_sales_raw
        p95_revenue = p95_revenue_raw
    
    return Percentiles(p95_sales=p95_sales, p95_revenue_usd=p95_revenue)

