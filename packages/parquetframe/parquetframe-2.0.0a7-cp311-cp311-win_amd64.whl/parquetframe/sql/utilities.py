"""
SQL utilities for ParquetFrame.

Provides helper functions for SQL query operations.
"""

import pandas as pd


def parameterize_query(query_template: str, **params) -> str:
    """
    Parameterize a SQL query template with given parameters.

    Args:
        query_template: SQL query with {param_name} placeholders
        **params: Parameter values to substitute

    Returns:
        Parameterized query string

    Raises:
        ValueError: If required parameters are missing

    Example:
        >>> query = parameterize_query(
        ...     "SELECT * FROM df WHERE age > {min_age} AND salary < {max_salary}",
        ...     min_age=25,
        ...     max_salary=70000
        ... )
        >>> print(query)
        SELECT * FROM df WHERE age > 25 AND salary < 70000
    """
    try:
        return query_template.format(**params)
    except KeyError as e:
        raise ValueError(f"Missing required parameter: {e}") from e


def query_dataframes_from_files(
    main_file: str, query: str, other_files: dict[str, str] | None = None, **kwargs
) -> pd.DataFrame:
    """
    Query files directly without loading into ParquetFrame first.

    Args:
        main_file: Path to main file (referenced as 'df' in query)
        query: SQL query string
        other_files: Optional dict of table_name -> file_path mappings
        **kwargs: Additional options for reading files

    Returns:
        Query result as DataFrame

    Example:
        >>> result = query_dataframes_from_files(
        ...     "users.csv",
        ...     "SELECT name, age FROM df WHERE age > 30"
        ... )

        >>> result = query_dataframes_from_files(
        ...     "users.csv",
        ...     "SELECT u.name, o.amount FROM df u JOIN orders o ON u.id = o.user_id",
        ...     other_files={"orders": "orders.json"}
        ... )
    """
    from ..core.formats import FORMAT_HANDLERS, detect_format
    from .engine import SQLEngine

    # Read main file
    main_format = detect_format(main_file)
    main_handler = FORMAT_HANDLERS[main_format]
    main_df = main_handler.read(main_file, **kwargs)

    # Create SQL engine
    engine = SQLEngine()
    engine.register_dataframe("df", main_df)

    # Read and register other files
    if other_files:
        for table_name, file_path in other_files.items():
            file_format = detect_format(file_path)
            handler = FORMAT_HANDLERS[file_format]
            df = handler.read(file_path, **kwargs)
            engine.register_dataframe(table_name, df)

    # Execute query
    return engine.query(query)


__all__ = [
    "parameterize_query",
    "query_dataframes_from_files",
]
