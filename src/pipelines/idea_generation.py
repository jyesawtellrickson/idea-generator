from typing import Annotated
from datetime import datetime
from typing_extensions import TypedDict
from typing import Literal
import json

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph import END, START
from langchain_core.tools import tool
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from langchain_core.messages import ToolMessage
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

from src.utils.api_helpers import query_arxiv
from src.agents.generator import gen_idea_generator_agent
from src.agents.evaluator import gen_evaluate_idea_agent

def build_langgraph(args):
    """
    Build the langgraph pipeline.
    """
    class State(TypedDict):
        messages: Annotated[list, add_messages]
        ideas: list[str]

    graph_builder = StateGraph(State)
    memory = MemorySaver()

    @tool
    def get_now(format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Get the current time, use python string formatting to change the format.
        """
        return datetime.now().strftime(format)

    @tool
    def get_arxiv_papers(keyword: str, num_results: int) -> list[dict]:
        """
        Fetches research papers from ArXiv.
        """
        return query_arxiv(keyword, num_results)

    tools = [get_now, get_arxiv_papers]
    tool_node = ToolNode(tools=tools)

    generator_agent = gen_idea_generator_agent(args, tools)
    evaluate_agent = gen_evaluate_idea_agent(args, tools)

    # Add all the parts to the graph
    graph_builder.add_node("generator_agent", generator_agent)
    graph_builder.add_node("evaluate_agent", evaluate_agent)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_edge("generator_agent", "evaluate_agent")
    graph_builder.add_edge("tools", "generator_agent")
    graph_builder.add_edge(START, "generator_agent")

    # The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
    # it is fine directly responding. This conditional routing defines the main agent loop.
    graph_builder.add_conditional_edges(
        "generator_agent",
        tools_condition,
    )
    # Compile the graph and save image
    graph = graph_builder.compile(checkpointer=memory)
    image = graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)

    with open("graph_image.png", "wb") as f:
        f.write(image)

    return graph


def run_langgraph(args, graph):
    """
    Run the langgraph pipeline.
    """
    def stream_graph_updates(user_input: str):
        config = {"configurable": {"thread_id": "1"}}
        for event in graph.stream({"messages": [("user", user_input)]}, config):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)
                if value.get("ideas"):
                    print("Ideas:", value["ideas"])


    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)



class InteractiveIdeaGenerationPipeline:
    def __init__(self, config):
        self.config = config
        self.graph = LangGraph()

        # Define agents
        self.idea_generation_agent = IdeaGenerationAgent()
        self.summarization_agent = SummarizationAgent()

        # Build graph
        self._build_graph()

    def _build_graph(self):
        """
        Builds the LangGraph workflow for idea generation with user interaction.
        """
        # Node: Fetch related papers
        self.graph.add_node(
            "fetch_papers",
            lambda user_prompt: fetch_related_papers(user_prompt, self.config['paper_api']),
        )

        # Node: Summarize research papers
        self.graph.add_node(
            "summarize",
            self.summarization_agent.summarize_papers,
            depends_on=["fetch_papers"],
        )

        # Node: Generate initial ideas
        self.graph.add_node(
            "generate_ideas",
            lambda args: self.idea_generation_agent.generate_ideas(*args),
            depends_on=["summarize", "fetch_papers"],
        )

        # Node: Refine ideas (placeholder for iterative feedback loop)
        self.graph.add_node(
            "refine_ideas",
            lambda args: self.idea_generation_agent.refine_ideas(*args),
            depends_on=["generate_ideas"],
            dynamic=True,  # Allows re-execution for feedback refinement
        )

    def run(self, user_prompt):
        """
        Executes the pipeline with a user-interactive loop for idea refinement.

        Args:
            user_prompt (str): The initial input describing the research area.

        Returns:
            dict: Final refined ideas and summaries.
        """
        # Step 1: Run initial pipeline
        start = input("\What research area would you like to focus on?")
        self.graph.set_input("user_prompt", start)
        results = self.graph.run()

        # Step 2: User interaction for refinement
        generated_ideas = results["generate_ideas"]
        print("\n💡 Initial Ideas:")
        for i, idea in enumerate(generated_ideas, 1):
            print(f"{i}. {idea}")

        while True:
            feedback = input("\nProvide feedback or refinement instructions (or type 'done' to finish): ")
            if feedback.lower() == "done":
                break

            # Pass feedback into the refinement node
            refined_ideas = self.graph.run_node("refine_ideas", args=(generated_ideas, feedback))
            print("\n🔄 Refined Ideas:")
            for i, idea in enumerate(refined_ideas, 1):
                print(f"{i}. {idea}")
            generated_ideas = refined_ideas  # Update ideas for next refinement cycle

        results = {
            "final_ideas": generated_ideas,
            "summaries": results["summarize"],
        }

        with open("logs/final_ideas.json", "w") as f:
            import json
            json.dump(generated_ideas, f, indent=4)
        print("\nResults saved to final_ideas.json")

        return results

