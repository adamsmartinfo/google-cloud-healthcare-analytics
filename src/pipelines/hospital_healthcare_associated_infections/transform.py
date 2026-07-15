import pandas as pd


def transform_hai_records(records):
    df = pd.DataFrame(records)

    selected_columns = [
        "facility_id",
        "facility_name",
        "state",
        "measure_id",
        "measure_name",
        "compared_to_national",
        "score",
        "start_date",
        "end_date",
    ]

    df = df[selected_columns]

    return df