from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import requests
import logging
import socket
import json
import sys
from logging.handlers import SocketHandler

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "service": "payment-service",
            "level": record.levelname,
            "message": record.getMessage()
        })

logstash_handler = SocketHandler("logstash", 5000)
logstash_handler.setFormatter(JSONLogFormatter())
logger.addHandler(logstash_handler)

app = Flask(__name__)
CORS(app)

@app.route('/pay', methods=['POST'])
def process_payment():
    data = request.json
    user_id = data.get("user_id")
    order_id = data.get("order_id")
    amount = data.get("amount")

    # Simulate success/failure (90% success rate)
    if random.random() < 0.9:
        return jsonify({
            "status": "success",
            "message": f"Payment of ${amount} for order {order_id} by user {user_id} successful"
        }), 200
    else:
        return jsonify({
            "status": "failure",
            "message": "Payment failed due to bank error"
        }), 500

@app.route('/pay', methods=['POST'])
def process_payment():
    data = request.json
    user_id = data.get("user_id")
    order_id = data.get("order_id")
    amount = data.get("amount")

    if random.random() < 0.9:
        message = f"Payment of ${amount} for order {order_id} successful"

        # Notify user
        try:
            requests.post("http://notification-service:5005/notify", json={
                "type": "email",
                "to": f"{user_id}@example.com",  # Simulated
                "message": message
            })
        except Exception as e:
            print(f"[payment-service] Failed to notify: {e}")

        return jsonify({"status": "success", "message": message}), 200
    else:
        return jsonify({
            "status": "failure",
            "message": "Payment failed due to bank error"
        }), 500


@app.route('/health')
def health():
    return {"status": "payment-service is healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
