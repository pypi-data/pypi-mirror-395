from flask import render_template


def render_email_template(template_name: str, **context) -> str:
    """
    Renders a Jinja2 email template stored inside:
    flask_mailjet/templates/mailjet/
    """
    return render_template(f"mailjet/{template_name}", **context)
