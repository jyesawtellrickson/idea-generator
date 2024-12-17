from datetime import datetime
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from langgraph.checkpoint.memory import MemorySaver

from src.agents.generator import gen_idea_generator_agent

import argparse


def check_weather(location: str, at_time: datetime | None = None) -> str:
    """Return the weather forecast for the specified location."""
    return f"It's always sunny in {location}"


tools = [check_weather]
model = ChatOllama(model="mistral")


def test_simple_react_agent():
    system_prompt = "You are a helpful bot named Fred."
    graph = create_react_agent(model, tools, state_modifier=system_prompt)
    inputs = {"messages": [("user", "What's your name? And what's the weather in SF?")]}
    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

    assert "sunny" in message.content
    assert "Fred" in message.content


def test_manual_memory_agent():
    system_prompt = "You are a helpful bot named Fred."
    graph = create_react_agent(model, tools, state_modifier=system_prompt)
    inputs = {
        "messages": [
            ("user", "My name is Bob."),
            ("ai", "Nice to meet you, Bob."),
            ("user", "What is my name?"),
        ]
    }
    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

    assert "Fred" in message.content
    assert "Bob" in message.content


def test_memory_agent():
    graph = create_react_agent(model, tools, checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "thread-1"}}

    def print_stream(graph, inputs, config):
        for s in graph.stream(inputs, config, stream_mode="values"):
            message = s["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()
        return message

    inputs = {"messages": [("user", "What's the weather in SF?")]}
    message = print_stream(graph, inputs, config)
    assert "sunny" in message.content.lower()

    inputs3 = {"messages": [("user", "So where do I live?")]}
    message = print_stream(graph, inputs3, config)
    assert "sf" in message.content.lower() or "francisco" in message.content.lower()

    inputs2 = {"messages": [("user", "Cool, so then should i go biking today?")]}
    message = print_stream(graph, inputs2, config)
    assert "sunny" in message.content.lower()
    assert "sf" in message.content.lower()


def test_generator_agent():
    parser = argparse.ArgumentParser(description="Generate Research Ideas")
    parser.add_argument("--model", type=str, default="mistral", choices=["mistral", "qwen2.5:14b"])
    args = parser.parse_args()

    tools = []

    agent = gen_idea_generator_agent(args, tools)
    response = agent.invoke("hello")
    print(response)
