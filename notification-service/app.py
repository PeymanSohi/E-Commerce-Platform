from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    notification_type = data.get("type")  # e.g., 'email' or 'sms'
    recipient = data.get("to")
    message = data.get("message")

    print(f"[{notification_type.upper()}] To: {recipient} | Message: {message}")

    return jsonify({"status": "sent", "to": recipient}), 200

@app.route('/health')
def health():
    return {"status": "notification-service is healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
