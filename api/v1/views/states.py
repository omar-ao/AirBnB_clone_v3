#!/usr/bin/python3

"""This is `states` module that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


def get_all_states():
    """Gets all states objects"""
    objects = storage.all()
    states = [v for k, v in objects.items() if v.__class__ == State]
    return states


def find_state(states, state_id):
    """Finds state by id in states objects"""
    state = [state for state in states if state.id == state_id]
    if state == []:
        return None
    return state[0]


@app_views.route('/states/', methods=['GET'])
def get_states():
    states = get_all_states()
    states = [state.to_dict() for state in states]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    states = get_all_states()
    state = find_state(states, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    states = get_all_states()
    state = find_state(states, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' not in data.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)

    state = State()
    state.name = data['name']
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    states = get_all_states()
    state = find_state(states, state_id)
    if state is None:
        abort(404)
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
