# order-service/app.py
from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

orders = {}  # In-memory: {username: [order1, order2, ...]}

@app.route('/order/<username>', methods=['POST'])
def place_order(username):
    data = request.json
    if not data.get('items'):
        return jsonify({'msg': 'No items provided'}), 400

    order_id = str(uuid.uuid4())
    order = {
        'order_id': order_id,
        'timestamp': datetime.utcnow().isoformat(),
        'items': data['items'],  # List of {product_id, quantity}
        'total': data.get('total', 0),
        'status': 'placed'
    }

    orders.setdefault(username, []).append(order)
    return jsonify({'msg': 'Order placed', 'order': order}), 201

@app.route('/order/<username>', methods=['GET'])
def get_orders(username):
    return jsonify(orders.get(username, []))

@app.route('/order/<username>/<order_id>', methods=['GET'])
def get_order(username, order_id):
    user_orders = orders.get(username, [])
    for order in user_orders:
        if order['order_id'] == order_id:
            return jsonify(order)
    return jsonify({'msg': 'Order not found'}), 404

@app.route('/order/<username>/<order_id>/status', methods=['PATCH'])
def update_order_status(username, order_id):
    data = request.json
    new_status = data.get('status')
    if not new_status:
        return jsonify({'msg': 'Missing status'}), 400

    for order in orders.get(username, []):
        if order['order_id'] == order_id:
            order['status'] = new_status
            return jsonify({'msg': 'Status updated', 'order': order})
    return jsonify({'msg': 'Order not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
