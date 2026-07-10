from src.common.bigquery import load_dataframe_to_bigquery


TABLE_NAME = "hospital_general_information"


def load_hospital_data(df):
    load_dataframe_to_bigquery(df, TABLE_NAME)