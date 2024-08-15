#!/usr/bin/env python3
"""Testing main, module"""

import requests


url = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """testing register user"""
    res = requests.post(f'{url}/users', data={'email': email,
                                              'password': password})
    assert res.status_code == 200, 'Failed to register user'
    assert res.json() == {'email': email, 'message': 'user created'},
    'Incorrect registration response'


def log_in_wrong_password(email: str, password: str) -> None:
    """test login wrong password"""
    res = requests.post(f'{url}/sessions', data={'email': email,
                                                 'password': password})
    assert res.status_code == 401, 'Wrong password should not allow login'


def log_in(email: str, password: str) -> str:
    """test login endpoint"""
    res = requests.post(f'{url}/sessions', data={'email': email,
                                                 'password': password})
    assert res.status_code == 200, 'Failed to log in'
    assert res.json() == {'email': email, 'message': 'logged in'},
    'Incorrect login response'
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """test profile unlogged"""
    res = requests.get(f'{url}/profile')
    assert res.status_code == 403
    'Unauthenticated profile access should be forbidden'


def profile_logged(session_id: str) -> None:
    """test profile logged"""
    res = requests.get(f'{url}/profile',
                       cookies={'session_id': session_id})
    assert res.status_code == 200, 'Profile access failed for logged-in user'
    assert res.json() == {'email': 'guillaume@holberton.io'}


def log_out(session_id: str) -> None:
    """test logout"""
    res = requests.delete(f'{url}/sessions',
                          cookies={'session_id': session_id})
    assert res.status_code == 200, 'Logout failed'


def reset_password_token(email: str) -> str:
    """test reset password token generation"""
    res = requests.put(f'{url}/reset_password', data={'email': email})
    assert res.status_code == 200, 'Failed to generate reset password token'
    assert 'reset_token' in res.json(), 'Reset token not found in response'
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test update password"""
    res = requests.put(f'{url}/reset_password',
                       data={'email': email,
                             'reset_token': reset_token,
                             'new_password': new_password})
    assert res.status_code == 200, 'Failed to update password'
    assert res.json() == {"email": email,
                          "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()

    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)

    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
