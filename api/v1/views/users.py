#!/usr/bin/python3

"""This is `amenities` module that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET'])
def get_users():
    users = [v.to_dict() for k, v in storage.all(User).items()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    users = storage.all(User)
    key = '{}.{}'.format('User', user_id)
    if key not in users.keys():
        abort(404)
    return jsonify(users[key].to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = storage.all(User)
    key = '{}.{}'.format('User', user_id)
    if key not in users.keys():
        abort(404)
    storage.delete(users[key])
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' not in data.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)

    user_obj = User()
    user_obj.name = data['name']
    storage.new(user_obj)
    storage.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    users = storage.all(User)
    key = '{}.{}'.format('User', user_id)
    if key not in users.keys():
        abort(404)
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    user_obj = users[key]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
