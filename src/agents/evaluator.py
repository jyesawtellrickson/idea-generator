from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_ollama import ChatOllama



def gen_evaluate_idea_agent(args, tools):
                            
    llm = ChatOllama(model=args.model)
    llm_with_tools = llm.bind_tools(tools)

    prompt = PromptTemplate.from_template(
        # "The user is interested in: {user_prompt}\n"
        "You are a research supervisor talking with your student. "
        "The proposed ideas are:\n"
        "{ideas}\n"
        "Provide critical feedback on the ideas, focusing on feasibility."
    )
    chain = prompt | llm_with_tools

    def gen_idea(state):
        ideas = state["ideas"]
        messages = state["messages"]
        last_message = messages[-1].content
        response = chain.invoke({"ideas": ideas})
        return {"messages": messages + [response], "ideas": ideas}
    
    return gen_idea