import os
import pytest
from flask import Flask
from flask_mailjet.loader import render_email_template


@pytest.fixture
def app():
    # Absolute path to src/flask_mailjet/templates
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "flask_mailjet", "templates"))

    app = Flask(
        __name__,
        template_folder=root
    )
    with app.app_context():
        yield app


def test_template_rendering(app):
    html = render_email_template("base.html", subject="Hello")
    assert "<title>Hello</title>" in html


def test_template_rendering_context(app):
    html = render_email_template("base.html", subject="Hi", user="Tim")
    assert "Tim" in html or "Hi" in html


def test_template_missing(app):
    with pytest.raises(Exception):
        render_email_template("does_not_exist.html")
