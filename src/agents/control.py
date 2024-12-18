from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate

from src.utils.utils import extract_numbered_lines
from langgraph.types import Command

from src.utils.utils import get_next_node
from langgraph.graph import END, START

from typing import Literal
from typing_extensions import TypedDict
from typing import Optional

from langgraph.graph import MessagesState

import pprint


def format_ideas(ideas):
    return "\n".join([f"{i+1}. {idea}" for i, idea in enumerate(ideas)])


def gen_control_agent(args, tools):
    llm = ChatOllama(model=args.model)

    members = ["generator_agent", "evaluate_agent", "chat_agent"]
    members = ["generator_agent", "chat_agent"]
    options = members  # + ["FINISH"]

    prompt_full = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are the controller for a research idea generator that"
                f" consists of the members: {members}. Given the previous input"
                " from the user and agents, respond with the worker to act "
                " next. Each worker will perform their task."
                " You should always use chat agent to respond to the user."
                " If there is enough information to start generating ideas,"
                " then route to generator_agent. If there are already ideas"
                " then route to the chat_agent."
                " Don't continually route to the generator agent."
                " If you're unsure, route to chat_agent and it can get more"
                " information from the user.",
            ),
            ("placeholder", "{conversation}"),
        ]
    )

    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""

        next: Literal[*options]
        ideas: Optional[list[str]]

    def supervisor_node(state: MessagesState):  # -> Command[Literal[*options]]:
        messages = prompt_full.invoke({"conversation": state["messages"][-3:]})
        # print("Control input")
        # pprint.pprint(messages)

        num_retries = 5
        i = 0
        response = None
        while response is None and i < num_retries:
            response = llm.with_structured_output(Router).invoke(messages)
            i += 1

        # print("Control Response", response)
        if response is None:
            print("Routing failed")
            goto = "chat_agent"  # END  # "chat_agent"
        else:
            # print(response)
            # print(response.get("ideas"))

            state["ideas"] = response.get("ideas", [])
            goto = response["next"]

        if goto == "FINISH":
            goto = END

        print(f"\n\nRouting to {goto}")
        return Command(update=state, goto=goto)

    return supervisor_node
