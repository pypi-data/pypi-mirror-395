from flask import Flask
from flask_mailjet.loader import render_email_template


def test_template_rendering():
    app = Flask(__name__, template_folder="../src/flask_mailjet/templates")
    with app.app_context():
        output = render_email_template("base.html", subject="Hello")
        assert "<title>Hello</title>" in output
