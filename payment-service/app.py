# payment-service/app.py
from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

payments = {}  # In-memory store {payment_id: payment_info}

@app.route('/pay', methods=['POST'])
def process_payment():
    data = request.json
    required_fields = ['username', 'order_id', 'amount', 'payment_method']

    if not all(field in data for field in required_fields):
        return jsonify({'msg': 'Missing fields'}), 400

    payment_id = str(uuid.uuid4())
    payment = {
        'payment_id': payment_id,
        'username': data['username'],
        'order_id': data['order_id'],
        'amount': data['amount'],
        'payment_method': data['payment_method'],
        'status': 'success',
        'timestamp': datetime.utcnow().isoformat()
    }

    payments[payment_id] = payment
    return jsonify({'msg': 'Payment processed', 'payment': payment}), 200

@app.route('/payment/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = payments.get(payment_id)
    if payment:
        return jsonify(payment)
    return jsonify({'msg': 'Payment not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
