#!/usr/bin/env python3
"""Flask App"""

from flask import Flask, jsonify, request, abort
from flask import make_response, url_for, redirect
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
    """User login"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    print(AUTH.valid_login(email, password))
    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response = make_response(jsonify({"email": email, "message": "logged in"}))

    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout endpoint"""
    session_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        response = redirect(url_for('index'))
        response.set_cookie('session_id', '', expires=0)
        return response
    except Exception:
        abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
