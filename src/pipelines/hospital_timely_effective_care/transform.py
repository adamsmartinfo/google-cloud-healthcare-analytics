import pandas as pd


def transform_timely_effective_care_records(records):
    df = pd.DataFrame(records)

    selected_columns = [
        "facility_id",
        "facility_name",
        "state",
        "_condition",
        "measure_id",
        "measure_name",
        "score",
        "sample",
        "start_date",
        "end_date",
    ]

    df = df[selected_columns]

    return df