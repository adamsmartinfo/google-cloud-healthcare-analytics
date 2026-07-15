from src.pipelines.hospital_outpatient_imaging_efficiency.extract import (
    extract_outpatient_imaging,
)
from src.pipelines.hospital_outpatient_imaging_efficiency.load import (
    load_outpatient_imaging_data,
)
from src.pipelines.hospital_outpatient_imaging_efficiency.transform import (
    transform_outpatient_imaging_records,
)


def run_pipeline():
    records = extract_outpatient_imaging()

    df = transform_outpatient_imaging_records(records)

    load_outpatient_imaging_data(df)

    print(
        "Outpatient Imaging Efficiency pipeline completed successfully "
        f"for {len(df)} records."
    )


if __name__ == "__main__":
    run_pipeline()