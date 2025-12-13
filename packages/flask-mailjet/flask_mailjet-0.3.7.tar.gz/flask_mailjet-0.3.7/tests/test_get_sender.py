import pytest
from flask import Flask
from flask_mailjet import Mailjet


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["MAILJET_API_KEY"] = "x"
    app.config["MAILJET_API_SECRET"] = "y"
    with app.app_context():
        yield app


def test_get_sender_explicit_arguments(app):
    mj = Mailjet(app)
    sender = mj._get_sender(name="Tim", email="tim@example.com")

    assert sender == {
        "Email": "tim@example.com",
        "Name": "Tim",
    }


def test_get_sender_uses_config(app):
    app.config["MAILJET_SENDER_NAME"] = "Config Sender"
    app.config["MAILJET_SENDER_EMAIL"] = "cfg@example.com"

    mj = Mailjet(app)
    sender = mj._get_sender()

    assert sender["Email"] == "cfg@example.com"
    assert sender["Name"] == "Config Sender"


def test_get_sender_fallback_defaults(app):
    # No config specified
    mj = Mailjet(app)
    sender = mj._get_sender()

    assert sender["Email"] == "do-not-reply@change-me.org"
    assert sender["Name"] == "Flask-Mailjet Sender"
