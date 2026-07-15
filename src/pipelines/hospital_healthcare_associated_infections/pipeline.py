from src.pipelines.hospital_healthcare_associated_infections.extract import (
    extract_hai,
)
from src.pipelines.hospital_healthcare_associated_infections.load import (
    load_hai_data,
)
from src.pipelines.hospital_healthcare_associated_infections.transform import (
    transform_hai_records,
)


def run_pipeline():
    records = extract_hai()

    df = transform_hai_records(records)

    load_hai_data(df)

    print(
        "Healthcare-Associated Infections pipeline completed successfully "
        f"for {len(df)} records."
    )


if __name__ == "__main__":
    run_pipeline()