from src.common.bigquery import load_dataframe_to_bigquery


TABLE_NAME = "hospital_outpatient_imaging_efficiency"


def load_outpatient_imaging_data(df):
    load_dataframe_to_bigquery(df, TABLE_NAME)