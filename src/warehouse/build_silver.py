from google.cloud import bigquery

from src.common.config import GCP_PROJECT_ID
from src.warehouse.schemas import SCHEMA_REGISTRY
from src.warehouse.sql_generator import generate_silver_table_sql


def build_silver_tables():
    client = bigquery.Client(project=GCP_PROJECT_ID)

    for table_name in SCHEMA_REGISTRY:
        print(f"Building Silver table: {table_name}")

        sql = generate_silver_table_sql(
            project_id=GCP_PROJECT_ID,
            table_name=table_name,
        )

        query_job = client.query(sql)
        query_job.result()

        print(f"Completed Silver table: {table_name}")


if __name__ == "__main__":
    build_silver_tables()