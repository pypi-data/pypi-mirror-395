# Flask-Mailjet

A lightweight Flask extension for sending emails using the Mailjet API.

## Installation

pip install flask-mailjet

## Usage

```python
from flask import Flask
from flask_mailjet import Mailjet

app = Flask(__name__)
app.config["MAILJET_API_KEY"] = "your-key"
app.config["MAILJET_API_SECRET"] = "your-secret"

mailjet = Mailjet(app)

@app.route("/send")
def send():
    mailjet.send_email(
        sender={"Email": "info@example.com", "Name": "Example"},
        recipients="user@example.com",
        subject="Hello",
        html="<h1>Hello World</h1>"
    )
    return "sent"
```


# Build the package

In your project root:

```bash
pip install build
python -m build
```

This produces:
```bash
dist/
    flask_mailjet-0.1.0.tar.gz
    flask_mailjet-0.1.0-py3-none-any.whl
```