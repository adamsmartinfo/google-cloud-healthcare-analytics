from langchain_core.tools import tool

from src.tools.bigquery.metadata import (
    get_table_schema,
    list_datasets,
    list_tables,
)
from src.tools.bigquery.query import execute_read_only_query


@tool
def list_bigquery_datasets() -> list[str]:
    """List the BigQuery datasets available in the configured project."""

    return list_datasets()


@tool
def list_bigquery_tables(dataset_id: str) -> list[str]:
    """List the tables available in a specific BigQuery dataset."""

    return list_tables(dataset_id)


@tool
def inspect_bigquery_table_schema(
    dataset_id: str,
    table_id: str,
) -> list[dict[str, str]]:
    """Inspect column names, data types, modes, and descriptions for a table."""

    return get_table_schema(dataset_id, table_id)


@tool
def run_bigquery_read_only_query(sql: str) -> list[dict]:
    """Run a read-only SELECT query in BigQuery with cost safeguards."""

    return execute_read_only_query(sql)