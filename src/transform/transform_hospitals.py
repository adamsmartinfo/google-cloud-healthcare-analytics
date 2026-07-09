import pandas as pd


def transform_hospital_records(records):
    df = pd.DataFrame(records)

    selected_columns = [
        "facility_id",
        "facility_name",
        "address",
        "citytown",
        "state",
        "zip_code",
        "hospital_type",
        "hospital_ownership",
        "emergency_services",
        "hospital_overall_rating",
    ]

    df = df[selected_columns]

    df.columns = [
        "facility_id",
        "facility_name",
        "address",
        "city",
        "state",
        "zip_code",
        "hospital_type",
        "hospital_ownership",
        "emergency_services",
        "hospital_overall_rating",
    ]

    return df