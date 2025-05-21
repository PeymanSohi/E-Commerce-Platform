from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import time
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
            "service": "order-service",
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

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    products = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default='Pending')

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

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.json
    user_id = data['user_id']
    product_list = data['products']
    amount = sum(p['price'] * p['quantity'] for p in product_list)

    order = Order(user_id=user_id, products=str(product_list))
    db.session.add(order)
    db.session.commit()

    try:
        response = requests.post("http://payment-service:5004/pay", json={
            "user_id": user_id,
            "order_id": order.id,
            "amount": amount
        })
        print(f"[order-service] Payment response: {response.text}")
    except Exception as e:
        print(f"[order-service] Payment call error: {e}")

    return jsonify({'message': 'Order placed', 'order_id': order.id}), 201

@app.route('/orders/<string:user_id>', methods=['GET'])
def get_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': o.id,
        'products': o.products,
        'status': o.status
    } for o in orders])

@app.route('/health')
def health():
    return {"status": "order-service is healthy"}, 200

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5003)
