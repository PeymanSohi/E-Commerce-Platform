from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

users = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    users[data['username']] = data['password']
    return {"message": "User registered"}, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if users.get(data['username']) == data['password']:
        token = create_access_token(identity=data['username'])
        return {"access_token": token}
    return {"msg": "Invalid credentials"}, 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
