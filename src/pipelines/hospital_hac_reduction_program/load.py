from src.common.bigquery import load_dataframe_to_bigquery


TABLE_NAME = "hospital_hac_reduction_program"


def load_hacrp_data(df):
    load_dataframe_to_bigquery(df, TABLE_NAME)