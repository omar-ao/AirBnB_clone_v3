#!/usr/bin/python3

"""This is `places` module that handles all
default RESTFul API actions for cities"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place


def get_all_cities():
    """Gets all states objects"""
    objects = storage.all()
    states = [v for k, v in objects.items() if v.__class__ == City]
    return states


def find_city(cities, city_id):
    """Finds state by id in states objects"""
    city = [city for city in cities if city.id == city_id]
    if city == []:
        return None
    return city[0]


def find_place(place_id):
    places = storage.all(Place)
    key = '{}.{}'.format('Place', place_id)
    return places.get(key)


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    cities = get_all_cities()
    city = find_city(cities, city_id)
    if city is None:
        abort(404)
    objs = storage.all(Place).items()
    places = [v.to_dict() for k, v in objs if v.city_id == city_id]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = find_place(place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = find_city(place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    cities = get_all_cities()
    city = find_city(cities, city_id)
    if city is None:
        abort(404)
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' not in data.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)
    if 'user_id' not in data.keys():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    place = Place()
    place.name = data['name']
    place.user_id = data['user_id']
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = find_place(place_id)
    if place is None:
        abort(404)
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
