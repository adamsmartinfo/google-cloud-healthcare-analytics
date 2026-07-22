from google.cloud import bigquery

from src.tools.bigquery.client import get_bigquery_client


def execute_read_only_query(
    sql: str,
    maximum_bytes_billed: int = 100_000_000,
) -> list[dict]:
    """Execute a read-only BigQuery query with validation and cost controls."""

    if not sql or not sql.strip():
        raise ValueError("sql is required.")

    normalized_sql = sql.strip().upper()

    if not normalized_sql.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")

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