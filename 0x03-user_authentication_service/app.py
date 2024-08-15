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
    if session_id is None:
        abort(403)

    try:
        user = AUTH.get_user_from_session_id(session_id=session_id)
        AUTH.destroy_session(user.id)

        return redirect(url_for('index'))
    except Exception:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """find profile for a user"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)

    try:
        user = AUTH.get_user_from_session_id(session_id=session_id)
        return jsonify({"email": user.email})
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST', 'PUT'], strict_slashes=False)
def reset_password():
    """reset password"""
    email = request.form.get('email')
    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email=email)
        return jsonify({"email": email, "reset_token": reset_token})
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """update password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not reset_token:
        abort(403)

    try:
        reset_token = AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
