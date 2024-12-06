import argparse
from src.pipelines.idea_generation import build_langgraph, run_langgraph

def main():
    parser = argparse.ArgumentParser(description='Generate Research Ideas')
    # which LLM
    parser.add_argument('--model', type=str, default="mistral")
    # which APIs to use
    # number of ideas
    # use feedback
    args = parser.parse_args()

    # Initialize the pipeline
    graph = build_langgraph(args)
    run_langgraph(args, graph)


if __name__ == "__main__":
    main()