import pandas as pd


def transform_hacrp_records(records):
    df = pd.DataFrame(records)

    selected_columns = [
        "facility_id",
        "facility_name",
        "state",
        "fiscal_year",
        "psi_90_composite_value",
        "clabsi_sir",
        "cauti_sir",
        "ssi_sir",
        "cdi_sir",
        "mrsa_sir",
        "total_hac_score",
        "payment_reduction",
    ]

    df = df[selected_columns]

    return df