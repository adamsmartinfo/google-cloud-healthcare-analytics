import json

from src.transform.transform_hospitals import transform_hospital_records


RAW_FILE_PATH = "data/raw/hospital_general_information_sample.json"


def main():
    with open(RAW_FILE_PATH, "r") as file:
        records = json.load(file)

    df = transform_hospital_records(records)

    print(df.head())
    print(df.info())


if __name__ == "__main__":
    main()