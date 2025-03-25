from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Define the API key and endpoint
API_KEY = 'YOUR_GEMINI_API'
API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}'

@app.route('/')
def index():
    return render_template('home.html')  # Renders the front-end HTML

@app.route('/index')
def indexx():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    # Get user input from the request JSON
    data = request.get_json()  # Get the data sent as JSON
    query = data.get('message')

    # Validate input
    if not query:
        return jsonify({"response": "Please enter a query."})

    # Prepare the request body for Gemini API
    request_body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": query
                    }
                ]
            }
        ]
    }

    # Send request to Gemini API
    try:
        response = requests.post(API_URL, json=request_body)
        response_data = response.json()

        # Extract the response content
        report_data = response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No data received.')
        return jsonify({"response": report_data})
    
    except Exception as e:
        return jsonify({"response": "Failed to fetch response. Please try again later."})

if __name__ == '__main__':
    app.run(debug=True)
