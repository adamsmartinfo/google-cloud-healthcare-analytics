"""
Central schema registry for the Healthcare Analytics Platform.

Each field definition contains:

- type: Desired BigQuery data type
- nullable: Whether NULL values are allowed
- business_name: Human-readable field name
- description: Business definition of the field

This registry will later support SQL generation, SAFE_CAST logic,
data validation, BigQuery descriptions, and data dictionaries.
"""


def field(
    data_type,
    business_name,
    description,
    nullable=True,
):
    """Create a standardized field definition."""
    return {
        "type": data_type,
        "nullable": nullable,
        "business_name": business_name,
        "description": description,
    }


HOSPITAL_GENERAL_INFORMATION_SCHEMA = {
    "facility_id": field(
        "STRING",
        "Facility ID",
        "Unique CMS identifier assigned to the hospital.",
        nullable=False,
    ),
    "facility_name": field(
        "STRING",
        "Facility Name",
        "Official name of the hospital.",
        nullable=False,
    ),
    "address": field(
        "STRING",
        "Address",
        "Street address of the hospital.",
    ),
    "city": field(
        "STRING",
        "City",
        "City in which the hospital is located.",
    ),
    "state": field(
        "STRING",
        "State",
        "Two-letter state or territory abbreviation.",
    ),
    "zip_code": field(
        "STRING",
        "ZIP Code",
        "Postal ZIP code of the hospital.",
    ),
    "hospital_type": field(
        "STRING",
        "Hospital Type",
        "CMS classification of the hospital.",
    ),
    "hospital_ownership": field(
        "STRING",
        "Hospital Ownership",
        "Ownership category of the hospital.",
    ),
    "emergency_services": field(
        "BOOL",
        "Emergency Services",
        "Indicates whether the hospital provides emergency services.",
    ),
    "hospital_overall_rating": field(
        "INT64",
        "Overall Hospital Rating",
        "CMS overall hospital star rating.",
    ),
}


HOSPITAL_READMISSIONS_SCHEMA = {
    "facility_id": field(
        "STRING",
        "Facility ID",
        "Unique CMS identifier assigned to the hospital.",
        nullable=False,
    ),
    "facility_name": field(
        "STRING",
        "Facility Name",
        "Official name of the hospital.",
    ),
    "state": field(
        "STRING",
        "State",
        "Two-letter state or territory abbreviation.",
    ),
    "measure_id": field(
        "STRING",
        "Measure ID",
        "CMS identifier for the readmission measure.",
        nullable=False,
    ),
    "measure_name": field(
        "STRING",
        "Measure Name",
        "Descriptive name of the readmission measure.",
    ),
    "compared_to_national": field(
        "STRING",
        "Compared to National",
        "Hospital performance compared with the national result.",
    ),
    "denominator": field(
        "INT64",
        "Denominator",
        "Number of eligible cases included in the measure.",
    ),
    "score": field(
        "FLOAT64",
        "Readmission Score",
        "CMS-reported readmission performance score.",
    ),
    "lower_estimate": field(
        "FLOAT64",
        "Lower Estimate",
        "Lower bound of the reported statistical estimate.",
    ),
    "higher_estimate": field(
        "FLOAT64",
        "Higher Estimate",
        "Upper bound of the reported statistical estimate.",
    ),
    "number_of_patients": field(
        "INT64",
        "Number of Patients",
        "Number of patients included in the measure.",
    ),
    "number_of_patients_returned": field(
        "INT64",
        "Patients Returned",
        "Number of patients who returned after discharge.",
    ),
    "start_date": field(
        "DATE",
        "Measure Start Date",
        "Beginning of the measure reporting period.",
    ),
    "end_date": field(
        "DATE",
        "Measure End Date",
        "End of the measure reporting period.",
    ),
}


HOSPITAL_HCAHPS_SCHEMA = {
    "facility_id": field(
        "STRING",
        "Facility ID",
        "Unique CMS identifier assigned to the hospital.",
        nullable=False,
    ),
    "facility_name": field(
        "STRING",
        "Facility Name",
        "Official name of the hospital.",
    ),
    "state": field(
        "STRING",
        "State",
        "Two-letter state or territory abbreviation.",
    ),
    "hcahps_measure_id": field(
        "STRING",
        "HCAHPS Measure ID",
        "CMS identifier for the patient experience measure.",
        nullable=False,
    ),
    "hcahps_question": field(
        "STRING",
        "HCAHPS Question",
        "Patient survey question or measure topic.",
    ),
    "hcahps_answer_description": field(
        "STRING",
        "Answer Description",
        "Description of the reported survey response.",
    ),
    "patient_survey_star_rating": field(
        "FLOAT64",
        "Patient Survey Star Rating",
        "CMS patient experience star rating.",
    ),
    "hcahps_answer_percent": field(
        "FLOAT64",
        "Answer Percentage",
        "Percentage of survey responses represented by the answer.",
    ),
    "hcahps_linear_mean_value": field(
        "FLOAT64",
        "Linear Mean Value",
        "CMS-calculated linear mean score for the survey measure.",
    ),
    "number_of_completed_surveys": field(
        "INT64",
        "Completed Surveys",
        "Number of completed patient surveys.",
    ),
    "survey_response_rate_percent": field(
        "FLOAT64",
        "Survey Response Rate",
        "Percentage of eligible patients who completed the survey.",
    ),
    "start_date": field(
        "DATE",
        "Survey Start Date",
        "Beginning of the survey reporting period.",
    ),
    "end_date": field(
        "DATE",
        "Survey End Date",
        "End of the survey reporting period.",
    ),
}


HOSPITAL_MORTALITY_SCHEMA = {
    "facility_id": field(
        "STRING",
        "Facility ID",
        "Unique CMS identifier assigned to the hospital.",
        nullable=False,
    ),
    "facility_name": field(
        "STRING",
        "Facility Name",
        "Official name of the hospital.",
    ),
    "state": field(
        "STRING",
        "State",
        "Two-letter state or territory abbreviation.",
    ),
    "measure_id": field(
        "STRING",
        "Measure ID",
        "CMS identifier for the mortality or complication measure.",
        nullable=False,
    ),
    "measure_name": field(
        "STRING",
        "Measure Name",
        "Descriptive name of the mortality or complication measure.",
    ),
    "compared_to_national": field(
        "STRING",
        "Compared to National",
        "Hospital performance compared with the national result.",
    ),
    "denominator": field(
        "INT64",
        "Denominator",
        "Number of eligible cases included in the measure.",
    ),
    "score": field(
        "FLOAT64",
        "Mortality Score",
        "CMS-reported mortality or complication score.",
    ),
    "lower_estimate": field(
        "FLOAT64",
        "Lower Estimate",
        "Lower bound of the reported statistical estimate.",
    ),
    "higher_estimate": field(
        "FLOAT64",
        "Higher Estimate",
        "Upper bound of the reported statistical estimate.",
    ),
    "start_date": field(
        "DATE",
        "Measure Start Date",
        "Beginning of the measure reporting period.",
    ),
    "end_date": field(
        "DATE",
        "Measure End Date",
        "End of the measure reporting period.",
    ),
}


HOSPITAL_TIMELY_EFFECTIVE_CARE_SCHEMA = {
    "facility_id": field(
        "STRING",
        "Facility ID",
        "Unique CMS identifier assigned to the hospital.",
        nullable=False,
    ),
    "facility_name": field(
        "STRING",
        "Facility Name",
        "Official name of the hospital.",
    ),
    "state": field(
        "STRING",
        "State",
        "Two-letter state or territory abbreviation.",
    ),
    "_condition": field(
        "STRING",
        "Clinical Condition",
        "Clinical or operational category associated with the measure.",
    ),
    "measure_id": field(
        "STRING",
        "Measure ID",
        "CMS identifier for the timely and effective care measure.",
        nullable=False,
    ),
    "measure_name": field(
        "STRING",
        "Measure Name",
        "Descriptive name of the timely and effective care measure.",
    ),
    "score": field(
        "FLOAT64",
        "Performance Score",
        "CMS-reported value for the measure.",
    ),
    "sample": field(
        "INT64",
        "Sample Size",
        "Number of cases included in the measure.",
    ),
    "start_date": field(
        "DATE",
        "Measure Start Date",
        "Beginning of the measure reporting period.",
    ),
    "end_date": field(
        "DATE",
        "Measure End Date",
        "End of the measure reporting period.",
    ),
}


HOSPITAL_HEALTHCARE_ASSOCIATED_INFECTIONS_SCHEMA = {
    "facility_id": field(
        "STRING",
        "Facility ID",
        "Unique CMS identifier assigned to the hospital.",
        nullable=False,
    ),
    "facility_name": field(
        "STRING",
        "Facility Name",
        "Official name of the hospital.",
    ),
    "state": field(
        "STRING",
        "State",
        "Two-letter state or territory abbreviation.",
    ),
    "measure_id": field(
        "STRING",
        "Measure ID",
        "CMS identifier for the infection measure.",
        nullable=False,
    ),
    "measure_name": field(
        "STRING",
        "Measure Name",
        "Descriptive name of the healthcare-associated infection measure.",
    ),
    "compared_to_national": field(
        "STRING",
        "Compared to National",
        "Hospital infection performance compared with the national result.",
    ),
    "score": field(
        "FLOAT64",
        "Infection Score",
        "CMS-reported infection performance score or ratio.",
    ),
    "start_date": field(
        "DATE",
        "Measure Start Date",
        "Beginning of the infection reporting period.",
    ),
    "end_date": field(
        "DATE",
        "Measure End Date",
        "End of the infection reporting period.",
    ),
}


HOSPITAL_OUTPATIENT_IMAGING_SCHEMA = {
    "facility_id": field(
        "STRING",
        "Facility ID",
        "Unique CMS identifier assigned to the hospital.",
        nullable=False,
    ),
    "facility_name": field(
        "STRING",
        "Facility Name",
        "Official name of the hospital.",
    ),
    "state": field(
        "STRING",
        "State",
        "Two-letter state or territory abbreviation.",
    ),
    "measure_id": field(
        "STRING",
        "Measure ID",
        "CMS identifier for the outpatient imaging measure.",
        nullable=False,
    ),
    "measure_name": field(
        "STRING",
        "Measure Name",
        "Descriptive name of the outpatient imaging efficiency measure.",
    ),
    "score": field(
        "FLOAT64",
        "Imaging Efficiency Score",
        "CMS-reported outpatient imaging efficiency value.",
    ),
    "start_date": field(
        "DATE",
        "Measure Start Date",
        "Beginning of the imaging measure reporting period.",
    ),
    "end_date": field(
        "DATE",
        "Measure End Date",
        "End of the imaging measure reporting period.",
    ),
}


HOSPITAL_VALUE_BASED_PURCHASING_SCHEMA = {
    "fiscal_year": field(
        "INT64",
        "Fiscal Year",
        "CMS fiscal year for the Value-Based Purchasing program.",
        nullable=False,
    ),
    "facility_id": field(
        "STRING",
        "Facility ID",
        "Unique CMS identifier assigned to the hospital.",
        nullable=False,
    ),
    "facility_name": field(
        "STRING",
        "Facility Name",
        "Official name of the hospital.",
    ),
    "state": field(
        "STRING",
        "State",
        "Two-letter state or territory abbreviation.",
    ),
    "unweighted_normalized_clinical_outcomes_domain_score": field(
        "FLOAT64",
        "Unweighted Clinical Outcomes Score",
        "Unweighted normalized clinical outcomes domain score.",
    ),
    "weighted_normalized_clinical_outcomes_domain_score": field(
        "FLOAT64",
        "Weighted Clinical Outcomes Score",
        "Weighted normalized clinical outcomes domain score.",
    ),
    "unweighted_person_and_community_engagement_domain_score": field(
        "FLOAT64",
        "Unweighted Engagement Score",
        "Unweighted person and community engagement domain score.",
    ),
    "weighted_person_and_community_engagement_domain_score": field(
        "FLOAT64",
        "Weighted Engagement Score",
        "Weighted person and community engagement domain score.",
    ),
    "unweighted_normalized_safety_domain_score": field(
        "FLOAT64",
        "Unweighted Safety Score",
        "Unweighted normalized hospital safety domain score.",
    ),
    "weighted_safety_domain_score": field(
        "FLOAT64",
        "Weighted Safety Score",
        "Weighted hospital safety domain score.",
    ),
    "unweighted_normalized_efficiency_and_cost_reduction_domain_score": field(
        "FLOAT64",
        "Unweighted Efficiency Score",
        "Unweighted efficiency and cost reduction domain score.",
    ),
    "weighted_efficiency_and_cost_reduction_domain_score": field(
        "FLOAT64",
        "Weighted Efficiency Score",
        "Weighted efficiency and cost reduction domain score.",
    ),
    "total_performance_score": field(
        "FLOAT64",
        "Total Performance Score",
        "Overall CMS Hospital Value-Based Purchasing performance score.",
    ),
}


HOSPITAL_HAC_REDUCTION_PROGRAM_SCHEMA = {
    "facility_id": field(
        "STRING",
        "Facility ID",
        "Unique CMS identifier assigned to the hospital.",
        nullable=False,
    ),
    "facility_name": field(
        "STRING",
        "Facility Name",
        "Official name of the hospital.",
    ),
    "state": field(
        "STRING",
        "State",
        "Two-letter state or territory abbreviation.",
    ),
    "fiscal_year": field(
        "INT64",
        "Fiscal Year",
        "CMS fiscal year for the HAC Reduction Program.",
        nullable=False,
    ),
    "psi_90_composite_value": field(
        "FLOAT64",
        "PSI-90 Composite Value",
        "Patient Safety Indicator 90 composite performance value.",
    ),
    "clabsi_sir": field(
        "FLOAT64",
        "CLABSI SIR",
        "Standardized infection ratio for central-line bloodstream infections.",
    ),
    "cauti_sir": field(
        "FLOAT64",
        "CAUTI SIR",
        "Standardized infection ratio for catheter-associated urinary infections.",
    ),
    "ssi_sir": field(
        "FLOAT64",
        "SSI SIR",
        "Standardized infection ratio for surgical-site infections.",
    ),
    "cdi_sir": field(
        "FLOAT64",
        "C. difficile SIR",
        "Standardized infection ratio for Clostridioides difficile infections.",
    ),
    "mrsa_sir": field(
        "FLOAT64",
        "MRSA SIR",
        "Standardized infection ratio for MRSA bloodstream infections.",
    ),
    "total_hac_score": field(
        "FLOAT64",
        "Total HAC Score",
        "Overall Hospital-Acquired Condition Reduction Program score.",
    ),
    "payment_reduction": field(
        "BOOL",
        "Payment Reduction",
        "Indicates whether the hospital is subject to a Medicare payment reduction.",
    ),
}


SCHEMA_REGISTRY = {
    "hospital_general_information": HOSPITAL_GENERAL_INFORMATION_SCHEMA,
    "hospital_readmissions": HOSPITAL_READMISSIONS_SCHEMA,
    "hospital_hcahps": HOSPITAL_HCAHPS_SCHEMA,
    "hospital_mortality": HOSPITAL_MORTALITY_SCHEMA,
    "hospital_timely_effective_care": (
        HOSPITAL_TIMELY_EFFECTIVE_CARE_SCHEMA
    ),
    "hospital_healthcare_associated_infections": (
        HOSPITAL_HEALTHCARE_ASSOCIATED_INFECTIONS_SCHEMA
    ),
    "hospital_outpatient_imaging_efficiency": (
        HOSPITAL_OUTPATIENT_IMAGING_SCHEMA
    ),
    "hospital_value_based_purchasing": (
        HOSPITAL_VALUE_BASED_PURCHASING_SCHEMA
    ),
    "hospital_hac_reduction_program": (
        HOSPITAL_HAC_REDUCTION_PROGRAM_SCHEMA
    ),
}