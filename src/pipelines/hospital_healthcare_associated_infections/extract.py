import json

from src.common.cms_client import fetch_all_cms_data
from src.common.config import CMS_HOSPITAL_HAI_API_URL
from src.common.storage import upload_file


RAW_OUTPUT_PATH = (
    "data/raw/hospital_healthcare_associated_infections.json"
)

GCS_RAW_PATH = (
    "raw/hospital_healthcare_associated_infections.json"
)


def extract_hai():
    print("Requesting CMS Healthcare-Associated Infections data...")

    records = fetch_all_cms_data(
        CMS_HOSPITAL_HAI_API_URL,
        batch_size=500,
    )

    with open(RAW_OUTPUT_PATH, "w") as file:
        json.dump(records, file, indent=2)

    upload_file(RAW_OUTPUT_PATH, GCS_RAW_PATH)

    print(f"Retrieved {len(records)} HAI records.")
    print(f"Saved raw data to {RAW_OUTPUT_PATH}")

    return records


if __name__ == "__main__":
    extract_hai()