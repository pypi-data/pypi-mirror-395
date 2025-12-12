import logging
import time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage
from django.utils import timezone

from django_nitro_mailer import defaults as nitro_defaults
from django_nitro_mailer.models import EmailLog

logger = logging.getLogger(__name__)


def create_email_message(
    subject: str,
    recipients: list[str],
    text_content: str,
    html_content: str | None = None,
    from_email: str | None = None,
    attachments: list[str] | None = None,
) -> EmailMultiAlternatives:
    email = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=from_email, to=recipients, attachments=attachments
    )
    if html_content:
        email.attach_alternative(html_content, "text/html")

    return email


def send_email_message(email_data: EmailMessage, connection: BaseEmailBackend) -> bool:
    nitro_email_database_logging = getattr(
        settings, "NITRO_EMAIL_DATABASE_LOGGING", nitro_defaults.NITRO_EMAIL_DATABASE_LOGGING
    )

    try:
        successful = bool(connection.send_messages([email_data]))

        if nitro_email_database_logging:
            EmailLog.log(email=email_data, result=EmailLog.Results.SUCCESS if successful else EmailLog.Results.FAILURE)

        logger.info(
            "Email sent successfully",
            extra={"recipients": email_data.recipients, "created_at": timezone.now()},
        )
    except Exception as e:
        if nitro_email_database_logging:
            EmailLog.log(email=email_data, result=EmailLog.Results.FAILURE, extra={"exc_info": str(e)})

        logger.exception("Failed to send email", exc_info=e)
        return False

    return successful


def throttle_email_delivery() -> None:
    throttle_delay = getattr(settings, "NITRO_EMAIL_SEND_THROTTLE_MS", nitro_defaults.NITRO_EMAIL_SEND_THROTTLE_MS)
    if throttle_delay > 0:
        logger.debug("Throttling email delivery. Sleeping for %d milliseconds", throttle_delay)
        time.sleep(throttle_delay / 1000)
