from typing import Annotated
from datetime import datetime
from typing_extensions import TypedDict
from typing import Literal
import json

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph import END, START
from langchain_core.tools import tool
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from langchain_core.messages import ToolMessage
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

from src.utils.api_helpers import query_arxiv
from src.agents.generator import gen_idea_generator_agent
from src.agents.evaluator import gen_evaluate_idea_agent
from src.agents.control import gen_control_agent
from src.agents.chat import gen_chat_agent

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

import operator
from typing import Annotated


def build_langgraph(args):
    """
    Build the langgraph pipeline.
    """

    class State(TypedDict):
        messages: Annotated[list, add_messages]
        ideas: Annotated[list[str], operator.add]

    graph_builder = StateGraph(State)
    memory = MemorySaver()

    @tool
    def get_now(format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Get the current time, use python string formatting to change the format.
        """
        return datetime.now().strftime(format)

    @tool
    def get_arxiv_papers(keyword: str, num_results: int) -> list[dict]:
        """
        Fetches research papers from ArXiv.
        """
        return query_arxiv(keyword, num_results)

    tools = [get_now, get_arxiv_papers]
    tool_node = ToolNode(tools=tools)

    generator_agent = gen_idea_generator_agent(args, tools)
    evaluate_agent = gen_evaluate_idea_agent(args, tools)
    control_agent = gen_control_agent(args, tools)
    chat_agent = gen_chat_agent(args, tools)

    # Add all the parts to the graph
    graph_builder.add_node("chat_agent", chat_agent)
    graph_builder.add_node("generator_agent", generator_agent)
    graph_builder.add_node("evaluate_agent", evaluate_agent)
    graph_builder.add_node("control_agent", control_agent)
    graph_builder.add_node("tools", tool_node)

    # graph_builder.add_edge("generator_agent", "evaluate_agent")
    # graph_builder.add_edge("evaluate_agent", "evaluate_agent")
    graph_builder.add_edge("tools", "generator_agent")
    graph_builder.add_edge(START, "control_agent")
    # graph_builder.add_edge("generator_agent", END)
    # graph_builder.add_edge("evaluate_agent", END)
    graph_builder.add_edge("control_agent", END)
    graph_builder.add_edge("chat_agent", END)

    # The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
    # it is fine directly responding. This conditional routing defines the main agent loop.
    graph_builder.add_conditional_edges(
        "generator_agent",
        tools_condition,
    )
    # Compile the graph and save image
    graph = graph_builder.compile(checkpointer=memory)
    image = graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)

    with open("graph_image.png", "wb") as f:
        f.write(image)

    return graph


def run_langgraph(args, graph):
    """
    Run the langgraph pipeline.
    """

    def stream_graph_updates(state):
        config = {"configurable": {"thread_id": "1"}, "recursion_limit": 10}
        for event in graph.stream(state, config):
            for value in event.values():
                state["messages"] = value["messages"]
                state["ideas"] = value.get("ideas", [])
                # print("\n\n################### Assistant Responded ###################\n\n")
                # print("Assistant:", value["messages"][-1].content)
                if value.get("ideas"):
                    1
                    # print("\n\n################### Ideas ###################\n\n")
                    # print("Ideas:", value["ideas"])
        return state

    ideas = []
    while True:
        state = {"messages": [], "ideas": ideas}
        user_input = input("\n\nUser: ")
        state["messages"].append(("user", user_input))
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        state = stream_graph_updates(state)
        ideas = state["ideas"][:5]

        print("\n\n################### Assistant Responded ###################\n\n")
        print(state["messages"][-1].content)

        print("current ideas:\n\n")
        print(ideas)
