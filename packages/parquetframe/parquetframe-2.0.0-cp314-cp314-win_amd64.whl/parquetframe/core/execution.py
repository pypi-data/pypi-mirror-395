"""
Execution context and mode selection for parallel and distributed operations.

Supports intelligent switching between:
- Local parallel (Rayon multi-threading)
- Distributed (Ray/Dask scale-out)
- Hybrid (Both combined)
"""

import os
from dataclasses import dataclass, field
from enum import Enum

# Import metrics
from .metrics import MetricsCollector, get_metrics_collector

try:
    import ray
except ImportError:
    ray = None

try:
    from dask.distributed import Client
except ImportError:
    Client = None


class ExecutionMode(Enum):
    """Execution mode for operations."""

    AUTO = "auto"
    LOCAL = "local"
    DISTRIBUTED = "distributed"
    HYBRID = "hybrid"


@dataclass
class ExecutionContext:
    """
    Context for execution configuration and resources.

    Holds configuration for parallel/distributed execution and metrics.
    """

    mode: ExecutionMode = ExecutionMode.AUTO
    rust_threads: int = 0  # 0 means auto-detect
    distributed_backend: str = "ray"  # 'ray' or 'dask'
    distributed_nodes: int = 1
    metrics: MetricsCollector = field(default_factory=get_metrics_collector)

    def __post_init__(self):
        pass

    @classmethod
    def from_env(cls) -> "ExecutionContext":
        """Create context from environment variables."""
        mode_str = os.getenv("PF_EXECUTION_MODE", "auto")
        return cls(
            mode=ExecutionMode(mode_str),
            rust_threads=int(os.getenv("PF_RUST_THREADS", "0")),
            distributed_backend=os.getenv("PF_DISTRIBUTED_BACKEND", "ray"),
            distributed_nodes=int(os.getenv("PF_DISTRIBUTED_NODES", "1")),
        )

    @classmethod
    def auto_detect(
        cls, data_size_gb: float, available_nodes: int = 1
    ) -> "ExecutionContext":
        """
        Intelligently choose execution mode based on data size and resources.

        Args:
            data_size_gb: Size of data in gigabytes
            available_nodes: Number of available distributed nodes

        Returns:
            ExecutionContext with optimal settings
        """
        # Check for distributed cluster
        has_cluster = available_nodes > 1

        # Decision matrix
        if data_size_gb > 100 and has_cluster:
            # Very large data + cluster → full distributed
            return cls(
                mode=ExecutionMode.DISTRIBUTED,
                distributed_backend="ray",
                distributed_nodes=available_nodes,
                rust_threads=8,  # Moderate per-worker parallelism
            )
        elif data_size_gb > 10 and has_cluster:
            # Large data + cluster → hybrid mode
            return cls(
                mode=ExecutionMode.HYBRID,
                distributed_nodes=available_nodes,
                rust_threads=16,  # High per-worker parallelism
            )
        elif data_size_gb > 1:
            # Medium data, single machine → local parallel
            return cls(
                mode=ExecutionMode.LOCAL,
                rust_threads=0,  # Use all available cores
            )
        else:
            # Small data → conservative parallelism
            return cls(mode=ExecutionMode.LOCAL, rust_threads=4)

    def resolve(self, override_mode: str | None = None) -> "ExecutionContext":
        """
        Resolve execution context with optional mode override.

        Args:
            override_mode: Optional mode to override current setting

        Returns:
            New ExecutionContext with resolved mode
        """
        if override_mode:
            return ExecutionContext(
                mode=ExecutionMode(override_mode),
                rust_threads=self.rust_threads,
                distributed_backend=self.distributed_backend,
                distributed_nodes=self.distributed_nodes,
            )
        return self


class ExecutionPlanner:
    """
    Plans execution strategy for operations.

    Considers:
    - Data size
    - Available resources (CPU cores, cluster nodes)
    - Operation characteristics
    """

    @staticmethod
    def check_distributed_available() -> tuple[bool, int]:
        """
        Check if distributed cluster is available.

        Returns:
            (available, num_nodes) tuple
        """
        # Try Ray first
        try:
            import ray

            if ray.is_initialized():
                nodes = ray.nodes()
                return len(nodes) > 1, len(nodes)
        except ImportError:
            pass

        # Try Dask
        try:
            from dask.distributed import Client

            try:
                client = Client.current()
                workers = client.scheduler_info()["workers"]
                return len(workers) > 1, len(workers)
            except ValueError:
                pass  # No client connected
        except ImportError:
            pass

        return False, 1

    @staticmethod
    def plan_execution(
        operation: str,
        data_size_gb: float,
        user_preference: ExecutionMode | None = None,
    ) -> ExecutionContext:
        """
        Plan optimal execution strategy.

        Args:
            operation: Operation name (e.g., 'filter', 'join')
            data_size_gb: Estimated data size in GB
            user_preference: Optional user-specified mode

        Returns:
            ExecutionContext with planned settings
        """
        # If user specified mode, use it
        if user_preference and user_preference != ExecutionMode.AUTO:
            distributed_available, num_nodes = (
                ExecutionPlanner.check_distributed_available()
            )
            return ExecutionContext(
                mode=user_preference,
                distributed_nodes=num_nodes if distributed_available else 1,
            )

        # Auto-detect resources
        distributed_available, num_nodes = (
            ExecutionPlanner.check_distributed_available()
        )

        # Auto-detect optimal mode
        return ExecutionContext.auto_detect(data_size_gb, num_nodes)


# Global configuration
_global_execution_context: ExecutionContext = ExecutionContext.from_env()


def set_execution_config(
    mode: str = "auto",
    rust_threads: int = 0,
    distributed_backend: str = "ray",
    distributed_nodes: int = 1,
):
    """
    Set global execution configuration.

    Args:
        mode: Execution mode (auto/local/distributed/hybrid)
        rust_threads: Number of Rayon threads (0 = auto)
        distributed_backend: Distributed backend (ray/dask)
        distributed_nodes: Number of nodes to use
    """
    global _global_execution_context
    _global_execution_context = ExecutionContext(
        mode=ExecutionMode(mode),
        rust_threads=rust_threads,
        distributed_backend=distributed_backend,
        distributed_nodes=distributed_nodes,
    )


def get_execution_context() -> ExecutionContext:
    """Get current global execution context."""
    return _global_execution_context


__all__ = [
    "ExecutionMode",
    "ExecutionContext",
    "ExecutionPlanner",
    "set_execution_config",
    "get_execution_context",
]
