from google.cloud import bigquery

from src.common.config import GCP_PROJECT_ID
from src.warehouse.config import GOLD_DATASET, SILVER_DATASET


def build_hospital_dimension():
    client = bigquery.Client(project=GCP_PROJECT_ID)

    sql = f"""
    CREATE OR REPLACE TABLE
      `{GCP_PROJECT_ID}.{GOLD_DATASET}.dim_hospital`
    AS
    SELECT DISTINCT
        facility_id,
        facility_name,
        address,
        city,
        state,
        zip_code,
        hospital_type,
        hospital_ownership,
        emergency_services,
        hospital_overall_rating
    FROM
      `{GCP_PROJECT_ID}.{SILVER_DATASET}.hospital_general_information`
    WHERE facility_id IS NOT NULL
    """

    client.query(sql).result()

    print("Completed Gold table: dim_hospital")


def build_hospital_performance_summary():
    client = bigquery.Client(project=GCP_PROJECT_ID)

    sql = f"""
    CREATE OR REPLACE TABLE
      `{GCP_PROJECT_ID}.{GOLD_DATASET}.fact_hospital_performance_summary`
    AS
    SELECT
        h.facility_id,
        h.facility_name,
        h.city,
        h.state,
        h.hospital_type,
        h.hospital_ownership,
        h.emergency_services,
        h.hospital_overall_rating,

        v.fiscal_year AS vbp_fiscal_year,
        v.weighted_normalized_clinical_outcomes_domain_score,
        v.weighted_person_and_community_engagement_domain_score,
        v.weighted_safety_domain_score,
        v.weighted_efficiency_and_cost_reduction_domain_score,
        v.total_performance_score,

        hac.fiscal_year AS hacrp_fiscal_year,
        hac.psi_90_composite_value,
        hac.clabsi_sir,
        hac.cauti_sir,
        hac.ssi_sir,
        hac.cdi_sir,
        hac.mrsa_sir,
        hac.total_hac_score,
        hac.payment_reduction

    FROM
      `{GCP_PROJECT_ID}.{GOLD_DATASET}.dim_hospital` AS h

    LEFT JOIN
      `{GCP_PROJECT_ID}.{SILVER_DATASET}.hospital_value_based_purchasing` AS v
      ON h.facility_id = v.facility_id

    LEFT JOIN
      `{GCP_PROJECT_ID}.{SILVER_DATASET}.hospital_hac_reduction_program` AS hac
      ON h.facility_id = hac.facility_id
    """

    client.query(sql).result()

    print("Completed Gold table: fact_hospital_performance_summary")


if __name__ == "__main__":
    build_hospital_dimension()
    build_hospital_performance_summary()