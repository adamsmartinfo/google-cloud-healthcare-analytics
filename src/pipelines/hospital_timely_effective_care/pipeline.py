from src.pipelines.hospital_timely_effective_care.extract import (
    extract_timely_effective_care,
)
from src.pipelines.hospital_timely_effective_care.load import (
    load_timely_effective_care_data,
)
from src.pipelines.hospital_timely_effective_care.transform import (
    transform_timely_effective_care_records,
)


def run_pipeline():
    records = extract_timely_effective_care()

    df = transform_timely_effective_care_records(records)

    load_timely_effective_care_data(df)

    print(
        "Timely & Effective Care pipeline completed successfully "
        f"for {len(df)} records."
    )


if __name__ == "__main__":
    run_pipeline()