from src.load.upload_to_gcs import upload_file


LOCAL_FILE_PATH = "data/raw/hospital_general_information_sample.json"
DESTINATION_BLOB_NAME = "raw/hospital_general_information_sample.json"


def main():
    upload_file(LOCAL_FILE_PATH, DESTINATION_BLOB_NAME)


if __name__ == "__main__":
    main()