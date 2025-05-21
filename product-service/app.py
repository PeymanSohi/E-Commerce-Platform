from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'category': p.category,
        'price': p.price,
        'stock': p.stock
    } for p in products])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    product = Product(
        name=data['name'],
        category=data.get('category', ''),
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product added'}), 201

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
