from dotenv import load_dotenv
from typing import List
from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph

from chains import revisor, first_responder
from tool_node_executor import execute_tools

load_dotenv()

MAX_ITERATIONS = 2

DRAFT="draft"
EXECUTE_TOOLS="execute_tools"
REVISOR="revise"

builder = MessageGraph()
builder.add_node(DRAFT, first_responder)
builder.add_node(EXECUTE_TOOLS, execute_tools)
builder.add_node(REVISOR, revisor)
builder.add_edge(DRAFT, EXECUTE_TOOLS)
builder.add_edge(EXECUTE_TOOLS, REVISOR)


def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    if count_tool_visits > MAX_ITERATIONS:
        return END
    return EXECUTE_TOOLS

builder.add_conditional_edges(REVISOR, event_loop)
builder.set_entry_point(DRAFT)
graph = builder.compile()

print(graph.get_graph().draw_ascii())
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

print()
if __name__ == "__main__":
    print('Starting graph...')

    res = graph.invoke(
        "Write about AI-powered SCO/autonomous soc problem domain, list startups that do that and raised capital."
    )

    print(res[-1].tool_calls[0]["args"]["answer"])
    print(res)


