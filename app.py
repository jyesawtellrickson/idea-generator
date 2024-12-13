# Import required libraries
from flask import Flask, request, jsonify, render_template
from src.pipelines.basic import print_stream, build_graph
import argparse

# Initialize Flask app
app = Flask(__name__)

parser = argparse.ArgumentParser(description="Generate Research Ideas")
parser.add_argument("--model", type=str, default="mistral", choices=["mistral", "qwen2.5:14b"])
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
    message = print_stream(graph, inputs, {"configurable": {"thread_id": "thread-1"}})
    # Replace this with your idea generator logic
    return message.content


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
    response = chatbot_response(user_message)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
