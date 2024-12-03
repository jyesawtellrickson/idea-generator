from flask import Flask, request, jsonify
from data_querying import query_data
from summariser import generate_summary

app = Flask(__name__)

@app.route('/idea_generator', methods=['POST'])
def idea_generator():
    # Step 1: Get user input
    user_input = request.json.get('keywords', '')
    if not user_input:
        return jsonify({'error': 'No keywords provided'}), 400
    
    # Step 2: Query data
    queried_data = query_data(user_input)
    if not queried_data:
        return jsonify({'error': 'No data found for the given keywords'}), 404
    
    # Step 3: Generate summary
    summary = generate_summary(queried_data)
    return jsonify({'keywords': user_input, 'ideas': summary})

if __name__ == '__main__':
    app.run(debug=True)