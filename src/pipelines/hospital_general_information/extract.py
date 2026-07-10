import json

from src.common.storage import upload_file
from src.common.cms_client import fetch_all_cms_data
from src.common.config import CMS_HOSPITAL_API_URL

RAW_OUTPUT_PATH = "data/raw/hospital_general_information.json"
GCS_RAW_PATH = "raw/hospital_general_information.json"

def save_raw_json(records, output_path):
    with open(output_path, "w") as file:
        json.dump(records, file, indent=2)


def main():
    print("Healthcare Analytics Pipeline")
    print("Requesting hospital data from CMS API...")

    hospitals = fetch_all_cms_data(CMS_HOSPITAL_API_URL, batch_size=500)

    save_raw_json(hospitals, RAW_OUTPUT_PATH)
    upload_file(RAW_OUTPUT_PATH, GCS_RAW_PATH)
    
    print(f"Retrieved {len(hospitals)} hospital records.")
    print(f"Saved raw data to {RAW_OUTPUT_PATH}")


if __name__ == "__main__":
    main()