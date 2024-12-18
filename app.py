# Import required libraries
from flask import Flask, request, jsonify, render_template, session
from src.pipelines.basic import print_stream, build_graph
from src.pipelines import idea_generation

import argparse
import uuid

# from flask_ngrok import run_with_ngrok

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "jye"
# run_with_ngrok(app)

parser = argparse.ArgumentParser(description="Generate Research Ideas")
parser.add_argument("--model", type=str, default="mistral", choices=["mistral", "qwen2.5:14b"])
parser.add_argument("--pipeline", type=str, default="basic", choices=["basic", "idea_generation"])
args = parser.parse_args()

if args.pipeline == "basic":
    graph = build_graph(args)
elif args.pipeline == "idea_generation":
    graph = idea_generation.build_langgraph(args)

init = True
init_message = (
    "\n\n---------------------------------------\n"
    "Welcome to the research idea generator!"
    " Please tell me about the area of research you're interested in to"
    " get started."
    "\n\nYou can quit by typing 'quit' or 'exit'."
)


# Define the chatbot logic
def chatbot_response(user_input):
    if "thread_id" not in session:
        session["thread_id"] = str(uuid.uuid4())

    thread_id = session["thread_id"]
    init = False
    papers = ""
    tool_results = []
    if init:
        inputs = {"messages": [("ai", init_message), ("user", user_input)]}
        init = False
    else:
        inputs = {"messages": [("user", user_input)]}

    if args.pipeline == "basic":
        message, tool_results = print_stream(
            graph, inputs, {"configurable": {"thread_id": thread_id}}
        )
        ideas = []
    elif args.pipeline == "idea_generation":
        state, tool_results = idea_generation.stream_graph_updates(
            graph, inputs, {"configurable": {"thread_id": thread_id}}
        )
        message = state["messages"][-1]
        ideas = state["ideas"][:5]
    # Replace this with your idea generator logic
    # Display papers queried to the user, from tool results
    if len(tool_results) > 0:
        for tool, content in tool_results:
            if tool == "arxiv_tool":
                papers = content

    return message.content, papers


# Define route for the main interface
@app.route("/")
def index():
    return render_template("index.html")


# Define route for chatbot interaction
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    response, papers = chatbot_response(user_message)
    data = {"response": response}
    if len(papers) > 0:
        data["papers"] = papers

    return jsonify(data)  # , "ideas": ideas})


if __name__ == "__main__":
    app.run()
