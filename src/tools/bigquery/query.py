import re

from google.cloud import bigquery

from src.tools.bigquery.client import get_bigquery_client


APPROVED_DATASETS = {
    "healthcare_gold",
}

APPROVED_TABLES = {
    "healthcare_gold": {
        "dim_hospital",
        "fact_hospital_performance_summary",
    },
}


def _validate_read_only_sql(sql: str) -> None:
    """Validate that SQL is read-only and references approved datasets and tables."""

    if not sql or not sql.strip():
        raise ValueError("sql is required.")

    normalized_sql = sql.strip().upper()

    if not normalized_sql.startswith(("SELECT", "WITH")):
        raise ValueError("Only SELECT queries and read-only CTE queries are allowed.")

    blocked_keywords = {
        "INSERT",
        "UPDATE",
        "DELETE",
        "MERGE",
        "CREATE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "EXPORT",
        "CALL",
        "GRANT",
        "REVOKE",
    }

    for keyword in blocked_keywords:
        if re.search(rf"\b{keyword}\b", normalized_sql):
            raise ValueError(
                f"Query blocked because it contains the prohibited keyword: {keyword}."
            )

    table_references = re.findall(
        r"(?:`[^`]+?\.)?"
        r"([A-Za-z_][A-Za-z0-9_]*)"
        r"\."
        r"([A-Za-z_][A-Za-z0-9_]*)"
        r"`?",
        sql,
    )

    for dataset, table in table_references:
        normalized_dataset = dataset.lower()
        normalized_table = table.lower()

        if normalized_dataset not in APPROVED_DATASETS:
            raise ValueError(
                "Query references an unapproved dataset. "
                f"Approved datasets: {sorted(APPROVED_DATASETS)}. "
                f"Unapproved dataset found: {dataset}."
            )

        approved_tables = {
            approved_table.lower()
            for approved_table in APPROVED_TABLES.get(normalized_dataset, set())
        }

        if normalized_table not in approved_tables:
            raise ValueError(
                f"Table '{dataset}.{table}' is not approved. "
                f"Approved tables for '{normalized_dataset}': "
                f"{sorted(approved_tables)}."
            )


def execute_read_only_query(
    sql: str,
    maximum_bytes_billed: int = 100_000_000,
) -> list[dict]:
    """Execute an approved read-only BigQuery query with cost controls."""

    _validate_read_only_sql(sql)

    client = get_bigquery_client()

    dry_run_config = bigquery.QueryJobConfig(
        dry_run=True,
        use_query_cache=False,
    )

    dry_run_job = client.query(sql, job_config=dry_run_config)
    estimated_bytes = dry_run_job.total_bytes_processed or 0

    if estimated_bytes > maximum_bytes_billed:
        raise ValueError(
            "Query exceeds the permitted processing limit. "
            f"Estimated bytes: {estimated_bytes:,}. "
            f"Maximum allowed: {maximum_bytes_billed:,}."
        )

    query_config = bigquery.QueryJobConfig(
        maximum_bytes_billed=maximum_bytes_billed,
    )

    query_job = client.query(sql, job_config=query_config)
    rows = query_job.result()

    return [dict(row.items()) for row in rows]