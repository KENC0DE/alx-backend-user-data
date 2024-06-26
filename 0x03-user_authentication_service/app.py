#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, jsonify, request, redirect
from flask import abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def root_msg() -> str:
    """Return root message"""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Register Users"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    try:
        AUTH.register_user(email, pwd)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Login or Not"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    if AUTH.valid_login(email, pwd):
        s_id = AUTH.create_session(email)
        msg = {'email': email, 'message': 'logged in'}
        resp = jsonify(msg)
        resp.set_cookie('session_id', s_id)
        return resp

    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Logout user"""
    s_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(s_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')

    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """User Profile"""
    s_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=s_id)
    if user:
        return jsonify({'email': user.email}), 200

    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password() -> str:
    """reset user password"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email,
                        'reset_token': token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Reset User password"""
    form = request.form
    try:
        AUTH.update_password(form['reset_token'], form['new_password'])
        return jsonify({'email': form['email'],
                        'message': 'Password updated'}), 200
    except (ValueError, KeyError):
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
