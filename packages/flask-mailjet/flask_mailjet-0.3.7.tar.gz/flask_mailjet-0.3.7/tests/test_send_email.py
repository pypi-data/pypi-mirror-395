from unittest.mock import MagicMock
from flask import Flask
from flask_mailjet import Mailjet


def make_app():
    app = Flask(__name__)
    app.config["MAILJET_API_KEY"] = "x"
    app.config["MAILJET_API_SECRET"] = "y"
    return app


class DummySend:
    """Replacement for client.send so we can mock create()."""
    def __init__(self):
        self.create = MagicMock(return_value={"Status": "success"})


def test_send_email_payload(monkeypatch):
    app = make_app()
    mj = Mailjet(app)

    dummy_send = DummySend()
    # Replace the entire send object
    mj.client.send = dummy_send

    with app.app_context():
        mj.send_email(
            recipients="a@example.com",
            subject="Hello",
            html="<b>Hi</b>",
        )

    # Now this exists because we replaced send entirely
    payload = dummy_send.create.call_args.kwargs["data"]
    msg = payload["Messages"][0]

    assert msg["To"] == [{"Email": "a@example.com"}]
    assert msg["Subject"] == "Hello"
    assert msg["HTMLPart"] == "<b>Hi</b>"
    assert msg["From"]["Email"] == "do-not-reply@change-me.org"


def test_send_email_with_pdf_payload(monkeypatch):
    app = make_app()
    mj = Mailjet(app)

    dummy_send = DummySend()
    mj.client.send = dummy_send

    with app.app_context():
        mj.send_email_with_pdf(
            recipients="a@example.com",
            subject="PDF",
            html="<p>Hello</p>",
            filename="test.pdf",
            file_bytes=b"123456",
        )

    payload = dummy_send.create.call_args.kwargs["data"]
    msg = payload["Messages"][0]
    att = msg["Attachments"][0]

    assert att["Filename"] == "test.pdf"
    assert att["ContentType"] == "application/pdf"
    assert att["Base64Content"] == "MTIzNDU2"
