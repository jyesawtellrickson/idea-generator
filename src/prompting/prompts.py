from langchain_core.prompts import PromptTemplate

# prompt = hub.pull("hwchase17/react")

controller_prompt_template = PromptTemplate.from_template(
    """
    You're an idea generation agent.
    You're tasked with generating ideas for research.

    Conversation so far: 
    {chat_history}

    Your scratchpad:
    {agent_scratchpad}

    You have access to the following tools:

    {tools}

    Action: the action to take, should be one of [{tool_names}]

    IMPORTANT: You must always return valid JSON fenced by a markdown code block. Do not return any additional text.
    """)

system_prompt = "You're an idea generation agent."