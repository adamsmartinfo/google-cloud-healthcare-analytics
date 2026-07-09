from google.cloud import bigquery

from src.utils.config import GCP_PROJECT_ID, BIGQUERY_DATASET


def load_dataframe_to_bigquery(df, table_name):
    client = bigquery.Client(project=GCP_PROJECT_ID)

    table_id = f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True,
    )

    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config,
    )

    job.result()

    print(f"Loaded {len(df)} rows into {table_id}")