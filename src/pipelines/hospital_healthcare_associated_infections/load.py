from src.common.bigquery import load_dataframe_to_bigquery


TABLE_NAME = "hospital_healthcare_associated_infections"


def load_hai_data(df):
    load_dataframe_to_bigquery(df, TABLE_NAME)