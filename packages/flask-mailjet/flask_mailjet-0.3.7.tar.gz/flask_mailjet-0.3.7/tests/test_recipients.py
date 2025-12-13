from flask_mailjet import Mailjet


def test_normalize_single_recipient():
    mj = Mailjet()
    result = mj._normalize_recipients("test@example.com")
    assert result == [{"Email": "test@example.com"}]


def test_normalize_multiple_recipients():
    mj = Mailjet()
    result = mj._normalize_recipients(["a@example.com", "b@example.com"])
    assert result == [
        {"Email": "a@example.com"},
        {"Email": "b@example.com"},
    ]
