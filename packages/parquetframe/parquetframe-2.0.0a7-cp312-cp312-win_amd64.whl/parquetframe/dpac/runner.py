"""
Workflow Runner for DPaC.
"""

import os

from parquetframe._rustic import run_workflow


class WorkflowRunner:
    """Executes DPaC workflows defined in YAML."""

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def run(self, yaml_path: str):
        """
        Run a workflow defined in a YAML file.

        Args:
            yaml_path: Path to the workflow.pf.yml file.
        """
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"Workflow file not found: {yaml_path}")

        # Call Rust backend
        run_workflow(os.path.abspath(yaml_path))


def run(yaml_path: str):
    """Convenience function to run a workflow."""
    runner = WorkflowRunner()
    runner.run(yaml_path)
