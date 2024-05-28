#!/usr/bin/python3

"""This is `amenities` module that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
def get_amenities():
    amenities = [v.to_dict() for k, v in storage.all(Amenity).items()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenities = storage.all(Amenity)
    key = '{}.{}'.format('Amenity', amenity_id)
    if key not in amenities.keys():
        abort(404)
    return jsonify(amenities[key].to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenities = storage.all(Amenity)
    key = '{}.{}'.format('Amenity', amenity_id)
    if key not in amenities.keys():
        abort(404)
    storage.delete(amenities[key])
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' not in data.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)

    am = Amenity()
    am.name = data['name']
    storage.new(am)
    storage.save()
    return jsonify(am.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenities = storage.all(Amenity)
    key = '{}.{}'.format('Amenity', amenity_id)
    if key not in amenities.keys():
        abort(404)
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    am = amenities[key]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(am, key, value)
    am.save()
    return jsonify(am.to_dict()), 200
