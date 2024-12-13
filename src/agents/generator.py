from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate

from src.utils.utils import extract_numbered_lines
from langgraph.types import Command

from src.utils.utils import get_next_node, format_ideas
from langgraph.prebuilt import create_react_agent


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

    agent = create_react_agent(llm, tools=tools, state_modifier=make_system_prompt())

    def chatbot(state):
        print("\n\nGENERATOR INPUT")
        print(state)
        try:
            state = agent.invoke(state)
            print("\n\nGENERATER STATE", state)
            ideas = extract_numbered_lines(state["messages"][-1].content)[:5]
        except Exception as e:
            ideas = []
            update = {"messages": state["messages"] + [f"Error: {e}"], "ideas": ideas}
            print("\n\nERROR", e)

        # update = {"messages": state["messages"] + [response], "ideas": ideas}
        update = {"messages": state["messages"], "ideas": ideas}
        print(update)

        return Command(
            update=update,
            # goto=get_next_node(update["messages"][-1], "evaluate_agent"),
            goto="chat_agent",
        )

    return chatbot
