import pytest
from flask import Flask
from flask_mailjet import Mailjet


def test_extension_init():
    app = Flask(__name__)
    app.config["MAILJET_API_KEY"] = "test"
    app.config["MAILJET_API_SECRET"] = "test"

    mj = Mailjet(app)
    assert "mailjet" in app.extensions
    assert mj.client is not None


def test_extension_init_missing_config():
    app = Flask(__name__)
    # No config set -> must raise
    with pytest.raises(RuntimeError):
        Mailjet(app)
