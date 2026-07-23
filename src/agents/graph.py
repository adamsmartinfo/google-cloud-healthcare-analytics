from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from src.agents.nodes import BIGQUERY_TOOLS, call_model
from src.agents.state import AgentState


workflow = StateGraph(AgentState)

workflow.add_node("model", call_model)
workflow.add_node("tools", ToolNode(BIGQUERY_TOOLS))

workflow.add_edge(START, "model")

workflow.add_conditional_edges(
    "model",
    tools_condition,
)

workflow.add_edge("tools", "model")

agent = workflow.compile()