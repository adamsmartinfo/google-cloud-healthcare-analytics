from config.settings import GCP_PROJECT_ID
from src.tools.bigquery.client import get_bigquery_client


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


def get_table_schema(
    dataset_id: str,
    table_id: str,
) -> list[dict[str, str]]:
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