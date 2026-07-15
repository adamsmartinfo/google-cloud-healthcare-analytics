import pandas as pd


def transform_outpatient_imaging_records(records):
    df = pd.DataFrame(records)

    selected_columns = [
        "facility_id",
        "facility_name",
        "state",
        "measure_id",
        "measure_name",
        "score",
        "start_date",
        "end_date",
    ]

    df = df[selected_columns]

    return df