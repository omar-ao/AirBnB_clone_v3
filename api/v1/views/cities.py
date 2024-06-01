#!/usr/bin/python3

"""This is `cities` module that handles all
default RESTFul API actions for cities"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
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


def find_city(city_id):
    cities = storage.all(City)
    key = '{}.{}'.format('City', city_id)
    return cities.get(key)


@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def get_cities(state_id):
    states = get_all_states()
    state = find_state(states, state_id)
    if state is None:
        abort(404)
    objs = storage.all(City).items()
    cities = [v.to_dict() for k, v in objs if v.state_id == state_id]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = find_city(city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = find_city(city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    states = get_all_states()
    state = find_state(states, state_id)
    if state is None:
        abort(404)
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' not in data.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)

    city = City()
    city.name = data['name']
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = find_city(city_id)
    if city is None:
        abort(404)
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
