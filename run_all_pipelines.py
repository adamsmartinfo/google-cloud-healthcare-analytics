"""Orchestrate the complete CMS healthcare analytics pipeline."""

import logging
import sys
from datetime import datetime, timezone
from time import perf_counter
from typing import Callable

from src.pipelines.hospital_general_information.pipeline import (
    run_pipeline as run_general_information,
)
from src.pipelines.hospital_hac_reduction_program.pipeline import (
    run_pipeline as run_hac_reduction_program,
)
from src.pipelines.hospital_hcahps.pipeline import (
    run_pipeline as run_hcahps,
)
from src.pipelines.hospital_healthcare_associated_infections.pipeline import (
    run_pipeline as run_healthcare_associated_infections,
)
from src.pipelines.hospital_mortality.pipeline import (
    run_pipeline as run_mortality,
)
from src.pipelines.hospital_outpatient_imaging_efficiency.pipeline import (
    run_pipeline as run_outpatient_imaging_efficiency,
)
from src.pipelines.hospital_readmissions.pipeline import (
    run_pipeline as run_readmissions,
)
from src.pipelines.hospital_timely_effective_care.pipeline import (
    run_pipeline as run_timely_effective_care,
)
from src.pipelines.hospital_value_based_purchasing.pipeline import (
    run_pipeline as run_value_based_purchasing,
)
from src.warehouse.build_gold import (
    build_hospital_dimension,
    build_hospital_performance_summary,
)
from src.warehouse.build_silver import build_silver_tables


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


PipelineStep = tuple[str, Callable[[], None]]


PIPELINE_STEPS: list[PipelineStep] = [
    ("Hospital General Information", run_general_information),
    ("Hospital Readmissions", run_readmissions),
    ("Hospital HCAHPS", run_hcahps),
    ("Hospital Mortality", run_mortality),
    ("Hospital Timely and Effective Care", run_timely_effective_care),
    (
        "Hospital Healthcare-Associated Infections",
        run_healthcare_associated_infections,
    ),
    (
        "Hospital Outpatient Imaging Efficiency",
        run_outpatient_imaging_efficiency,
    ),
    (
        "Hospital Value-Based Purchasing",
        run_value_based_purchasing,
    ),
    (
        "Hospital HAC Reduction Program",
        run_hac_reduction_program,
    ),
]


def run_step(step_name: str, step_function: Callable[[], None]) -> None:
    """Run one pipeline step and log its elapsed time."""
    step_start = perf_counter()

    logger.info("Starting: %s", step_name)

    step_function()

    elapsed_seconds = perf_counter() - step_start
    logger.info(
        "Completed: %s in %.2f seconds",
        step_name,
        elapsed_seconds,
    )


def run_all() -> None:
    """Run ingestion, Silver, and Gold layers in sequence."""
    platform_start = perf_counter()
    started_at = datetime.now(timezone.utc)

    logger.info("=" * 72)
    logger.info("Starting CMS healthcare analytics platform refresh")
    logger.info("UTC start time: %s", started_at.isoformat())
    logger.info("=" * 72)

    for step_name, step_function in PIPELINE_STEPS:
        run_step(step_name, step_function)

    run_step("Build Silver Tables", build_silver_tables)
    run_step("Build Gold Hospital Dimension", build_hospital_dimension)
    run_step(
        "Build Gold Hospital Performance Summary",
        build_hospital_performance_summary,
    )

    completed_at = datetime.now(timezone.utc)
    total_seconds = perf_counter() - platform_start

    logger.info("=" * 72)
    logger.info("CMS healthcare analytics platform refresh succeeded")
    logger.info("UTC completion time: %s", completed_at.isoformat())
    logger.info("Total elapsed time: %.2f seconds", total_seconds)
    logger.info("=" * 72)


def main() -> int:
    """Run the platform refresh and return an operating-system exit code."""
    try:
        run_all()
        return 0
    except Exception:
        logger.exception(
            "CMS healthcare analytics platform refresh failed."
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
