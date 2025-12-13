"""
CLI command for running workflows.
"""

import argparse

from parquetframe.dpac import run


def main():
    parser = argparse.ArgumentParser(description="Run a ParquetFrame workflow.")
    parser.add_argument("workflow_file", help="Path to the workflow YAML file.")
    args = parser.parse_args()

    try:
        print(f"Running workflow: {args.workflow_file}")
        run(args.workflow_file)
        print("Workflow completed successfully.")
    except Exception as e:
        print(f"Workflow failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
