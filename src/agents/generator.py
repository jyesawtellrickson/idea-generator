from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent

from langgraph.types import Command
from langchain_core.messages import HumanMessage, AIMessage


def gen_idea_generator_agent(args, tools):
    llm = ChatOllama(model=args.model)

    prompt_template = ChatPromptTemplate.from_messages(
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
            ("placeholder", "{conversation}"),
        ]
    )

    agent = create_react_agent(llm, tools=tools)  # , state_modifier=make_system_prompt())

    def chatbot(state):
        """
        Chatbot for generating ideas.
        It will use various APIs to get the latest research.
        Will return a numbered list of ideas.
        """
        # print("\n\nGENERATOR INPUT")
        # print(state)
        try:
            prompt = prompt_template.invoke(
                {"conversation": state["messages"][-5:], "ideas": state.get("ideas", [])}
            )
            state = agent.invoke(prompt)
            # print("\n\nGENERATER STATE", state)
            # update = state
            update = {
                "messages": [
                    AIMessage(content=state["messages"][-1].content, name="generator_agent")
                ],
            }
        except Exception as e:
            ideas = []
            update = {"messages": state["messages"] + [f"Error: {e}"], "ideas": ideas}
            print("\n\nERROR", e)

        return Command(
            update=update,
            goto="control_agent",  # "chat_agent",
        )

    return chatbot
