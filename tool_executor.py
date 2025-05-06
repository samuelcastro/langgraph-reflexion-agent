from dotenv import load_dotenv

load_dotenv()

# The TavilySearch tool is a tool that can be used to search the web
from langchain_tavily import TavilySearch

# The StructuredTool will will created a tool that can be used to search the web
from langchain_core.tools import StructuredTool

# A node that runs the tools called in the last AIMessage.
# It can be used either in StateGraph with a "messages" state key
# (or a custom key passed via ToolNode's 'messages_key').
# If multiple tool calls are requested, they will be run in parallel.
# The output will be a list of ToolMessages, one for each tool call.
# More: https://langchain-ai.github.io/langgraph/reference/agents/?h=toolnode#langgraph.prebuilt.tool_node.ToolNode
# It essentially look in the state for the messages_key checking the last AIMessage to
# see if there any any tool calls. If there are, it will run them in parallel.
from langgraph.prebuilt import ToolNode
from schemas import AnswerQuestion, ReviseAnswer

tavily_tool = TavilySearch(max_results=5)


def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries"""
    return tavily_tool.batch([{"query": query} for query in search_queries])


execute_tools = ToolNode(
    [
        StructuredTool.from_function(run_queries, name=AnswerQuestion.__name__),
        StructuredTool.from_function(run_queries, name=ReviseAnswer.__name__),
    ]
)
