# cart-service/app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory carts: {username: [{product_id, quantity}]}
carts = {}

@app.route('/cart/<username>', methods=['GET'])
def get_cart(username):
    return jsonify(carts.get(username, []))

@app.route('/cart/<username>/add', methods=['POST'])
def add_to_cart(username):
    data = request.json
    if not data.get('product_id') or not data.get('quantity'):
        return jsonify({'msg': 'Missing fields'}), 400

    user_cart = carts.setdefault(username, [])
    for item in user_cart:
        if item['product_id'] == data['product_id']:
            item['quantity'] += data['quantity']
            return jsonify({'msg': 'Quantity updated'}), 200

    user_cart.append({
        'product_id': data['product_id'],
        'quantity': data['quantity']
    })
    return jsonify({'msg': 'Product added to cart'}), 201

@app.route('/cart/<username>/remove', methods=['POST'])
def remove_from_cart(username):
    data = request.json
    user_cart = carts.get(username, [])
    carts[username] = [item for item in user_cart if item['product_id'] != data.get('product_id')]
    return jsonify({'msg': 'Product removed'}), 200

@app.route('/cart/<username>/update', methods=['POST'])
def update_cart(username):
    data = request.json
    user_cart = carts.get(username, [])
    for item in user_cart:
        if item['product_id'] == data['product_id']:
            item['quantity'] = data['quantity']
            return jsonify({'msg': 'Quantity updated'}), 200
    return jsonify({'msg': 'Product not found in cart'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
