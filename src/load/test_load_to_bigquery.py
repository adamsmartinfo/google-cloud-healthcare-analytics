import json

from src.load.load_to_bigquery import load_dataframe_to_bigquery
from src.transform.transform_hospitals import transform_hospital_records


RAW_FILE_PATH = "data/raw/hospital_general_information.json"
TABLE_NAME = "hospital_general_information"


def main():
    with open(RAW_FILE_PATH, "r") as file:
        records = json.load(file)

    df = transform_hospital_records(records)

    load_dataframe_to_bigquery(df, TABLE_NAME)


if __name__ == "__main__":
    main()