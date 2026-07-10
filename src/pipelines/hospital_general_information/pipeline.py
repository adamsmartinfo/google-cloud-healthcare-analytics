from src.common.config import CMS_HOSPITAL_API_URL
from src.common.cms_client import fetch_all_cms_data
from src.pipelines.hospital_general_information.load import load_hospital_data
from src.pipelines.hospital_general_information.transform import (
    transform_hospital_records,
)


def run_pipeline():
    records = fetch_all_cms_data(
        CMS_HOSPITAL_API_URL,
        batch_size=500,
    )

    df = transform_hospital_records(records)

    load_hospital_data(df)

    print(f"Pipeline completed successfully for {len(df)} hospital records.")


if __name__ == "__main__":
    run_pipeline()