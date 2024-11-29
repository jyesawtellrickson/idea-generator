# src/pipelines/interactive_idea_generation_pipeline.py

from langgraph import LangGraph, Node
from agents.generator import IdeaGenerationAgent
from agents.summariser import SummarizationAgent
from utils.api_helpers import fetch_related_papers


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
        self.graph.set_input("user_prompt", user_prompt)
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

        return {
            "final_ideas": generated_ideas,
            "summaries": results["summarize"],
        }


if __name__ == "__main__":
    # Example configuration
    config = {
        "paper_api": {
            "endpoint": "https://api.semanticscholar.org/v1/papers",
            "api_key": "YOUR_API_KEY_HERE"
        },
        "llm": {
            "model": "gpt-4",
            "temperature": 0.7
        }
    }

    # Example input
    user_prompt = "Explore novel ways to enhance transformer efficiency in NLP."

    pipeline = InteractiveIdeaGenerationPipeline(config)
    result = pipeline.run(user_prompt)

    # Save results to file
    with open("final_ideas.json", "w") as f:
        import json
        json.dump(result, f, indent=4)
    print("\nResults saved to final_ideas.json")
