# notification-service/app.py
from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

notifications = []  # In-memory store of notifications

@app.route('/notify/email', methods=['POST'])
def send_email():
    data = request.json
    required = ['to', 'subject', 'message']
    if not all(k in data for k in required):
        return jsonify({'msg': 'Missing fields'}), 400

    notification = {
        'id': str(uuid.uuid4()),
        'type': 'email',
        'to': data['to'],
        'subject': data['subject'],
        'message': data['message'],
        'timestamp': datetime.utcnow().isoformat()
    }
    notifications.append(notification)
    print(f"[EMAIL SENT] → {notification['to']} | {notification['subject']}")
    return jsonify({'msg': 'Email sent', 'notification': notification}), 200

@app.route('/notify/sms', methods=['POST'])
def send_sms():
    data = request.json
    required = ['to', 'message']
    if not all(k in data for k in required):
        return jsonify({'msg': 'Missing fields'}), 400

    notification = {
        'id': str(uuid.uuid4()),
        'type': 'sms',
        'to': data['to'],
        'message': data['message'],
        'timestamp': datetime.utcnow().isoformat()
    }
    notifications.append(notification)
    print(f"[SMS SENT] → {notification['to']} | {notification['message']}")
    return jsonify({'msg': 'SMS sent', 'notification': notification}), 200

@app.route('/notifications', methods=['GET'])
def get_notifications():
    return jsonify(notifications)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
