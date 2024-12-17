# Import required libraries
from flask import Flask, request, jsonify, render_template
from src.pipelines.basic import print_stream, build_graph
import argparse
# from flask_ngrok import run_with_ngrok

# Initialize Flask app
app = Flask(__name__)
# run_with_ngrok(app)

parser = argparse.ArgumentParser(description="Generate Research Ideas")
parser.add_argument("--model", type=str, default="mistral", choices=["mistral", "qwen2.5:14b"])
parser.add_argument("--pipeline", type=str, default="basic", choices=["basic", "idea_generation"])
args = parser.parse_args()
graph = build_graph(args)
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
    init = True
    if init:
        inputs = {"messages": [("ai", init_message), ("user", user_input)]}
        init = False
    else:
        inputs = {"messages": [("user", user_input)]}

    if args.pipeline == "basic":
        message = print_stream(graph, inputs, {"configurable": {"thread_id": "thread-1"}})
        ideas = []
    elif args.pipeline == "idea_generation":
        state = print_stream(graph, inputs, {"configurable": {"thread_id": "1"}})
        message = state["messages"][-1]
        ideas = state["ideas"][:5]
    # Replace this with your idea generator logic
    return message.content, ideas


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
    response, ideas = chatbot_response(user_message)
    return jsonify({"response": response})  # , "ideas": ideas})


if __name__ == "__main__":
    app.run()
