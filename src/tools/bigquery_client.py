from google.cloud import bigquery

from config.settings import GCP_PROJECT_ID


def get_bigquery_client() -> bigquery.Client:
    """Create an authenticated BigQuery client for the configured project."""

    if not GCP_PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID is not configured.")

    return bigquery.Client(project=GCP_PROJECT_ID)

def list_datasets() -> list[str]:
    """Return the dataset IDs available in the configured BigQuery project."""

    client = get_bigquery_client()
    datasets = client.list_datasets()

    return [dataset.dataset_id for dataset in datasets]

def list_tables(dataset_id: str) -> list[str]:
    """Return the table IDs available in a BigQuery dataset."""

    if not dataset_id:
        raise ValueError("dataset_id is required.")

    client = get_bigquery_client()
    tables = client.list_tables(dataset_id)

    return [table.table_id for table in tables]

def get_table_schema(dataset_id: str, table_id: str) -> list[dict[str, str]]:
    """Return column metadata for a BigQuery table."""

    if not dataset_id:
        raise ValueError("dataset_id is required.")

    if not table_id:
        raise ValueError("table_id is required.")

    client = get_bigquery_client()
    table_reference = f"{GCP_PROJECT_ID}.{dataset_id}.{table_id}"
    table = client.get_table(table_reference)

    return [
        {
            "name": field.name,
            "type": field.field_type,
            "mode": field.mode,
            "description": field.description or "",
        }
        for field in table.schema
    ]

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