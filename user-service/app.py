# user-service/app.py
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

users = {}  # In-memory user store for demo

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('username') or not data.get('password'):
        return jsonify({'msg': 'Missing fields'}), 400

    if data['username'] in users:
        return jsonify({'msg': 'User already exists'}), 400

    users[data['username']] = data['password']
    return jsonify({'msg': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if users.get(data['username']) == data.get('password'):
        token = create_access_token(identity=data['username'])
        return jsonify({'access_token': token}), 200
    return jsonify({'msg': 'Invalid credentials'}), 401

@app.route('/profile', methods=['GET'])
def profile():
    return jsonify({'msg': 'You need JWT auth here.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
