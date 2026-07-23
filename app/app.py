import ast
import json
import sys
from pathlib import Path
from typing import Any

import altair as alt
import pandas as pd
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


# -------------------------------------------------------------------
# Make the project root importable when Streamlit runs app/app.py
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.agents.graph import agent


# -------------------------------------------------------------------
# Page configuration
# -------------------------------------------------------------------
st.set_page_config(
    page_title="AI Hospital Researcher Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------------------------------------------------------------
# Styling
# -------------------------------------------------------------------
st.markdown(
    """
<style>
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero-container {
        padding: 1.6rem 1.8rem;
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2.15rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        line-height: 1.6;
        opacity: 0.85;
        margin-bottom: 0;
    }

    .status-card {
        padding: 0.9rem 1rem;
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    .status-label {
        font-size: 0.78rem;
        font-weight: 600;
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 0.05rem;
    }

    .status-value {
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 0.2rem;
    }

    .section-description {
        opacity: 0.75;
        margin-top: -0.5rem;
        margin-bottom: 1rem;
    }

    div[data-testid="stChatMessage"] {
        border: 1px solid rgba(128, 128, 128, 0.18);
        border-radius: 14px;
        padding: 0.25rem 0.5rem;
        margin-bottom: 0.75rem;
    }

    div.stButton > button {
        border-radius: 10px;
        min-height: 3.2rem;
        white-space: normal;
        text-align: left;
    }
</style>
""",
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# Agent and tool-message helpers
# -------------------------------------------------------------------
def parse_tool_content(content: Any) -> dict[str, Any] | None:
    """Convert LangChain tool-message content into a dictionary."""

    if isinstance(content, dict):
        return content

    if not isinstance(content, str):
        return None

    try:
        parsed_content = json.loads(content)

        if isinstance(parsed_content, dict):
            return parsed_content

    except json.JSONDecodeError:
        pass

    try:
        parsed_content = ast.literal_eval(content)

        if isinstance(parsed_content, dict):
            return parsed_content

    except (ValueError, SyntaxError):
        pass

    return None


def extract_generated_sql(messages: list[Any]) -> str | None:
    """
    Extract the most recent BigQuery SQL statement from an AI tool call.

    This is a fallback in case the successful ToolMessage does not
    contain the SQL statement.
    """

    for message in reversed(messages):
        if not isinstance(message, AIMessage):
            continue

        for tool_call in reversed(message.tool_calls or []):
            if tool_call.get("name") != "run_bigquery_read_only_query":
                continue

            arguments = tool_call.get("args", {})
            sql = arguments.get("sql")

            if isinstance(sql, str) and sql.strip():
                return sql.strip()

    return None


def extract_query_details(
    messages: list[Any],
) -> tuple[str | None, list[dict[str, Any]]]:
    """Extract the latest successful SQL statement and query results."""

    for message in reversed(messages):
        if not isinstance(message, ToolMessage):
            continue

        if message.name != "run_bigquery_read_only_query":
            continue

        payload = parse_tool_content(message.content)

        if not payload or payload.get("success") is not True:
            continue

        sql = payload.get("sql")
        results = payload.get("results", [])

        if not isinstance(sql, str) or not sql.strip():
            sql = None

        if not isinstance(results, list):
            results = []

        valid_results = [
            row
            for row in results
            if isinstance(row, dict)
        ]

        return sql, valid_results

    return None, []


def get_agent_response(
    question: str,
) -> tuple[str, str | None, list[dict[str, Any]]]:
    """
    Send a question to the LangGraph agent.

    Returns:
        - Final natural-language answer
        - Executed BigQuery SQL
        - Returned BigQuery rows
    """

    result = agent.invoke(
        {
            "messages": [
                HumanMessage(content=question),
            ]
        }
    )

    messages = result.get("messages", [])

    generated_sql, query_results = extract_query_details(messages)

    if generated_sql is None:
        generated_sql = extract_generated_sql(messages)

    for message in reversed(messages):
        if not isinstance(message, AIMessage):
            continue

        if not message.content:
            continue

        if isinstance(message.content, str):
            response = message.content
        else:
            response = str(message.content)

        return response, generated_sql, query_results

    raise RuntimeError(
        "The healthcare analytics agent returned no final response."
    )


# -------------------------------------------------------------------
# Session-state helpers
# -------------------------------------------------------------------
def initial_messages() -> list[dict[str, Any]]:
    """Return the initial Streamlit chat history."""

    return [
        {
            "role": "assistant",
            "content": (
                "Welcome to the AI Hospital Researcher Assistant. "
                "Ask a question about CMS hospital performance, patient "
                "experience, ratings, mortality, readmissions, or "
                "value-based purchasing."
            ),
            "sql": None,
            "results": [],
        }
    ]


# -------------------------------------------------------------------
# Dataframe and chart helpers
# -------------------------------------------------------------------
def build_results_dataframe(
    query_results: list[dict[str, Any]],
) -> pd.DataFrame:
    """Convert BigQuery result rows into a display-ready dataframe."""

    if not query_results:
        return pd.DataFrame()

    dataframe = pd.DataFrame(query_results)

    for column in dataframe.columns:
        if pd.api.types.is_bool_dtype(dataframe[column]):
            continue

        if pd.api.types.is_numeric_dtype(dataframe[column]):
            continue

        converted_column = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

        non_null_original = dataframe[column].notna().sum()
        non_null_converted = converted_column.notna().sum()

        if (
            non_null_original > 0
            and non_null_converted == non_null_original
        ):
            dataframe[column] = converted_column

    return dataframe


def format_column_label(column_name: str) -> str:
    """Convert a warehouse column name into a readable chart label."""

    label = column_name.replace("_", " ").strip()

    replacements = {
        "cms": "CMS",
        "id": "ID",
        "vbp": "VBP",
        "hcahps": "HCAHPS",
    }

    words = []

    for word in label.split():
        replacement = replacements.get(word.lower())

        if replacement:
            words.append(replacement)
        else:
            words.append(word.capitalize())

    return " ".join(words)


def get_chart_columns(
    dataframe: pd.DataFrame,
) -> tuple[list[str], list[str]]:
    """Identify numeric and categorical columns in query results."""

    numeric_columns = [
        column
        for column in dataframe.select_dtypes(include="number").columns
        if not pd.api.types.is_bool_dtype(dataframe[column])
    ]

    category_columns = [
        column
        for column in dataframe.columns
        if column not in numeric_columns
    ]

    return numeric_columns, category_columns


def select_primary_metric(numeric_columns: list[str]) -> str | None:
    """
    Select the most meaningful numeric column for visualization.

    Analytical measures such as averages, ratings, scores, rates, and
    percentages are preferred over supporting fields such as counts.
    """

    if not numeric_columns:
        return None

    preferred_keywords = [
        "average",
        "avg",
        "rating",
        "score",
        "rate",
        "percent",
        "percentage",
        "amount",
        "value",
        "measure",
    ]

    supporting_keywords = [
        "count",
        "number",
        "total",
        "row_count",
        "hospital_count",
        "rated_hospital_count",
    ]

    for keyword in preferred_keywords:
        for column in numeric_columns:
            if keyword in column.lower():
                return column

    for column in numeric_columns:
        if not any(
            keyword in column.lower()
            for keyword in supporting_keywords
        ):
            return column

    return numeric_columns[0]


def select_category_column(category_columns: list[str]) -> str | None:
    """Select the most useful categorical column for chart labels."""

    if not category_columns:
        return None

    preferred_keywords = [
        "state",
        "hospital",
        "facility",
        "ownership",
        "category",
        "region",
        "city",
        "name",
        "type",
    ]

    for keyword in preferred_keywords:
        for column in category_columns:
            if keyword in column.lower():
                return column

    return category_columns[0]


def build_bar_chart(
    dataframe: pd.DataFrame,
    category_column: str,
    value_column: str,
) -> alt.Chart | None:
    """Build a descending horizontal bar chart."""

    chart_dataframe = dataframe[
        [category_column, value_column]
    ].copy()

    chart_dataframe[category_column] = (
        chart_dataframe[category_column]
        .fillna("Unknown")
        .astype(str)
    )

    chart_dataframe = chart_dataframe.dropna(
        subset=[value_column]
    )

    if chart_dataframe.empty:
        return None

    chart_dataframe = (
        chart_dataframe
        .sort_values(
            by=value_column,
            ascending=False,
        )
        .head(20)
    )

    category_label = format_column_label(category_column)
    value_label = format_column_label(value_column)
    chart_title = f"{value_label} by {category_label}"

    chart_height = max(
        300,
        min(len(chart_dataframe) * 38, 700),
    )

    return (
        alt.Chart(chart_dataframe)
        .mark_bar()
        .encode(
            x=alt.X(
                f"{value_column}:Q",
                title=value_label,
            ),
            y=alt.Y(
                f"{category_column}:N",
                title=category_label,
                sort=alt.EncodingSortField(
                    field=value_column,
                    order="descending",
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    f"{category_column}:N",
                    title=category_label,
                ),
                alt.Tooltip(
                    f"{value_column}:Q",
                    title=value_label,
                    format=",.2f",
                ),
            ],
        )
        .properties(
            title=chart_title,
            height=chart_height,
        )
    )


def build_line_chart(
    dataframe: pd.DataFrame,
    numeric_columns: list[str],
) -> alt.Chart | None:
    """Build a line chart for numeric-only query results."""

    value_columns = numeric_columns[:3]

    chart_dataframe = (
        dataframe[value_columns]
        .copy()
        .head(20)
        .reset_index(drop=True)
    )

    chart_dataframe["result_order"] = (
        chart_dataframe.index + 1
    )

    melted_dataframe = chart_dataframe.melt(
        id_vars="result_order",
        value_vars=value_columns,
        var_name="metric",
        value_name="value",
    )

    melted_dataframe["metric"] = melted_dataframe[
        "metric"
    ].map(format_column_label)

    if melted_dataframe["value"].dropna().empty:
        return None

    if len(value_columns) == 1:
        value_label = format_column_label(value_columns[0])
        chart_title = f"{value_label} by Result Order"
    else:
        value_label = "Value"
        chart_title = "Query Results by Result Order"

    return (
        alt.Chart(melted_dataframe)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "result_order:Q",
                title="Result Order",
                axis=alt.Axis(tickMinStep=1),
            ),
            y=alt.Y(
                "value:Q",
                title=value_label,
            ),
            color=alt.Color(
                "metric:N",
                title="Metric",
            ),
            tooltip=[
                alt.Tooltip(
                    "result_order:Q",
                    title="Result Order",
                    format=".0f",
                ),
                alt.Tooltip(
                    "metric:N",
                    title="Metric",
                ),
                alt.Tooltip(
                    "value:Q",
                    title=value_label,
                    format=",.2f",
                ),
            ],
        )
        .properties(
            title=chart_title,
            height=400,
        )
    )


def render_automatic_chart(dataframe: pd.DataFrame) -> None:
    """
    Render a chart inside a collapsed dropdown when results are suitable.

    Category plus numeric results produce a descending horizontal bar chart.
    Numeric-only results produce a line chart based on result order.
    """

    if dataframe.empty or len(dataframe) < 2:
        return

    numeric_columns, category_columns = get_chart_columns(dataframe)

    if not numeric_columns:
        return

    if category_columns:
        category_column = select_category_column(category_columns)
        value_column = select_primary_metric(numeric_columns)

        if category_column is None or value_column is None:
            return

        chart = build_bar_chart(
            dataframe=dataframe,
            category_column=category_column,
            value_column=value_column,
        )

        if chart is None:
            return

        with st.expander("View visualization"):
            st.altair_chart(
                chart,
                use_container_width=True,
            )

            if len(dataframe) > 20:
                st.caption(
                    "The visualization displays the 20 highest values. "
                    "The complete results are available in the query-results "
                    "table."
                )
            else:
                st.caption(
                    "Results are sorted from largest to smallest."
                )

        return

    chart = build_line_chart(
        dataframe=dataframe,
        numeric_columns=numeric_columns,
    )

    if chart is None:
        return

    with st.expander("View visualization"):
        st.altair_chart(
            chart,
            use_container_width=True,
        )

        st.caption(
            "The visualization displays numeric values in the order "
            "returned by the query."
        )


# -------------------------------------------------------------------
# Chat display helpers
# -------------------------------------------------------------------
def display_query_details(
    generated_sql: str | None,
    query_results: list[dict[str, Any]],
) -> None:
    """Display visualization, returned rows, and generated SQL."""

    results_dataframe = build_results_dataframe(query_results)

    if not results_dataframe.empty:
        render_automatic_chart(results_dataframe)

        with st.expander(
            f"View query results ({len(results_dataframe):,} rows)"
        ):
            st.dataframe(
                results_dataframe,
                use_container_width=True,
                hide_index=True,
            )

    if generated_sql:
        with st.expander("View generated SQL"):
            st.code(generated_sql, language="sql")


def display_chat_message(message: dict[str, Any]) -> None:
    """Display a saved chat message and its query details."""

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        display_query_details(
            generated_sql=message.get("sql"),
            query_results=message.get("results", []),
        )


# -------------------------------------------------------------------
# Session state
# -------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = initial_messages()


# -------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------
with st.sidebar:
    st.title("🏥 Hospital Research")

    st.caption(
        "A portfolio project demonstrating data engineering, "
        "analytics engineering, and agentic AI."
    )

    st.markdown(
        """
<div class="status-card">
<div class="status-label">Application Status</div>
<div class="status-value">🟢 Agent Ready</div>
</div>

<div class="status-card">
<div class="status-label">Data Platform</div>
<div class="status-value">Google BigQuery</div>
</div>

<div class="status-card">
<div class="status-label">Data Source</div>
<div class="status-value">CMS Hospital Data</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.subheader("Technology")

    st.markdown(
        """
- Python
- Streamlit
- LangGraph
- OpenAI
- Google BigQuery
"""
    )

    st.divider()

    st.caption(
        "Answers are generated from approved healthcare warehouse tables. "
        "Results should be independently validated before operational use."
    )

    if st.button(
        "Clear conversation",
        use_container_width=True,
        type="secondary",
    ):
        st.session_state.messages = initial_messages()
        st.rerun()


# -------------------------------------------------------------------
# Hero section
# -------------------------------------------------------------------
st.markdown(
    """
<div class="hero-container">
<div class="hero-title">🏥 AI Hospital Researcher Assistant</div>
<div class="hero-subtitle">
Explore CMS hospital performance data using natural-language questions.
The application uses a governed LangGraph agent to generate read-only SQL,
query Google BigQuery, and explain the results in business-friendly language.
</div>
</div>
""",
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# Capability overview
# -------------------------------------------------------------------
capability_columns = st.columns(3)

with capability_columns[0]:
    st.metric(
        label="Hospitals",
        value="5,432",
        help="Distinct hospitals represented in the hospital dimension.",
    )

with capability_columns[1]:
    st.metric(
        label="Approved Gold Tables",
        value="2",
        help="The agent is restricted to approved Gold-layer tables.",
    )

with capability_columns[2]:
    st.metric(
        label="Query Access",
        value="Read Only",
        help="The application does not permit data modification queries.",
    )


st.divider()


# -------------------------------------------------------------------
# Suggested questions
# -------------------------------------------------------------------
st.subheader("Suggested Questions")

st.markdown(
    """
<div class="section-description">
Select a question below or enter your own question in the chat box.
</div>
""",
    unsafe_allow_html=True,
)

suggested_questions = [
    "Which states have the highest average hospital ratings?",
    "Show the highest-rated hospitals in Utah.",
    "Which states have the strongest patient experience scores?",
    "How many hospitals are represented in the dataset?",
]

selected_question = None
question_columns = st.columns(2)

for index, question in enumerate(suggested_questions):
    with question_columns[index % 2]:
        if st.button(
            question,
            key=f"suggested_question_{index}",
            use_container_width=True,
        ):
            selected_question = question


st.divider()


# -------------------------------------------------------------------
# Chat
# -------------------------------------------------------------------
st.subheader("Hospital Research Chat")

st.markdown(
    """
<div class="section-description">
Responses may take several seconds while the agent generates,
validates, and executes a BigQuery query.
</div>
""",
    unsafe_allow_html=True,
)

for saved_message in st.session_state.messages:
    display_chat_message(saved_message)


typed_question = st.chat_input(
    "Ask a hospital analytics question..."
)

user_question = selected_question or typed_question

if user_question:
    user_message = {
        "role": "user",
        "content": user_question,
        "sql": None,
        "results": [],
    }

    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner(
            "Generating and validating the hospital analysis..."
        ):
            try:
                response, generated_sql, query_results = get_agent_response(
                    user_question
                )

                st.markdown(response)

                display_query_details(
                    generated_sql=generated_sql,
                    query_results=query_results,
                )

            except Exception as error:
                generated_sql = None
                query_results = []

                response = (
                    "I could not complete that analysis. Please try another "
                    "hospital research question.\n\n"
                    f"Technical details: "
                    f"`{type(error).__name__}: {error}`"
                )

                st.error(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "sql": generated_sql,
            "results": query_results,
        }
    )
