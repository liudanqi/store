#!/usr/bin/env python3
import pytest
from flask import Flask
from flask.testing import FlaskClient
# from seller.call import bp


@pytest.fixture
def client() -> FlaskClient:
    app: Flask = Flask(__name__)
    app.register_blueprint(bp)
    client: FlaskClient = app.test_client()
    return client
