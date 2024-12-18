from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate

from src.utils.utils import extract_numbered_lines
from langgraph.types import Command

from src.utils.utils import get_next_node
from langgraph.graph import END, START

from src.utils.utils import format_ideas

import pprint


def gen_chat_agent(args, tools):
    llm = ChatOllama(model=args.model)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are the chat agent for a research idea generator that"
                " also consists of a generator_agent, evaluator_agent and router."
                " The goal of the system is to help the user generate"
                " innovative research ideas."
                " Your jobs include reading all AIMessages and using that"
                " information to respond to the last HumanMessage from the"
                " user."
                " Initially, you should get information from the user about the"
                " topics they're interested in doing research on."
                " When the generator_agent has generated some ideas, you"
                " should feed those ideas back to the user as well as ask the"
                " user if (1) they like any of the ideas and would like to"
                " further refine them, or (2) they don't like any of the ideas"
                " and would like to generate even more."
                " IMPORTANT: It is important that you do not generate ideas yourself, you"
                " should just generate the text to talk to the user. There are"
                " other agents to do the generation and evaluation of ideas."
                " Keep suggested ideas to five or less."
                " The ideas so far can be found in the message history."
                " These also include: {ideas}",
            ),
            ("placeholder", "{conversation}"),
        ]
    )

    chain = prompt | llm

    def chatbot(state):
        # print("\n\nChat input")
        # pprint.pprint(state)
        try:
            response = chain.invoke(
                {
                    "conversation": state["messages"][-5:],
                    "ideas": format_ideas(list(set(state["ideas"]))),
                }
            )
            update = {"messages": state["messages"] + [response], "ideas": state["ideas"]}

        except Exception as e:
            update = {"messages": state["messages"] + [f"Error: {e}"], "ideas": []}

        return Command(
            update=update,
            goto=END,  # "control_agent",  # get_next_node(update["messages"][-1], END),
        )

    return chatbot
