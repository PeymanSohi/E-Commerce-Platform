from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import time
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
            "service": "cart-service",
            "level": record.levelname,
            "message": record.getMessage()
        })

logstash_handler = SocketHandler("logstash", 5000)
logstash_handler.setFormatter(JSONLogFormatter())
logger.addHandler(logstash_handler)

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ecommerce_user:ecommerce_pass@mysql:3306/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

def create_tables():
    for _ in range(10):
        try:
            with app.app_context():
                db.create_all()
            print("✅ Tables created")
            break
        except Exception as e:
            print("⏳ Waiting for MySQL...", str(e))
            time.sleep(3)

@app.route('/cart/<string:user_id>', methods=['GET'])
def get_cart(user_id):
    items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': item.id,
        'product_id': item.product_id,
        'quantity': item.quantity
    } for item in items])

@app.route('/cart/<string:user_id>', methods=['POST'])
def add_to_cart(user_id):
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']
    existing_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item added to cart'}), 201

@app.route('/cart/<string:user_id>/<int:item_id>', methods=['DELETE'])
def remove_item(user_id, item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item removed'}), 200

@app.route('/health')
def health():
    return {"status": "cart-service is healthy"}, 200

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5002)
