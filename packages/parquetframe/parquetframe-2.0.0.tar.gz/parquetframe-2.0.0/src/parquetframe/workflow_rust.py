"""
Rust-accelerated workflow engine integration.

This module provides a Python interface to the Rust workflow engine,
offering high-performance parallel execution of workflow steps.

Phase 3.5-3.6: Initial integration with placeholder functions.
Full implementation connects to pf-workflow-core Rust crate.
"""

from typing import Any

try:
    from parquetframe import _rustic

    RUST_WORKFLOW_AVAILABLE = _rustic.rust_available()
except ImportError:
    RUST_WORKFLOW_AVAILABLE = False
    _rustic = None


# Expose Rust-side cancellation token
try:
    from parquetframe._rustic import CancellationToken as _RustCancellationToken
except Exception:  # pragma: no cover
    _RustCancellationToken = None


class CancellationToken:
    """Cancellation token for stopping running workflows.

    Example:
        >>> from parquetframe.workflow_rust import CancellationToken, execute_workflow_rust
        >>> token = CancellationToken()
        >>> # In another thread: token.cancel()
    """

    def __init__(self) -> None:
        if _RustCancellationToken is None:
            raise RuntimeError("Rust workflow backend not available")
        self._inner = _RustCancellationToken()

    def cancel(self) -> None:
        self._inner.cancel()

    def is_cancelled(self) -> bool:
        return self._inner.is_cancelled()


class RustWorkflowEngine:
    """
    Rust-accelerated workflow execution engine.

    Provides high-performance parallel execution of workflow DAGs
    with resource-aware scheduling and progress tracking.

    Features:
    - Parallel execution of independent steps
    - Resource-aware scheduling
    - Automatic dependency resolution
    - Progress tracking
    - Cancellation support
    - Performance metrics

    Example:
        >>> engine = RustWorkflowEngine(max_parallel=4)
        >>> if engine.is_available():
        ...     result = engine.execute_workflow(workflow_config)
        ...     print(f"Executed in {result['execution_time_ms']}ms")
    """

    def __init__(self, max_parallel: int | None = None):
        """
        Initialize the Rust workflow engine.

        Args:
            max_parallel: Maximum number of parallel workers.
                         If None, uses system CPU count.
        """
        self.max_parallel = max_parallel or 4
        self._check_availability()

    def _check_availability(self) -> None:
        """Check if Rust workflow engine is available."""
        if not RUST_WORKFLOW_AVAILABLE:
            raise RuntimeError(
                "Rust backend not available. "
                "Please rebuild with: maturin develop --release"
            )

    @staticmethod
    def is_available() -> bool:
        """
        Check if Rust workflow engine is available.

        Returns:
            True if the Rust workflow engine can be used.
        """
        if not RUST_WORKFLOW_AVAILABLE or _rustic is None:
            return False
        # Check if execute_workflow function exists in _rustic
        if not hasattr(_rustic, "execute_workflow"):
            return False
        # Try to call workflow_rust_available if it exists, else fallback to rust_available
        checker = getattr(_rustic, "workflow_rust_available", None)
        if checker is not None:
            return checker()
        # Fallback: if rust is available but no specific workflow check, assume available
        return getattr(_rustic, "rust_available", lambda: False)()

    def execute_step(
        self,
        step_type: str,
        config: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute a single workflow step using Rust backend.

        Args:
            step_type: Type of step (e.g., "read", "filter", "transform")
            config: Step configuration
            context: Workflow execution context

        Returns:
            Step execution result

        Example:
            >>> engine = RustWorkflowEngine()
            >>> result = engine.execute_step(
            ...     "read",
            ...     {"input": "data.parquet"},
            ...     {"variables": {}}
            ... )
        """
        return _rustic.execute_step(step_type, config, context)

    def create_dag(self, steps: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Create a DAG (Directed Acyclic Graph) from workflow steps.

        Analyzes step dependencies and creates an execution plan
        for parallel execution.

        Args:
            steps: List of step definitions with dependencies

        Returns:
            DAG execution plan

        Example:
            >>> engine = RustWorkflowEngine()
            >>> dag = engine.create_dag([
            ...     {"name": "read", "type": "read"},
            ...     {"name": "filter", "type": "filter", "depends_on": ["read"]}
            ... ])
        """
        return _rustic.create_dag(steps)

    def execute_workflow(
        self,
        workflow_config: dict[str, Any],
        *,
        on_progress: Any | None = None,
        cancel_token: CancellationToken | None = None,
        step_handler: Any | None = None,
    ) -> dict[str, Any]:
        """
        Execute a complete workflow using Rust parallel engine.

        Provides:
        - Automatic dependency resolution
        - Parallel execution of independent steps
        - Resource-aware scheduling
        - Progress tracking
        - Error handling and rollback

        Args:
            workflow_config: Complete workflow configuration including
                           steps, variables, and execution settings

        Returns:
            Workflow execution results including:
            - status: "completed" or "failed"
            - execution_time_ms: Total execution time
            - steps_executed: Number of steps executed
            - parallel_workers: Number of parallel workers used

        Example:
            >>> engine = RustWorkflowEngine(max_parallel=4)
            >>> workflow = {
            ...     "name": "data_pipeline",
            ...     "steps": [
            ...         {"name": "read", "type": "read", "config": {...}},
            ...         {"name": "filter", "type": "filter", "config": {...}}
            ...     ]
            ... }
            >>> result = engine.execute_workflow(workflow)
            >>> print(f"Completed in {result['execution_time_ms']}ms")
        """
        return _rustic.execute_workflow(
            workflow_config,
            max_parallel=self.max_parallel,
            on_progress=on_progress,
            cancel_token=(cancel_token._inner if cancel_token else None),
            step_handler=step_handler,
        )

    def get_metrics(self) -> dict[str, Any]:
        """
        Get workflow engine performance metrics.

        Returns:
            Dictionary containing:
            - total_workflows: Total workflows executed
            - total_steps: Total steps executed
            - avg_execution_ms: Average execution time
            - parallel_speedup: Average parallel speedup factor

        Example:
            >>> engine = RustWorkflowEngine()
            >>> metrics = engine.get_metrics()
            >>> print(f"Average speedup: {metrics['parallel_speedup']}x")
        """
        return _rustic.workflow_metrics()


# Convenience functions for backward compatibility


def execute_workflow_rust(
    workflow_config: dict[str, Any],
    max_parallel: int | None = None,
    *,
    on_progress: Any | None = None,
    cancel_token: CancellationToken | None = None,
    step_handler: Any | None = None,
) -> dict[str, Any]:
    """
    Execute a workflow using the Rust engine.

    Convenience function that creates an engine and executes the workflow.

    Args:
        workflow_config: Workflow configuration
        max_parallel: Maximum parallel workers

    Returns:
        Execution results

    Example:
        >>> result = execute_workflow_rust(workflow_config, max_parallel=4)
    """
    engine = RustWorkflowEngine(max_parallel=max_parallel)
    return engine.execute_workflow(
        workflow_config,
        on_progress=on_progress,
        cancel_token=cancel_token,
        step_handler=step_handler,
    )


def is_rust_workflow_available() -> bool:
    """
    Check if Rust workflow engine is available.

    Returns:
        True if Rust workflow acceleration is available

    Example:
        >>> if is_rust_workflow_available():
        ...     print("Using Rust-accelerated workflows")
        ... else:
        ...     print("Using Python workflows")
    """
    return RustWorkflowEngine.is_available()


# Module-level availability flag
__all__ = [
    "CancellationToken",
    "RustWorkflowEngine",
    "execute_workflow_rust",
    "is_rust_workflow_available",
    "RUST_WORKFLOW_AVAILABLE",
]
