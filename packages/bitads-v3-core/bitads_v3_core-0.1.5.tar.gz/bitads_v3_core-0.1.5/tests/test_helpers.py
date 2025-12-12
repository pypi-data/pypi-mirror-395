"""
Test helpers including mock implementations of port interfaces.
"""
from typing import List

from bitads_v3_core.domain.models import Percentiles, P95Config, P95Mode
from bitads_v3_core.app.ports import IP95Provider


class MockP95Provider(IP95Provider):
    """Mock implementation of IP95Provider for testing."""
    
    def __init__(self, percentiles: Percentiles):
        """
        Initialize with fixed percentiles.
        
        Args:
            percentiles: Fixed Percentiles to return
        """
        self.percentiles = percentiles
    
    def get_effective_p95(self, scope: str) -> Percentiles:
        """Return the fixed percentiles regardless of scope."""
        return self.percentiles


