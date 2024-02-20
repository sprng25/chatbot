from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-response/', methods=['GET'])
def get_response():
    user_message = request.args.get('message', '')

    # Send user message to Rasa server
    rasa_response = send_to_rasa_server(user_message)

    return jsonify({'response': rasa_response})

def send_to_rasa_server(message):
    rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"
    
    data = {
        "sender": "user",
        "message": message,
    }

    response = requests.post(rasa_server_url, json=data)
    rasa_response = response.json()[0]['text'] if response.json() else 'I am sorry, but I do not understand.'

    return rasa_response

if __name__ == '__main__':
    app.run(debug=True)