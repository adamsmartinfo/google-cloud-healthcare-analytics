from google.cloud import bigquery

from config.settings import GCP_PROJECT_ID


def get_bigquery_client() -> bigquery.Client:
    """Create an authenticated BigQuery client for the configured project."""

    if not GCP_PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID is not configured.")

    return bigquery.Client(project=GCP_PROJECT_ID)