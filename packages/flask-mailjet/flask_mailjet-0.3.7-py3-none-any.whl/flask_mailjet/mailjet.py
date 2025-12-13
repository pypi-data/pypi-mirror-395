from __future__ import annotations
import base64
from typing import List, Dict, Any, Union
from mailjet_rest import Client
from flask import Flask, current_app


class Mailjet:
    """Flask extension providing Mailjet email sending support."""

    def __init__(self, app: Flask | None = None) -> None:
        self.client: Client | None = None
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Bind Mailjet client to the Flask app."""
        api_key = app.config.get("MAILJET_API_KEY")
        api_secret = app.config.get("MAILJET_API_SECRET")

        if not api_key or not api_secret:
            raise RuntimeError(
                "Configuration values MAILJET_API_KEY and MAILJET_API_SECRET are required."
            )

        self.client = Client(
            auth=(api_key, api_secret),
            version="v3.1"
        )

        app.extensions["mailjet"] = self

    # ------------------------------------------------------------------
    # Email Sending API
    # ------------------------------------------------------------------
    def _normalize_recipients(self, recipients: Union[str, List[str]]) -> List[Dict[str, str]]:
        if isinstance(recipients, str):
            return [{"Email": recipients}]
        return [{"Email": r} for r in recipients]

    def _get_sender(self, name: str | None = None, email: str | None = None) -> dict:
        """
        Determine sender name and email from config or provided overrides.

        Priority:
        1. Explicit arguments (name/email)
        2. Flask config MAILJET_SENDER_NAME / MAILJET_SENDER_EMAIL
        3. Final fallback: "Flask-Mailjet Sender" + do-not-reply@change-me.org
        """

        cfg = current_app.config

        sender_name = (
                name
                or cfg.get("MAILJET_SENDER_NAME")
                or "Flask-Mailjet Sender"
        )

        sender_email = (
                email
                or cfg.get("MAILJET_SENDER_EMAIL")
                or "do-not-reply@change-me.org"
        )

        return {
            "Email": sender_email,
            "Name": sender_name,
        }

    def send_email(
        self,
        recipients: Union[str, List[str]],
        subject: str,
        html: str,
        sender: Dict[str, str] | None = None,
    ) -> Any:
        """Send a basic HTML email."""
        if self.client is None:
            raise RuntimeError("Mailjet extension not initialized.")

        if sender is None:
            sender = self._get_sender()

        payload = {
            "Messages": [
                {
                    "From": sender,
                    "To": self._normalize_recipients(recipients),
                    "Subject": subject,
                    "HTMLPart": html,
                }
            ]
        }

        return self.client.send.create(data=payload)

    def send_email_with_pdf(
        self,
        recipients: Union[str, List[str]],
        subject: str,
        html: str,
        filename: str,
        file_bytes: bytes,
        content_type: str = "application/pdf",
        sender: Dict[str, str] | None = None,
    ) -> Any:
        """Send an email with a file attachment."""
        if self.client is None:
            raise RuntimeError("Mailjet extension not initialized.")

        encoded = base64.b64encode(file_bytes).decode("utf-8")

        if sender is None:
            sender = self._get_sender()

        payload = {
            "Messages": [
                {
                    "From": sender,
                    "To": self._normalize_recipients(recipients),
                    "Subject": subject,
                    "HTMLPart": html,
                    "Attachments": [
                        {
                            "ContentType": content_type,
                            "Filename": filename,
                            "Base64Content": encoded,
                        }
                    ],
                }
            ]
        }

        return self.client.send.create(data=payload)