from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
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
            "service": "user-service",
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
app.config['JWT_SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

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

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return {"message": "User registered"}, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        token = create_access_token(identity=user.username)
        return {"access_token": token}
    return {"msg": "Invalid credentials"}, 401

@app.route('/health')
def health():
    return {"status": "user-service is healthy"}, 200

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=8000)
