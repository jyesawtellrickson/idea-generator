from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate

from src.utils.utils import extract_numbered_lines
from langgraph.types import Command

from src.utils.utils import get_next_node, format_ideas
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from typing import Optional
from pydantic import BaseModel, Field

from src.utils.api_helpers import build_api_tools


tools = build_api_tools()


class IdeasList(BaseModel):
    """List of research ideas."""

    ideas: list[str] = Field(description="A list of research ideas")
    # user_response: str = Field(description="Text response to share ideas with user")
    goto: Optional[str] = Field(
        description="The next agent to call ('research', 'feedback'), or __end__ if the user's query has been resolved. Must be one of the specified values."
    )


def gen_idea_generator_agent(args, tools):
    llm = ChatOllama(model=args.model)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a research idea generator that suggests "
                "five new research directions based on the discussion with the "
                "user."
                "You should also take into account the ideas so far which are: "
                "{ideas}"
                "You should return only a list of ideas, numbered."
                "You should make use of your tools to pull the latest research "
                "rather than making up ideas directly. Don't return code to "
                "the user, use the tools directly."
                "Only do this if you actually received feedback and adjusted.",
            ),
            ("human", "{input}"),
        ]
    )

    def make_system_prompt():
        return (
            "You are a research idea generator that suggests "
            "five new research directions based on the discussion with the "
            "user. You should return only the list of ideas, numbered."
            "You should make use of your tools to pull the latest research "
            "rather than making up ideas directly. Don't return code to "
            "the user, use the tools directly."
            "If the user has suggested an idea to refine or delve deeper on "
            "focus on that idea and how you could provide more detail."
        )

    tools = build_api_tools()

    # llm = llm.with_structured_output(IdeasList)

    agent = create_react_agent(llm, tools=tools)  # , state_modifier=make_system_prompt())

    def chatbot(state):
        # print("\n\nGENERATOR INPUT")
        # print(state)
        try:
            state = agent.invoke(state)
            # print("\n\nGENERATER STATE", state)
            # update = state
            update = {
                "messages": [
                    HumanMessage(content=state["messages"][-1].content, name="generator_agent")
                ],
            }
        except Exception as e:
            ideas = []
            update = {"messages": state["messages"] + [f"Error: {e}"], "ideas": ideas}
            print("\n\nERROR", e)

        return Command(
            update=update,
            # goto=get_next_node(update["messages"][-1], "evaluate_agent"),
            goto="control_agent",  # "chat_agent",
        )

    return chatbot
