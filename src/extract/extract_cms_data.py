import json
import requests


CMS_API_URL = "https://data.cms.gov/provider-data/api/1/datastore/query/xubh-q36u/0?limit=10"
RAW_OUTPUT_PATH = "data/raw/hospital_general_information_sample.json"

def get_hospital_data():
    response = requests.get(CMS_API_URL)
    response.raise_for_status()

    data = response.json()
    return data["results"]


def save_raw_json(hospitals, output_path):
    with open(output_path, "w") as file:
        json.dump(hospitals, file, indent=2)


def main():
    print("Healthcare Analytics Pipeline")
    print("Requesting hospital data from CMS API...")

    hospitals = get_hospital_data()

    save_raw_json(hospitals, RAW_OUTPUT_PATH)

    print(f"Retrieved {len(hospitals)} hospital records.")
    print(f"Saved raw data to {RAW_OUTPUT_PATH}")


if __name__ == "__main__":
    main()