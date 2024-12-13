from datetime import datetime
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool


from src.utils.api_helpers import query_arxiv


def build_graph(args):
    @tool
    def get_arxiv_papers(keyword: str, num_results: int = 10) -> list[dict]:
        """
        Fetches the latest research papers from ArXiv.
        Covers many topics including computer science, physics, math, etc.
        """
        return query_arxiv(keyword, num_results)

    @tool
    def review_ideas(ideas: str) -> str:
        """
        Gives feedback on any generated ideas.
        :param ideas: The generated ideas, it should be the full ideas as currently understood.
        """
        system_prompt = (
            "You are reviewing the research ideas generated by an LLM."
            " Please provide feedback on the ideas. Be critical, no need"
            " to be overly positive. You should suggest improvements."
            " You can use the tools available to aid in your review."
        )
        model = ChatOllama(model=args.model)
        graph = create_react_agent(model, [get_arxiv_papers], state_modifier=system_prompt)
        inputs = {"messages": [("user", ideas)]}
        for s in graph.stream(inputs, stream_mode="values"):
            message = s["messages"][-1]
        # return f"Reviewing the ideas: {ideas}"
        return message.content

    tools = [get_arxiv_papers, review_ideas]
    model = ChatOllama(model=args.model)

    system_prompt = (
        "You are a good conversational chat agent that helps generate ideas."
        " When generating ideas, don't generate more than 5."
        # " When you suggest ideas, share the pros and cons."
        # " Focus on impact of the work, novelty and feasibility."
        " If you're suggesting ideas, make sure to look at current"
        " research, don't just suggest random ideas."
        " Do talk to and engage the user, don't just return a list."
        " IMPORTANT: always use the arXiv API to get the latest research."
        " IMPORTANT: if the user asks for reading, always use the arXiv API."
    )
    system_prompt = "You are a helpful chat agent."

    # system_prompt="Use the arxiv papers tool"

    graph = create_react_agent(
        model, tools, checkpointer=MemorySaver(), state_modifier=system_prompt
    )
    return graph


def print_stream(graph, inputs, config):
    for s in graph.stream(inputs, config, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
    return message


def run_basic(args):

    graph = build_graph(args)

    config = {"configurable": {"thread_id": "thread-1"}}

    init_message = (
        "\n\n---------------------------------------\n"
        "Welcome to the research idea generator!"
        " Please tell me about the area of research you're interested in to"
        " get started."
        "\n\nYou can quit by typing 'quit' or 'exit'."
    )
    print(init_message)
    init = True
    while True:
        user_input = input("\nUser: ")
        if init:
            inputs = {"messages": [("ai", init_message), ("user", user_input)]}
        else:
            inputs = {"messages": [("user", user_input)]}

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        print_stream(graph, inputs, config)
        init = False
