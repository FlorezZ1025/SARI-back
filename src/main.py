from flask import jsonify, redirect, request, url_for
from app import app, jwt

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(debug=True)