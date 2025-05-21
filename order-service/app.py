from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    products = db.Column(db.String(500), nullable=False)  # e.g., JSON string
    status = db.Column(db.String(20), default='Pending')

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.json
    order = Order(user_id=data['user_id'], products=str(data['products']))
    db.session.add(order)
    db.session.commit()
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
