import pandas as pd


def transform_readmission_records(records):
    df = pd.DataFrame(records)

    selected_columns = [
        "facility_id",
        "facility_name",
        "state",
        "measure_id",
        "measure_name",
        "compared_to_national",
        "denominator",
        "score",
        "lower_estimate",
        "higher_estimate",
        "number_of_patients",
        "number_of_patients_returned",
        "start_date",
        "end_date",
    ]

    df = df[selected_columns]

    return df