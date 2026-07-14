from src.pipelines.hospital_hcahps.extract import extract_hcahps
from src.pipelines.hospital_hcahps.load import load_hcahps_data
from src.pipelines.hospital_hcahps.transform import transform_hcahps_records


def run_pipeline():
    records = extract_hcahps()

    df = transform_hcahps_records(records)

    load_hcahps_data(df)

    print(f"HCAHPS pipeline completed successfully for {len(df)} records.")


if __name__ == "__main__":
    run_pipeline()