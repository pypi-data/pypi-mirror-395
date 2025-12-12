"""
Port interfaces (protocols) for external adapters.

These are abstract interfaces that define contracts for future implementations.
No concrete implementations are provided in this core module.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple

from ..domain.models import MinerWindowStats, Percentiles, ScoreResult, P95Config


class IP95Provider(ABC):
    """Interface for providing P95 percentiles for a given scope."""
    
    @abstractmethod
    def get_effective_p95(self, scope: str) -> Percentiles:
        """
        Get effective P95 percentiles for the given scope.
        
        Args:
            scope: Opaque scope identifier (e.g., "network", "campaign:123")
        
        Returns:
            Percentiles with p95_sales and p95_revenue_usd
        """
        pass


class IMinerStatsSource(ABC):
    """Interface for fetching miner statistics from a data source."""
    
    @abstractmethod
    def fetch_window(self, scope: str, window_days: int = 30) -> List[Tuple[str, MinerWindowStats]]:
        """
        Fetch miner statistics for a rolling window.
        
        Args:
            scope: Opaque scope identifier
            window_days: Number of days for the rolling window (default 30)
        
        Returns:
            List of (miner_id, MinerWindowStats) tuples
        """
        pass


class IScoreSink(ABC):
    """Interface for publishing score results."""
    
    @abstractmethod
    def publish(self, scores: List[ScoreResult], scope: str) -> None:
        """
        Publish score results to a destination.
        
        Args:
            scores: List of score results
            scope: Opaque scope identifier
        """
        pass


class IConfigSource(ABC):
    """Interface for fetching P95 configuration."""
    
    @abstractmethod
    def get_p95_config(self, scope: str) -> P95Config:
        """
        Get P95 configuration for the given scope.
        
        Args:
            scope: Opaque scope identifier
        
        Returns:
            P95Config with mode and parameters
        """
        pass


