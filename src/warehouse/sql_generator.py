from src.warehouse.schemas import SCHEMA_REGISTRY


LANDING_DATASET = "healthcare_data"
SILVER_DATASET = "healthcare_silver"


def build_select_expression(column_name, field_definition):
    data_type = field_definition["type"]

    if data_type == "STRING":
        return f"TRIM({column_name}) AS {column_name}"

    if data_type == "BOOL":
        return (
            "CASE "
            f"WHEN LOWER(TRIM({column_name})) IN ('yes', 'true', '1') THEN TRUE "
            f"WHEN LOWER(TRIM({column_name})) IN ('no', 'false', '0') THEN FALSE "
            f"ELSE NULL END AS {column_name}"
        )

    if data_type == "DATE":
        return f"SAFE_CAST({column_name} AS DATE) AS {column_name}"

    return f"SAFE_CAST({column_name} AS {data_type}) AS {column_name}"


def generate_silver_table_sql(project_id, table_name):
    schema = SCHEMA_REGISTRY[table_name]

    select_expressions = [
        build_select_expression(column_name, field_definition)
        for column_name, field_definition in schema.items()
    ]

    formatted_columns = ",\n    ".join(select_expressions)

    return f"""
CREATE OR REPLACE TABLE `{project_id}.{SILVER_DATASET}.{table_name}` AS
SELECT
    {formatted_columns}
FROM `{project_id}.{LANDING_DATASET}.{table_name}`;
""".strip()