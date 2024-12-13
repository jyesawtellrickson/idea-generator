from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate

from src.utils.utils import extract_numbered_lines
from langgraph.types import Command

from src.utils.utils import get_next_node
from langgraph.graph import END, START

from typing import Literal
from typing_extensions import TypedDict


def format_ideas(ideas):
    return "\n".join([f"{i+1}. {idea}" for i, idea in enumerate(ideas)])


def gen_control_agent(args, tools):
    llm = ChatOllama(model=args.model)

    members = ["generator_agent", "evaluate_agent", "chat_agent"]
    members = ["generator_agent", "chat_agent"]
    options = members + ["FINISH"]

    prompt = ()

    prompt_full = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are the controller for a research idea generator that "
                f"consists of the members: {members}. Given the previous input "
                "from the user below, respond with the worker to act next. Each worker "
                "will perform their task and respond with their results and "
                "status. When finished, respond with FINISH."
                "IMPORTANT: respond only with the name of the next agent to act."
                "e.g. 'chat_agent', nothing else.",
            ),
            ("human", "{input}"),
        ]
    )

    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""

        next: Literal[*options]

    """def supervisor_node(state):
        messages = [
            {"role": "system", "content": prompt},
        ] + state["messages"]

        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]

        if goto == "FINISH":
            goto = END

        return Command(goto=goto)"""

    def supervisor_node_manual(state):
        """messages = [
            {"role": "system", "content": prompt},
        ] + state["messages"]
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                ("human", "{input}"),
            ]
        )"""
        chain = prompt_full | llm
        response = chain.invoke({"input": state["messages"][-1].content, "ideas": None})
        # print("RESPNSOE", response)
        # update = {"messages": state["messages"] + [response], "ideas": state["ideas"]}

        next_agent = response.content
        print("\n\nROUTING TO \n\n", next_agent)
        if "generator_agent" in next_agent:
            goto = "generator_agent"
        elif "evaluate_agent" in next_agent:
            goto = "evaluate_agent"
        elif "chat_agent" in next_agent:
            goto = "chat_agent"
        else:
            goto = "chat_agent"
        # goto = get_next_node(response, END)

        # if goto == "FINISH":
        #    goto = END
        return Command(update=state, goto=goto)

    return supervisor_node_manual
