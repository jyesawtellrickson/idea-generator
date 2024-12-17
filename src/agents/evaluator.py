from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_ollama import ChatOllama

from src.utils.utils import get_next_node
from langgraph.types import Command

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


def gen_evaluate_idea_agent(args, tools):

    llm = ChatOllama(model=args.model)
    llm_with_tools = llm.bind_tools(tools)

    prompt = PromptTemplate.from_template(
        # "The user is interested in: {user_prompt}\n"
        "You are a research supervisor talking with your student. "
        "The proposed ideas are:\n"
        "{ideas}\n"
        "Provide critical feedback on the ideas, focusing on feasibility and "
        "impact."
    )
    chain = prompt | llm_with_tools

    def gen_idea(state):
        ideas = state["ideas"]
        messages = state["messages"]
        last_message = messages[-1].content
        response = chain.invoke({"ideas": ideas})
        update = {
            "messages": messages
            + [AIMessage(content="FEEDBACK:\n\n" + response.content, name="evaluate_agent")],
            "ideas": ideas,
        }

        goto = get_next_node(update["messages"][-1], "generator_agent")

        return Command(update=update, goto=goto)

    return gen_idea


def score_idea_with_llm(idea: dict, model_name="gpt-4"):
    """
    Uses an LLM to score an idea based on defined criteria.
    """
    prompt = f"""
    Evaluate the following idea on a scale of 1-10 for:
    - Impact: Potential significance in advancing knowledge or solving problems.
    - Novelty: Degree of innovation or uniqueness.
    - Feasibility: Practicality of implementation.

    Idea:
    Title: {idea.get('title', 'No title')}
    Abstract: {idea.get('abstract', 'No abstract')}

    Provide scores and a brief justification for each criterion.
    """
    model = ChatOllama(model=model_name)
    response = model.chat(prompt)
    # Parse response to extract scores
    return response
