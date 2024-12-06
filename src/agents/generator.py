from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate

def gen_idea_generator_agent(args, tools):
    llm = ChatOllama(model=args.model)
    llm_with_tools = llm.bind_tools(tools)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", "You are a research idea generator that suggests "
                "five new research directions based on the discussion with the "
                "user. You should return only the list of ideas, numbered."
                "You should make use of your tools to pull the latest research "
                "rather than making up ideas directly. Don't return code to "
                "the user, use the tools directly."
            ),
            ("human", "{input}")
        ]
    )
    chain = prompt | llm_with_tools


    def chatbot(state):
        response = chain.invoke({
            "input": state["messages"][-1].content,
        })
        ideas = response.content.split("\n")
        return {"messages": state["messages"] + [response], "ideas": ideas}

    return chatbot