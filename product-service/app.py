# product-service/app.py
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

products = {}  # In-memory product storage

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    if not data.get('name') or not data.get('price'):
        return jsonify({'msg': 'Missing name or price'}), 400

    product_id = str(uuid.uuid4())
    products[product_id] = {
        'id': product_id,
        'name': data['name'],
        'price': data['price'],
        'description': data.get('description', ''),
        'inventory': data.get('inventory', 0)
    }
    return jsonify(products[product_id]), 201

@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(list(products.values()))

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product)
    return jsonify({'msg': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
