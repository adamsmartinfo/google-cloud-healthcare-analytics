import pandas as pd


def transform_vbp_records(records):
    df = pd.DataFrame(records)

    selected_columns = [
        "fiscal_year",
        "facility_id",
        "facility_name",
        "state",
        "unweighted_normalized_clinical_outcomes_domain_score",
        "weighted_normalized_clinical_outcomes_domain_score",
        "unweighted_person_and_community_engagement_domain_score",
        "weighted_person_and_community_engagement_domain_score",
        "unweighted_normalized_safety_domain_score",
        "weighted_safety_domain_score",
        "unweighted_normalized_efficiency_and_cost_reduction_domain_score",
        "weighted_efficiency_and_cost_reduction_domain_score",
        "total_performance_score",
    ]

    df = df[selected_columns]

    return df