from src.common.bigquery import load_dataframe_to_bigquery


TABLE_NAME = "hospital_readmissions"


def load_readmissions_data(df):
    load_dataframe_to_bigquery(df, TABLE_NAME)