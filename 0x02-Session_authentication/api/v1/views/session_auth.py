#!/usr/bin/env python3
"""Session user endpoint"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User
import os

@app_views.route('/auth_session/login', methods='POST',
                 strict_slashed=False)
def handle_all_routes():
    """return current_user json"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})[0]
    if user:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_cookie = auth.create_session(user.id)
            response = make_response(user.to_json())
            response.set_cookie(os.getenv('SESSION_NAME'), session_cookie)
            return response
        return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404
