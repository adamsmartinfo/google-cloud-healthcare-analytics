from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from src.tools.bigquery.metadata import (
    get_table_schema,
    list_datasets,
    list_tables,
)


@dataclass(frozen=True)
class WarehouseContext:
    """Cached metadata describing the available BigQuery warehouse."""

    datasets: tuple[str, ...]
    tables: dict[str, tuple[str, ...]]
    schemas: dict[str, tuple[dict[str, Any], ...]]


@lru_cache(maxsize=1)
def get_warehouse_context() -> WarehouseContext:
    """Load and cache BigQuery datasets, tables, and table schemas."""

    datasets = tuple(list_datasets())
    tables: dict[str, tuple[str, ...]] = {}
    schemas: dict[str, tuple[dict[str, Any], ...]] = {}

    for dataset_id in datasets:
        dataset_tables = tuple(list_tables(dataset_id))
        tables[dataset_id] = dataset_tables

        for table_id in dataset_tables:
            full_table_id = f"{dataset_id}.{table_id}"

            schema = get_table_schema(
                dataset_id=dataset_id,
                table_id=table_id,
            )

            schemas[full_table_id] = tuple(schema)

    return WarehouseContext(
        datasets=datasets,
        tables=tables,
        schemas=schemas,
    )

def format_warehouse_context(context: WarehouseContext) -> str:
    """Convert warehouse metadata into concise prompt-ready text."""

    lines: list[str] = ["Available BigQuery warehouse metadata:"]

    for dataset_id in context.datasets:
        lines.append(f"\nDataset: {dataset_id}")

        for table_id in context.tables.get(dataset_id, ()):
            full_table_id = f"{dataset_id}.{table_id}"
            lines.append(f"  Table: {full_table_id}")

            for column in context.schemas.get(full_table_id, ()):
                column_name = column["name"]
                column_type = column["type"]
                lines.append(f"    - {column_name}: {column_type}")

    return "\n".join(lines)

def format_dataset_context(
    context: WarehouseContext,
    dataset_id: str,
) -> str:
    """Convert one dataset's metadata into concise prompt-ready text."""

    dataset_tables = context.tables.get(dataset_id)

    if dataset_tables is None:
        raise ValueError(f"Dataset not found in warehouse context: {dataset_id}")

    lines: list[str] = [
        f"Available BigQuery warehouse metadata for dataset {dataset_id}:"
    ]

    for table_id in dataset_tables:
        full_table_id = f"{dataset_id}.{table_id}"
        lines.append(f"\nTable: {full_table_id}")

        for column in context.schemas.get(full_table_id, ()):
            lines.append(
                f"  - {column['name']}: {column['type']}"
            )

    return "\n".join(lines)