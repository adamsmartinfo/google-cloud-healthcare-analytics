from typing import Any


HEALTHCARE_METRICS: dict[str, dict[str, Any]] = {
    "hospital_count": {
        "display_name": "Hospital Count",
        "description": (
            "The number of distinct hospitals represented in the selected "
            "population."
        ),
        "preferred_table": "healthcare_gold.dim_hospital",
        "calculation": "COUNT(DISTINCT facility_id)",
        "aggregation_rule": "COUNT DISTINCT",
        "default_grain": "overall",
        "higher_is_better": None,
        "guidance": (
            "Use COUNT(DISTINCT facility_id) when joins or repeated rows could "
            "cause duplicate hospitals. Do not sum hospital identifiers."
        ),
    },
    "average_hospital_overall_rating": {
        "display_name": "Average Hospital Overall Rating",
        "description": (
            "The average CMS hospital overall rating among hospitals with a "
            "reported rating. Ratings range from 1 to 5 stars."
        ),
        "preferred_table": "healthcare_gold.dim_hospital",
        "source_column": "hospital_overall_rating",
        "calculation": "AVG(hospital_overall_rating)",
        "aggregation_rule": "AVERAGE",
        "default_grain": "state or hospital group",
        "higher_is_better": True,
        "guidance": (
            "Exclude NULL hospital ratings. Include the number of rated "
            "hospitals when comparing averages across groups. Do not sum "
            "hospital ratings."
        ),
    },
    "high_rated_hospital_percentage": {
        "display_name": "Percentage of Hospitals Rated 4 or 5 Stars",
        "description": (
            "The percentage of rated hospitals whose CMS hospital overall "
            "rating is 4 or 5 stars."
        ),
        "preferred_table": "healthcare_gold.dim_hospital",
        "source_column": "hospital_overall_rating",
        "calculation": (
            "SAFE_DIVIDE("
            "COUNTIF(hospital_overall_rating >= 4), "
            "COUNTIF(hospital_overall_rating IS NOT NULL)"
            ") * 100"
        ),
        "aggregation_rule": "PERCENTAGE",
        "default_grain": "state or hospital group",
        "higher_is_better": True,
        "guidance": (
            "The denominator must include only hospitals with a reported "
            "overall rating. Also return the rated-hospital count. Do not "
            "average hospital-level percentages."
        ),
    },
    "payment_reduction_rate": {
        "display_name": "Payment Reduction Rate",
        "description": (
            "The percentage of hospitals subject to a payment reduction in "
            "the hospital performance summary."
        ),
        "preferred_table": (
            "healthcare_gold.fact_hospital_performance_summary"
        ),
        "source_column": "payment_reduction",
        "calculation": (
            "SAFE_DIVIDE("
            "COUNTIF(payment_reduction = TRUE), "
            "COUNTIF(payment_reduction IS NOT NULL)"
            ") * 100"
        ),
        "aggregation_rule": "PERCENTAGE",
        "default_grain": "state or hospital group",
        "higher_is_better": False,
        "guidance": (
            "Clearly distinguish hospitals with payment reductions from "
            "hospitals with missing payment-reduction information. Do not "
            "average Boolean values directly."
        ),
    },
    "average_value_based_purchasing_score": {
        "display_name": "Average Value-Based Purchasing Score",
        "description": (
            "The average Value-Based Purchasing score among hospitals with "
            "a reported score."
        ),
        "preferred_table": (
            "healthcare_gold.fact_hospital_performance_summary"
        ),
        "source_column": "total_performance_score",
        "calculation": "AVG(total_performance_score)",
        "aggregation_rule": "AVERAGE",
        "default_grain": "state or hospital group",
        "higher_is_better": True,
        "guidance": (
            "Exclude NULL scores and include the number of hospitals with a "
            "reported score. Do not sum performance scores."
        ),
    },
}


GENERAL_ANALYTICS_RULES = [
    "Use only approved metric calculations when a requested metric matches the catalog.",
    "Do not aggregate text fields such as facility_name, city, state, or hospital_type.",
    "Do not sum ratings, percentages, or performance scores.",
    "Exclude NULL values when calculating averages unless the metric definition says otherwise.",
    "Include the relevant hospital count when comparing averages or percentages across groups.",
    "Use COUNT(DISTINCT facility_id) when duplicate hospital rows may be present.",
]


def format_healthcare_metric_catalog() -> str:
    """
    Format the healthcare metric catalog as compact text for an LLM prompt.

    Returns:
        A human-readable catalog containing approved metric definitions,
        calculations, preferred tables, aggregation rules, and guidance.
    """
    sections: list[str] = []

    rules_text = "\n".join(
        f"- {rule}"
        for rule in GENERAL_ANALYTICS_RULES
    )

    sections.append(
        "GENERAL ANALYTICS RULES\n"
        f"{rules_text}"
    )

    for metric_id, metric in HEALTHCARE_METRICS.items():
        section_lines = [
            f"Metric ID: {metric_id}",
            f"Display name: {metric['display_name']}",
            f"Description: {metric['description']}",
            f"Preferred table: {metric['preferred_table']}",
            f"Calculation: {metric['calculation']}",
            f"Aggregation rule: {metric['aggregation_rule']}",
            f"Default grain: {metric['default_grain']}",
        ]

        higher_is_better = metric.get("higher_is_better")

        if higher_is_better is True:
            section_lines.append(
                "Interpretation: Higher values are generally better."
            )
        elif higher_is_better is False:
            section_lines.append(
                "Interpretation: Lower values are generally better."
            )
        else:
            section_lines.append(
                "Interpretation: This is a descriptive count, not a quality measure."
            )

        source_column = metric.get("source_column")

        if source_column:
            section_lines.append(f"Source column: {source_column}")

        section_lines.append(f"Guidance: {metric['guidance']}")

        sections.append("\n".join(section_lines))

    return "\n\n".join(sections)