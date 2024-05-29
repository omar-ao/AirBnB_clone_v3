#!/usr/bin/python3

"""This is `reviews` module that handles all
default RESTFul API actions for cities"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review


def get_all_places():
    """Gets all places objects"""
    objects = storage.all()
    places = [v for k, v in objects.items() if v.__class__ == Place]
    return places


def find_place(places, place_id):
    """Finds place by id in places objects"""
    place = [place for place in places if place.id == place_id]
    if place == []:
        return None
    return place[0]


def find_review(review_id):
    reviews = storage.all(Review)
    key = '{}.{}'.format('Review', review_id)
    return reviews.get(key)


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    places = get_all_places()
    place = find_place(places, place_id)
    if place is None:
        abort(404)
    objs = storage.all(Review).items()
    reviews = [v.to_dict() for k, v in objs if v.place_id == place_id]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = find_review(review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = find_place(review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    places = get_all_places()
    place = find_place(places, place_id)
    if place is None:
        abort(404)
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'text' not in data.keys():
        return make_response(jsonify({"error": "Missing text"}), 400)
    if 'user_id' not in data.keys():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    review = Review()
    review.text = data['text']
    review.user_id = data['user_id']
    review.place_id = place_id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = find_review(review_id)
    if review is None:
        abort(404)
    if request.content_type != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
