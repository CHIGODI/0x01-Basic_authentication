#!/usr/bin/env python3
"""Flask App"""

from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """return simple json"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """register a user."""
    email = request.form.get('email')
    password = request.form.get('password')

    if password and email:
        try:
            AUTH.register_user(email,
                               password)
        except Exception:
            return jsonify({"message": "email already registered"}), 400

        return jsonify({"email": email,
                        "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """user login"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        if not AUTH.valid_login(email, password):
            Flask.abort(401)
        AUTH.create_session(email)
        return {"email": email, "message": "logged in"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
