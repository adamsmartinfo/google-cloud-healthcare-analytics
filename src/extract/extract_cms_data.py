import json

from src.utils.cms_client import fetch_cms_data
from src.utils.config import CMS_HOSPITAL_API_URL
from src.load.upload_to_gcs import upload_file

RAW_OUTPUT_PATH = "data/raw/hospital_general_information_sample.json"
GCS_RAW_PATH = "raw/hospital_general_information_sample.json"

def save_raw_json(records, output_path):
    with open(output_path, "w") as file:
        json.dump(records, file, indent=2)


def main():
    print("Healthcare Analytics Pipeline")
    print("Requesting hospital data from CMS API...")

    hospitals = fetch_cms_data(CMS_HOSPITAL_API_URL, limit=10)

    save_raw_json(hospitals, RAW_OUTPUT_PATH)
    upload_file(RAW_OUTPUT_PATH, GCS_RAW_PATH)
    
    print(f"Retrieved {len(hospitals)} hospital records.")
    print(f"Saved raw data to {RAW_OUTPUT_PATH}")


if __name__ == "__main__":
    main()