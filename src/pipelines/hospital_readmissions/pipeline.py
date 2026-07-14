from src.pipelines.hospital_readmissions.extract import extract_readmissions
from src.pipelines.hospital_readmissions.load import load_readmissions_data
from src.pipelines.hospital_readmissions.transform import (
    transform_readmission_records,
)


def run_pipeline():
    records = extract_readmissions()

    df = transform_readmission_records(records)

    load_readmissions_data(df)

    print(
        f"Readmissions pipeline completed successfully for {len(df)} records."
    )


if __name__ == "__main__":
    run_pipeline()