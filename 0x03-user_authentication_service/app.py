#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, jsonify, request
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
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
