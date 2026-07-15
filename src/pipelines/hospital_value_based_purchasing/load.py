from src.common.bigquery import load_dataframe_to_bigquery


TABLE_NAME = "hospital_value_based_purchasing"


def load_vbp_data(df):
    load_dataframe_to_bigquery(df, TABLE_NAME)