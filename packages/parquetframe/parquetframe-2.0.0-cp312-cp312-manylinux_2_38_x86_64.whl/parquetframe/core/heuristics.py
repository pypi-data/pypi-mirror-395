"""
Engine selection heuristics for intelligent DataFrame backend choice.

Implements the decision logic for automatically selecting the optimal DataFrame
engine based on data size, operation type, system resources, and user preferences.
"""

import logging

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

from ..config import get_config
from .base import Engine, EngineCapabilities

logger = logging.getLogger(__name__)


class EngineHeuristics:
    """Intelligent engine selection based on data characteristics and system resources."""

    def __init__(self):
        # Load thresholds from config
        config = get_config()
        self.pandas_threshold_bytes = int(config.pandas_threshold_mb * 1024 * 1024)
        self.dask_threshold_bytes = int(config.polars_threshold_mb * 1024 * 1024)

        # Memory considerations
        self.memory_safety_factor = 0.8  # Use 80% of available memory

    def select_engine(
        self,
        engines: dict[str, Engine],
        capabilities: dict[str, EngineCapabilities],
        data_size_bytes: int = 0,
        operation_type: str | None = None,
        prefer_lazy: bool | None = None,
    ) -> str:
        """
        Select optimal engine based on multiple factors.

        Args:
            engines: Available engines
            capabilities: Engine capabilities
            data_size_bytes: Estimated data size
            operation_type: Type of operation
            prefer_lazy: User preference for lazy evaluation

        Returns:
            Selected engine name
        """
        if not engines:
            raise ValueError("No engines available")

        # Check for config override
        config = get_config()
        if config.default_engine and config.default_engine in engines:
            if engines[config.default_engine].is_available:
                logger.debug(
                    f"Using configured default engine: {config.default_engine}"
                )
                return config.default_engine

        # Get system information
        available_memory = self._get_available_memory()

        # Score each available engine
        scores = {}
        for name, engine in engines.items():
            if not engine.is_available:
                continue

            caps = capabilities.get(name)
            if not caps:
                continue

            score = self._calculate_engine_score(
                engine_name=name,
                capabilities=caps,
                data_size_bytes=data_size_bytes,
                available_memory=available_memory,
                operation_type=operation_type,
                prefer_lazy=prefer_lazy,
            )

            scores[name] = score
            logger.debug(f"Engine {name} score: {score:.3f}")

        if not scores:
            # Fallback to first available engine
            for name, engine in engines.items():
                if engine.is_available:
                    logger.warning(f"No engines scored, falling back to {name}")
                    return name
            raise RuntimeError("No available engines found")

        # Return highest scoring engine
        selected = max(scores, key=lambda k: scores[k])
        logger.debug(f"Selected engine: {selected} (score: {scores[selected]:.3f})")
        return selected

    def _calculate_engine_score(
        self,
        engine_name: str,
        capabilities: EngineCapabilities,
        data_size_bytes: int,
        available_memory: int,
        operation_type: str | None,
        prefer_lazy: bool | None,
    ) -> float:
        """Calculate score for an engine based on various factors."""
        score = 0.0

        # 1. Size-based scoring (40% of total score)
        size_score = self._score_by_size(capabilities, data_size_bytes)
        score += size_score * 0.4

        # 2. Memory efficiency (25% of total score)
        memory_score = self._score_by_memory(
            capabilities, data_size_bytes, available_memory
        )
        score += memory_score * 0.25

        # 3. Performance characteristics (20% of total score)
        performance_score = capabilities.performance_score
        score += (performance_score / 2.0) * 0.2  # Normalize to 0-1 range

        # 4. Lazy evaluation preference (10% of total score)
        lazy_score = self._score_by_lazy_preference(capabilities, prefer_lazy)
        score += lazy_score * 0.1

        # 5. Operation-specific scoring (5% of total score)
        operation_score = self._score_by_operation(capabilities, operation_type)
        score += operation_score * 0.05

        return score

    def _score_by_size(
        self, capabilities: EngineCapabilities, data_size_bytes: int
    ) -> float:
        """Score engine based on data size fit."""
        min_size, max_size = capabilities.optimal_size_range

        if min_size <= data_size_bytes <= max_size:
            return 1.0  # Perfect fit
        elif data_size_bytes < min_size:
            # Penalize oversized engines for small data
            ratio = data_size_bytes / min_size if min_size > 0 else 1.0
            return max(0.3, ratio)  # Minimum score of 0.3
        else:
            # Penalize undersized engines for large data
            ratio = max_size / data_size_bytes if data_size_bytes > 0 else 1.0
            return max(0.1, ratio)  # Minimum score of 0.1

    def _score_by_memory(
        self,
        capabilities: EngineCapabilities,
        data_size_bytes: int,
        available_memory: int,
    ) -> float:
        """Score engine based on memory efficiency."""
        if available_memory <= 0:
            return 0.5  # Neutral score if memory info unavailable

        # Estimate memory usage considering engine efficiency
        estimated_usage = data_size_bytes / capabilities.memory_efficiency
        memory_ratio = estimated_usage / (available_memory * self.memory_safety_factor)

        if memory_ratio <= 0.5:
            return 1.0  # Excellent memory fit
        elif memory_ratio <= 1.0:
            return 1.0 - (memory_ratio - 0.5) * 2  # Linear decrease
        else:
            return max(0.1, 1.0 / memory_ratio)  # Penalize heavily for memory overflow

    def _score_by_lazy_preference(
        self, capabilities: EngineCapabilities, prefer_lazy: bool | None
    ) -> float:
        """Score based on lazy evaluation preference."""
        if prefer_lazy is None:
            return 0.5  # Neutral

        if prefer_lazy == capabilities.is_lazy:
            return 1.0  # Perfect match
        else:
            return 0.2  # Penalty for mismatch

    def _score_by_operation(
        self, capabilities: EngineCapabilities, operation_type: str | None
    ) -> float:
        """Score based on operation type (future extensibility)."""
        # Currently neutral, but can be extended for operation-specific preferences
        return 0.5

    def _get_available_memory(self) -> int:
        """Get available system memory in bytes."""
        if not HAS_PSUTIL:
            # Conservative fallback: assume 4GB available
            # This ensures core functionality works without psutil
            logger.debug("psutil not available, using 4GB conservative fallback")
            return 4 * 1024 * 1024 * 1024  # 4GB in bytes
        try:
            memory = psutil.virtual_memory()
            return memory.available
        except Exception as e:
            logger.warning(f"Could not get memory info: {e}")
            return 0

    def configure_thresholds(
        self, pandas_threshold_mb: int, dask_threshold_mb: int
    ) -> None:
        """Configure size thresholds for engine selection."""
        self.pandas_threshold_bytes = pandas_threshold_mb * 1024 * 1024
        self.dask_threshold_bytes = dask_threshold_mb * 1024 * 1024
        logger.info(
            f"Updated thresholds: pandas<{pandas_threshold_mb}MB, dask>{dask_threshold_mb}MB"
        )
