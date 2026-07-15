from src.pipelines.hospital_hac_reduction_program.extract import (
    extract_hacrp,
)
from src.pipelines.hospital_hac_reduction_program.load import (
    load_hacrp_data,
)
from src.pipelines.hospital_hac_reduction_program.transform import (
    transform_hacrp_records,
)


def run_pipeline():
    records = extract_hacrp()

    df = transform_hacrp_records(records)

    load_hacrp_data(df)

    print(
        "Hospital-Acquired Condition Reduction Program pipeline "
        f"completed successfully for {len(df)} records."
    )


if __name__ == "__main__":
    run_pipeline()