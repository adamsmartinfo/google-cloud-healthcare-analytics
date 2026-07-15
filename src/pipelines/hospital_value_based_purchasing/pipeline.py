from src.pipelines.hospital_value_based_purchasing.extract import extract_vbp
from src.pipelines.hospital_value_based_purchasing.load import load_vbp_data
from src.pipelines.hospital_value_based_purchasing.transform import (
    transform_vbp_records,
)


def run_pipeline():
    records = extract_vbp()

    df = transform_vbp_records(records)

    load_vbp_data(df)

    print(
        "Hospital Value-Based Purchasing pipeline completed successfully "
        f"for {len(df)} records."
    )


if __name__ == "__main__":
    run_pipeline()