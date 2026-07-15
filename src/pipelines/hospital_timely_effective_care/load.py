from src.common.bigquery import load_dataframe_to_bigquery


TABLE_NAME = "hospital_timely_effective_care"


def load_timely_effective_care_data(df):
    load_dataframe_to_bigquery(df, TABLE_NAME)