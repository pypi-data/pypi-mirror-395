import logging

from django.core.mail import send_mail
from django.template.loader import render_to_string

from benevalibre.models import InstanceSettings

logger = logging.getLogger("benevalibre.notifications")


def notify_user(user, action, context):
    """Notifie par mail un⋅e utilisateur⋅rice d'une action."""
    subject, message = render_action_mail(action, context)

    try:
        user.email_user(subject, message)
    except Exception:
        logger.exception(
            "Failed to send '%s' notification email to %r",
            action,
            user,
        )


def notify_users(users, action, context):
    """Notifie par un seul mail plusieurs utilisateur⋅rices d'une action."""
    subject, message = render_action_mail(action, context)

    try:
        send_mail(
            subject,
            message,
            from_email=None,
            recipient_list=users.values_list("email", flat=True),
        )
    except Exception:
        logger.exception(
            "Failed to send '%s' notification email to each user",
            action,
        )


def render_action_mail(action, context):
    email_template_name = f"notifications/{action}_email.txt"
    subject_template_name = f"notifications/{action}_email_subject.txt"

    context["site_name"] = InstanceSettings.objects.get_current().site_name

    subject = render_to_string(subject_template_name, context)
    subject = "".join(subject.splitlines())

    message = render_to_string(email_template_name, context)

    return (subject, message)
