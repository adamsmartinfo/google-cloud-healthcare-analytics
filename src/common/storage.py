from google.cloud import storage

from src.common.config import GCS_BUCKET_NAME


def upload_file(local_file_path, destination_blob_name):
    client = storage.Client()

    bucket = client.bucket(GCS_BUCKET_NAME)

    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(local_file_path)

    print(f"Uploaded {local_file_path} to {destination_blob_name}")