import re
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, START


def extract_numbered_lines(text, max=5):
    """
    Extract lines that start with numbers from the given text.
    """
    numbered_lines = re.findall(r"^\d+\.\s*(.*)$", text, re.MULTILINE)[:5]
    return numbered_lines


def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return "control_agent"
    return goto


def format_ideas(ideas):
    return "\n".join([f"{i+1}. {idea}" for i, idea in enumerate(ideas)])
