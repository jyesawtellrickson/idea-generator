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

from src.utils.api_helpers import get_arxiv_papers as query_arxiv
from src.agents.generator import gen_idea_generator_agent
from src.agents.evaluator import gen_evaluator_agent
from src.agents.control import gen_control_agent
from src.agents.chat import gen_chat_agent

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import pprint

import operator
from typing import Annotated

from src.utils.api_helpers import build_api_tools


def build_langgraph(args):
    """
    Build the langgraph pipeline.
    """

    class State(TypedDict):
        messages: Annotated[list, add_messages]
        ideas: Annotated[list[str], operator.add]

    graph_builder = StateGraph(State)
    memory = MemorySaver()

    tools = build_api_tools()[:1]
    # tools = [get_now, get_arxiv_papers]
    # tool_node = ToolNode(tools=tools)

    generator_agent = gen_idea_generator_agent(args, tools)
    evaluator_agent = gen_evaluator_agent(args, tools)
    control_agent = gen_control_agent(args, tools)
    chat_agent = gen_chat_agent(args, tools)

    # Add all the parts to the graph
    graph_builder.add_node("chat_agent", chat_agent)
    graph_builder.add_node("generator_agent", generator_agent)
    graph_builder.add_node("evaluator_agent", evaluator_agent)
    graph_builder.add_node("control_agent", control_agent)
    # graph_builder.add_node("tools", tool_node)

    # graph_builder.add_edge("control_agent", "generator_agent")
    # graph_builder.add_edge("control_agent", "chat_agent")
    # graph_builder.add_edge("control_agent", "evaluator_agent")
    # graph_builder.add_edge("generator_agent", "control_agent")
    # graph_builder.add_edge("evaluator_agent", "control_agent")
    # graph_builder.add_edge("tools", "generator_agent")
    graph_builder.add_edge(START, "control_agent")
    # graph_builder.add_edge("generator_agent", END)
    # graph_builder.add_edge("evaluate_agent", END)
    # graph_builder.add_edge("control_agent", END)
    graph_builder.add_edge("chat_agent", END)

    # The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
    # it is fine directly responding. This conditional routing defines the main agent loop.
    """graph_builder.add_conditional_edges(
        "generator_agent",
        tools_condition,
    )"""
    # Compile the graph and save image
    graph = graph_builder.compile(checkpointer=memory)
    image = graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)

    with open("graph_image.png", "wb") as f:
        f.write(image)

    return graph


def stream_graph_updates(graph, state, config):
    tool_results = []
    # Handle depth recursion error
    try:
        for state in graph.stream(state, config, stream_mode="values"):
            message = state["messages"][-1]
            if isinstance(message, ToolMessage):
                content = message.content
                if message.name == "arxiv_tool":
                    try:
                        content = json.loads(content)
                        content = [c.get("title") for c in content]
                    except:
                        content = content
                tool_results.append([message.name, content])
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()

        return state, tool_results
    except:
        return state, []


def run_langgraph(args, graph):
    """
    Run the langgraph pipeline.
    """

    ideas = []
    while True:
        state = {"messages": [], "ideas": ideas}
        user_input = input("\n\nUser: ")
        state["messages"].append(("user", user_input))
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        config = {"configurable": {"thread_id": "1"}, "recursion_limit": 5}
        state, _ = stream_graph_updates(graph, state, config)
        ideas = state.get("ideas", [])[:5]
        # print("\n\n######################################\n\n")
        # print("STATE:\n\n")
        # print(state)
        # print("\n\n################### Assistant Responded ###################\n\n")
        # print(state["messages"][-1].content)

        print("current ideas:\n\n")
        print(list(set(ideas)))
