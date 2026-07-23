from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")