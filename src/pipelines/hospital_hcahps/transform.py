import pandas as pd


def transform_hcahps_records(records):
    df = pd.DataFrame(records)

    selected_columns = [
        "facility_id",
        "facility_name",
        "state",
        "hcahps_measure_id",
        "hcahps_question",
        "hcahps_answer_description",
        "patient_survey_star_rating",
        "hcahps_answer_percent",
        "hcahps_linear_mean_value",
        "number_of_completed_surveys",
        "survey_response_rate_percent",
        "start_date",
        "end_date",
    ]

    df = df[selected_columns]

    return df