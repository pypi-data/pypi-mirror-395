# BitAds Miner Scoring Core

A minimal, testable core for computing BitAds Miner Scores in the range [0,1] for each miner over a rolling last 30 days window. The core is pure, deterministic, and unit-testable with no external dependencies (no SDKs, HTTP, DB, cloud, or blockchain code).

## Architecture

The codebase follows a clean architecture with clear separation of concerns:

- **Domain Layer** (`domain/`): Pure business logic and data models
- **Application Layer** (`app/`): Application services and port interfaces
- **Tests** (`tests/`): Comprehensive unit tests

## Public APIs

### Domain Models

#### `MinerWindowStats`
Statistics for a miner over a rolling window (e.g., 30 days):
- `sales: int >= 0` - Number of sales
- `revenue_usd: float >= 0` - Revenue in USD
- `refund_orders: int >= 0` - Number of refund orders

#### `Percentiles`
P95 percentiles for sales and revenue:
- `p95_sales: float >= 0` - 95th percentile of sales
- `p95_revenue_usd: float >= 0` - 95th percentile of revenue

#### `ScoreResult`
Result of scoring a single miner:
- `miner_id: str` - Opaque miner identifier
- `base: float in [0,1]` - Base score before refund multiplier
- `refund_multiplier: float in [0,1]` - Multiplier from refund rate
- `score: float in [0,1]` - Final score

#### `P95Mode` (Enum)
- `MANUAL` - Use manually configured P95 values
- `AUTO` - Compute P95 from miner statistics

#### `P95Config`
Configuration for P95 computation:
- `mode: P95Mode` - Computation mode
- `manual_p95_sales: Optional[float]` - Required if mode == MANUAL
- `manual_p95_revenue_usd: Optional[float]` - Required if mode == MANUAL
- `ema_alpha: Optional[float] in [0,1]` - EMA smoothing factor for AUTO mode
- `scope: str` - Opaque scope identifier (e.g., "network", "campaign:123")

### Pure Functions

All functions are in `domain/math_ops.py` and `domain/percentiles.py`:

#### `refund_rate(stats: MinerWindowStats) -> float`
Computes refund rate: `min(1, refund_orders / max(1, sales))`

#### `normalize_sales(sales: float, p95_sales: float, eps=1e-9) -> float`
Normalizes sales using square root: `min(1, sqrt(sales) / max(sqrt(p95_sales), eps))`

#### `normalize_revenue(rev: float, p95_rev: float, eps=1e-9) -> float`
Normalizes revenue using logarithm: `min(1, ln(1+rev) / max(ln(1+p95_rev), eps))`

#### `base_score(sales_norm: float, rev_norm: float, w_sales=0.15, w_rev=0.85) -> float`
Computes base score: `w_sales * sales_norm + w_rev * rev_norm`

#### `final_score(base: float, ref_rate: float) -> float`
Computes final score: `(1 - ref_rate) * base`, clamped to [0,1]

#### `apply_early_sales_soft_cap(score: float, sales: int, threshold=3, factor=0.30) -> float`
Applies soft cap for low sales: if `sales < threshold`, multiply score by `factor`

#### `percentile(values: List[float], p: float) -> float`
Computes percentile value. P95 = value at index `ceil(0.95 * N)` using ascending sort, 1-indexed.

#### `ema(prev: float, obs: float, alpha: float) -> float`
Computes Exponential Moving Average: `alpha * obs + (1 - alpha) * prev`

#### `compute_auto_p95(miner_stats: List[MinerWindowStats], prev: Optional[Percentiles], alpha: Optional[float], use_flooring: bool) -> Percentiles`
Computes P95 percentiles from miner statistics. If `use_flooring=True`, applies floors:
- `max(P95_sales, 5.0)`
- `max(P95_revenue, 300.0)`

### Application Service

#### `ScoreCalculator`
Main service for computing miner scores.

**Constructor:**
```python
ScoreCalculator(
    p95_provider: IP95Provider,
    use_soft_cap: bool = False,
    use_flooring: bool = False
)
```

**Methods:**
- `score_one(miner_id: str, stats: MinerWindowStats, scope: str) -> ScoreResult`
- `score_many(entries: List[Tuple[str, MinerWindowStats]], scope: str) -> List[ScoreResult]`

### Port Interfaces

All interfaces are in `app/ports.py`:

- **`IP95Provider`**: Provides P95 percentiles for a given scope
- **`IMinerStatsSource`**: Fetches miner statistics from a data source
- **`IScoreSink`**: Publishes score results
- **`IConfigSource`**: Fetches P95 configuration

These are abstract interfaces for future adapters. No concrete implementations are provided in this core module.

## Formulas

### Scoring Algorithm

1. **Refund Rate**: `ref_rate = min(1, refund_orders / max(1, sales))`
2. **Sales Normalization**: `sales_norm = min(1, sqrt(sales) / max(sqrt(p95_sales), eps))`
3. **Revenue Normalization**: `rev_norm = min(1, ln(1+rev) / max(ln(1+p95_rev), eps))`
4. **Base Score**: `base = 0.15 * sales_norm + 0.85 * rev_norm`
5. **Final Score**: `score = (1 - ref_rate) * base`
6. **Soft Cap** (if enabled): If `sales < 3`, multiply score by `0.30`

### Constants

- `W_SALES = 0.15` - Weight for sales in base score
- `W_REV = 0.85` - Weight for revenue in base score
- `EPS = 1e-9` - Epsilon for numerical stability

## Feature Flags

- **`use_soft_cap`**: When `True`, applies 0.30 multiplier to scores for miners with `sales < 3`
- **`use_flooring`**: When `True`, applies normalization floors to auto-computed P95 values:
  - `P95_sales >= 5.0`
  - `P95_revenue >= 300.0`

## Running Unit Tests

### Using pytest (recommended):
```bash
# Navigate to the package directory
cd bitads_v3_core

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_examples.py -v

# Run with coverage
python -m pytest tests/ --cov=bitads_v3_core --cov-report=html
```

### Using unittest:
```bash
python -m unittest discover tests -v
```

## Test Coverage

The test suite includes:

1. **Example Tests** (`test_examples.py`):
   - Example A: Network P95s, Miner with sales=48, rev=2300, refunds=6 → score ≈ 0.802
   - Example B: Same P95s, Miner with sales=10, rev=3000, refunds=1 → score ≈ 0.668
   - Example C: Zero sales → score = 0

2. **Edge Cases** (`test_edges.py`):
   - Zero P95s
   - High refunds (refund_orders > sales)
   - Early-sales soft cap
   - Clamping to [0,1]
   - Zero sales/revenue

3. **Percentile Tests** (`test_percentiles.py`):
   - Percentile computation correctness
   - EMA behavior with various alpha values
   - Auto P95 computation with/without EMA
   - Flooring behavior

4. **Mode Tests** (`test_modes.py`):
   - Manual mode returns constants
   - Auto mode computes from stats
   - EMA smoothing in auto mode
   - Flooring flag behavior

## Numeric Tolerances

All tests use a tolerance of **1e-6** for floating-point comparisons:

```python
TOLERANCE = 1e-6
self.assertAlmostEqual(actual, expected, delta=TOLERANCE)
```

## Numerical Guarantees

- Every public API clamps outputs to [0,1]
- All math functions are total/defined (use `eps=1e-9` guards)
- No floating-point NaNs/inf leak through public interfaces
- All domain models validate inputs and enforce invariants

## Example Usage

```python
from bitads_v3_core.domain.models import MinerWindowStats, Percentiles
from bitads_v3_core.app.scoring import ScoreCalculator
from bitads_v3_core.app.ports import IP95Provider

# Create a simple P95 provider (manual mode)
class SimpleP95Provider(IP95Provider):
    """Simple provider that returns fixed percentiles."""
    def __init__(self, percentiles: Percentiles):
        self.percentiles = percentiles
    
    def get_effective_p95(self, scope: str) -> Percentiles:
        return self.percentiles

# Set up P95 provider with fixed percentiles
percentiles = Percentiles(p95_sales=60.0, p95_revenue_usd=4000.0)
provider = SimpleP95Provider(percentiles)

# Create calculator
calculator = ScoreCalculator(provider, use_soft_cap=False)

# Score a miner
stats = MinerWindowStats(sales=48, revenue_usd=2300.0, refund_orders=6)
result = calculator.score_one("miner_123", stats, "network")

print(f"Miner: {result.miner_id}")
print(f"Base Score: {result.base:.3f}")
print(f"Refund Multiplier: {result.refund_multiplier:.3f}")
print(f"Final Score: {result.score:.3f}")
```

### Installation

```bash
pip install bitads-v3-core
```

### Alternative: Using with Test Helpers

If you're working within the project and want to use the test helpers:

```python
import sys
from pathlib import Path

# Add project root to path (only needed in development)
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from bitads_v3_core.domain.models import MinerWindowStats, Percentiles
from bitads_v3_core.app.scoring import ScoreCalculator
from tests.test_helpers import MockP95Provider

# Use MockP95Provider from tests
percentiles = Percentiles(p95_sales=60.0, p95_revenue_usd=4000.0)
provider = MockP95Provider(percentiles)
calculator = ScoreCalculator(provider)

stats = MinerWindowStats(sales=48, revenue_usd=2300.0, refund_orders=6)
result = calculator.score_one("miner_123", stats, "network")
```

## Project Structure

```
bitads_v3_core/                    # Project root
├── pyproject.toml                 # Package configuration
├── README.md
├── MANIFEST.in
├── bitads_v3_core/                # Package root
│   ├── __init__.py                # Package initialization (version)
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py              # Domain models
│   │   ├── math_ops.py            # Pure math functions
│   │   └── percentiles.py         # Percentile computation
│   └── app/
│       ├── __init__.py
│       ├── ports.py               # Port interfaces
│       └── scoring.py             # ScoreCalculator service
└── tests/
    ├── __init__.py
    ├── conftest.py                # Pytest configuration
    ├── test_helpers.py            # Mock implementations
    ├── test_examples.py           # Example test cases
    ├── test_edges.py              # Edge case tests
    ├── test_percentiles.py        # Percentile tests
    └── test_modes.py              # Mode behavior tests
```

## Dependencies

This core module has **no external dependencies** beyond Python standard library:
- `dataclasses` (Python 3.7+)
- `enum` (standard library)
- `typing` (standard library)
- `math` (standard library)
- `unittest` (standard library, for tests)

## License

This is a core domain module for BitAds Miner Scoring. No external coupling, SDKs, or infrastructure code.


