#!/usr/bin/python3

"""This is `index` module that contains the index view"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
