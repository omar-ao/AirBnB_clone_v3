#!/usr/bin/python3

"""
This is `app' module that runs the Flask application
for the AirBnB_clone API"""


from api.v1.views import app_views
from flask import Flask, Blueprint
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Close db storage on app teardown"""
    storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
