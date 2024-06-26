#!/usr/bin/python3

"""This is `users` module that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    users = [v.to_dict() for k, v in storage.all(User).items()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    users = storage.all(User)
    key = '{}.{}'.format('User', user_id)
    if key not in users.keys():
        abort(404)
    return jsonify(users[key].to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'email' not in data.keys():
        return make_response(jsonify({"error": "Missing email"}), 400)

    if 'password' not in data.keys():
        return make_response(jsonify({"error": "Missing password"}), 400)

    user_obj = User()
    user_obj.email = data['email']
    user_obj.password = data['password']
    storage.new(user_obj)
    storage.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    users = storage.all(User)
    key = '{}.{}'.format('User', user_id)
    if key not in users.keys():
        abort(404)
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    user_obj = users[key]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
