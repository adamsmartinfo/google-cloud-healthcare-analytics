from src.pipelines.hospital_mortality.extract import extract_mortality
from src.pipelines.hospital_mortality.load import load_mortality_data
from src.pipelines.hospital_mortality.transform import (
    transform_mortality_records,
)


def run_pipeline():
    records = extract_mortality()

    df = transform_mortality_records(records)

    load_mortality_data(df)

    print(
        f"Mortality pipeline completed successfully for {len(df)} records."
    )


if __name__ == "__main__":
    run_pipeline()