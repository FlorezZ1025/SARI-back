from flask import jsonify, redirect, request, url_for
from app import app, jwt

@app.after_request
def add_cors_headers(response):
    # 
    # response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-credentials', True)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    # response.headers.add('Access-Control-Allow-Credentials', 'true')  # Para cookies
    return response

# @app.route('/')
# def index():
#     return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(debug=True)