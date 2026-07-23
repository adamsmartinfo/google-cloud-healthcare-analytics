from langchain_core.messages import HumanMessage, ToolMessage

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from src.agents.graph import agent
from src.context.healthcare_metrics import (
    GENERAL_ANALYTICS_RULES,
    HEALTHCARE_METRICS,
)
from src.tools.bigquery.tools import run_bigquery_read_only_query


def test_metric_catalog() -> None:
    """Confirm the approved healthcare semantic layer is available."""
    assert len(HEALTHCARE_METRICS) == 5
    assert len(GENERAL_ANALYTICS_RULES) == 6

    assert (
        HEALTHCARE_METRICS["hospital_count"]["calculation"]
        == "COUNT(DISTINCT facility_id)"
    )

    assert (
        HEALTHCARE_METRICS[
            "average_value_based_purchasing_score"
        ]["source_column"]
        == "total_performance_score"
    )


def test_unapproved_table_is_blocked() -> None:
    """Confirm SQL cannot access a table outside the approved table list."""
    result = run_bigquery_read_only_query.invoke(
        {
            "sql": """
SELECT *
FROM healthcare_gold.fake_table
LIMIT 1
"""
        }
    )

    assert result["success"] is False
    assert result["error_type"] == "ValueError"
    assert "is not approved" in result["error_message"]


def test_healthcare_agent() -> None:
    """Run one representative healthcare analytics question end to end."""
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=(
                        "Which five states have the highest average "
                        "hospital overall rating? Include the number of "
                        "rated hospitals in each state."
                    )
                )
            ]
        }
    )

    messages = result["messages"]

    assert messages
    assert any(
        isinstance(message, ToolMessage)
        for message in messages
    )

    final_message = messages[-1]

    assert getattr(final_message, "content", None)
    assert final_message.content.strip()


def run_tests() -> None:
    """Run the Phase 3 regression checks without requiring pytest."""
    tests = [
        (
            "Healthcare metric catalog",
            test_metric_catalog,
        ),
        (
            "Unapproved table guardrail",
            test_unapproved_table_is_blocked,
        ),
        (
            "Healthcare agent end-to-end",
            test_healthcare_agent,
        ),
    ]

    failures = 0

    for test_name, test_function in tests:
        try:
            test_function()
            print(f"PASS: {test_name}")
        except Exception as exc:
            failures += 1
            print(f"FAIL: {test_name}")
            print(f"      {type(exc).__name__}: {exc}")

    print()
    print(f"Tests passed: {len(tests) - failures}")
    print(f"Tests failed: {failures}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    run_tests()