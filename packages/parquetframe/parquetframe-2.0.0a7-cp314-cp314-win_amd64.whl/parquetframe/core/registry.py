"""
Engine registry for managing and selecting DataFrame engines.

Provides centralized registration and selection of available DataFrame engines
with intelligent selection based on data characteristics and system resources.
"""

import logging
import os

from .base import Engine, EngineCapabilities
from .heuristics import EngineHeuristics

logger = logging.getLogger(__name__)


class EngineRegistry:
    """Registry for DataFrame engines with intelligent selection."""

    def __init__(self):
        self._engines: dict[str, Engine] = {}
        self._capabilities: dict[str, EngineCapabilities] = {}
        self._heuristics = EngineHeuristics()
        self._default_engine = "auto"

        # Register available engines
        self._register_default_engines()

    def register_engine(self, engine: Engine, capabilities: EngineCapabilities) -> None:
        """
        Register a DataFrame engine.

        Args:
            engine: Engine instance
            capabilities: Engine capabilities description
        """
        if not engine.is_available:
            logger.warning(
                f"Engine {engine.name} is not available (library not installed)"
            )
            return

        self._engines[engine.name] = engine
        self._capabilities[engine.name] = capabilities
        logger.debug(f"Registered engine: {engine.name}")

    def get_engine(self, name: str) -> Engine:
        """
        Get engine by name.

        Args:
            name: Engine name

        Returns:
            Engine instance

        Raises:
            KeyError: If engine not found
        """
        if name == "auto":
            return self.select_optimal_engine()

        if name not in self._engines:
            available = list(self._engines.keys())
            raise KeyError(f"Engine '{name}' not found. Available: {available}")

        return self._engines[name]

    def list_engines(self) -> list[str]:
        """List available engine names."""
        return list(self._engines.keys())

    def get_capabilities(self, name: str) -> EngineCapabilities:
        """Get engine capabilities."""
        if name not in self._capabilities:
            raise KeyError(f"No capabilities found for engine: {name}")
        return self._capabilities[name]

    def select_optimal_engine(
        self,
        data_size_bytes: int = 0,
        operation_type: str | None = None,
        prefer_lazy: bool | None = None,
    ) -> Engine:
        """
        Select optimal engine based on data characteristics.

        Args:
            data_size_bytes: Estimated data size in bytes
            operation_type: Type of operation ('read', 'compute', 'transform')
            prefer_lazy: Preference for lazy evaluation

        Returns:
            Selected Engine instance
        """
        # Check for environment override
        env_engine = os.environ.get("PARQUETFRAME_ENGINE")
        if env_engine and env_engine in self._engines:
            logger.debug(f"Using engine from environment: {env_engine}")
            return self._engines[env_engine]

        # Use heuristics for selection
        selected_name = self._heuristics.select_engine(
            engines=self._engines,
            capabilities=self._capabilities,
            data_size_bytes=data_size_bytes,
            operation_type=operation_type,
            prefer_lazy=prefer_lazy,
        )

        logger.debug(f"Selected engine: {selected_name} for {data_size_bytes} bytes")
        return self._engines[selected_name]

    def _register_default_engines(self) -> None:
        """Register default engines (pandas, polars, dask)."""
        # Import engines here to avoid circular imports
        try:
            from ..engines.pandas_engine import PandasEngine

            pandas_engine = PandasEngine()
            pandas_caps = EngineCapabilities(
                name="pandas",
                is_lazy=False,
                supports_distributed=False,
                optimal_size_range=(0, 1024 * 1024 * 1024),  # 0 - 1GB
                memory_efficiency=1.0,
                performance_score=1.0,
            )
            self.register_engine(pandas_engine, pandas_caps)
        except ImportError:
            logger.debug("Pandas engine not available")

        try:
            from ..engines.polars_engine import PolarsEngine

            polars_engine = PolarsEngine()
            polars_caps = EngineCapabilities(
                name="polars",
                is_lazy=True,
                supports_distributed=False,
                optimal_size_range=(
                    1024 * 1024 * 100,
                    1024 * 1024 * 1024 * 100,
                ),  # 100MB - 100GB
                memory_efficiency=1.5,
                performance_score=2.0,
            )
            self.register_engine(polars_engine, polars_caps)
        except ImportError:
            logger.debug("Polars engine not available")

        try:
            from ..engines.dask_engine import DaskEngine

            dask_engine = DaskEngine()
            dask_caps = EngineCapabilities(
                name="dask",
                is_lazy=True,
                supports_distributed=True,
                optimal_size_range=(1024 * 1024 * 1024 * 10, float("inf")),  # 10GB+
                memory_efficiency=0.8,
                performance_score=1.2,
            )
            self.register_engine(dask_engine, dask_caps)
        except ImportError:
            logger.debug("Dask engine not available")

    def set_default_engine(self, engine_name: str) -> None:
        """Set default engine for auto-selection."""
        if engine_name not in self._engines and engine_name != "auto":
            raise KeyError(f"Unknown engine: {engine_name}")
        self._default_engine = engine_name

    def get_default_engine(self) -> str:
        """Get default engine name."""
        return self._default_engine
