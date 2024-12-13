import argparse
from src.pipelines.idea_generation import build_langgraph, run_langgraph
from src.pipelines.basic import run_basic


def main():
    parser = argparse.ArgumentParser(description="Generate Research Ideas")
    # which LLM
    parser.add_argument("--model", type=str, default="mistral", choices=["mistral", "qwen2.5:14b"])
    parser.add_argument(
        "--pipeline", type=str, default="basic", choices=["basic", "idea_generation"]
    )
    # which APIs to use
    # number of ideas
    # use feedback
    args = parser.parse_args()
    print(args)
    # Initialize the pipeline
    if args.pipeline == "basic":
        run_basic(args)
    elif args.pipeline == "idea_generation":
        graph = build_langgraph(args)
        run_langgraph(args, graph)


if __name__ == "__main__":
    main()
