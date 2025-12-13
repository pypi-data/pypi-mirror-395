"""
Interactive REPL for ParquetFrame.

Rich interactive shell with syntax highlighting and tab completion.
"""


def start_repl():
    """Start the enhanced ParquetFrame REPL."""
    try:
        import importlib.util

        from rich.console import Console
        from rich.markdown import Markdown
        from rich.panel import Panel

        if importlib.util.find_spec("rich"):
            from rich.syntax import Syntax  # noqa: F401

        import parquetframe as pf
    except ImportError:
        print("⚠️  Rich not installed.")
        print("Install with: pip install rich")
        print("\nStarting basic REPL...")
        return start_basic_repl()

    console = Console()

    # Welcome message
    welcome = """
# ParquetFrame Interactive REPL

**Features**:
- Syntax highlighting
- Rich output formatting
- Easy data inspection

**Quick Start**:
```python
import parquetframe as pf
df = pf.read_parquet("data.parquet")
```
    """

    console.print(
        Panel(Markdown(welcome), title="🚀 ParquetFrame REPL", border_style="blue")
    )

    # Import commonly used libraries
    import numpy as np
    import pandas as pd

    # Make available in REPL
    namespace = {"pf": pf, "pd": pd, "np": np, "console": console}

    # Start interactive mode
    try:
        from IPython import embed

        embed(user_ns=namespace, colors="neutral")
    except ImportError:
        # Fallback to basic REPL
        import code

        console.print(
            "\n💡 Install IPython for better experience: pip install ipython\n"
        )
        code.interact(local=namespace, banner="")


def start_basic_repl():
    """Start basic REPL without rich features."""
    import code

    import numpy as np
    import pandas as pd

    import parquetframe as pf

    banner = """
╔══════════════════════════════════════╗
║   ParquetFrame Interactive REPL      ║
╚══════════════════════════════════════╝

Available:
  pf  - ParquetFrame
  pd  - pandas
  np  - numpy

Example:
  >>> df = pf.read_parquet("data.parquet")
  >>> df.head()
    """

    namespace = {"pf": pf, "pd": pd, "np": np}

    code.interact(local=namespace, banner=banner)


if __name__ == "__main__":
    start_repl()
