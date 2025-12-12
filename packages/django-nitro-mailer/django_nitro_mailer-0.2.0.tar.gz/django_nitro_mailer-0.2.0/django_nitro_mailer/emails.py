import logging
from dataclasses import dataclass

from django.conf import settings
from django.core.mail import get_connection
from django.db import transaction
from django.db.models.query import QuerySet

from django_nitro_mailer import defaults as nitro_defaults
from django_nitro_mailer.models import Email
from django_nitro_mailer.utils import send_email_message, throttle_email_delivery

logger = logging.getLogger(__name__)


@dataclass
class SendEmailsResult:
    success_count: int
    failure_count: int


def send_emails(queryset: QuerySet | None = None) -> SendEmailsResult:
    if queryset is None:
        queryset = Email.objects.exclude(priority=Email.Priorities.DEFERRED).order_by("-priority", "created_at")

    result = SendEmailsResult(success_count=0, failure_count=0)

    nitro_email_backend = getattr(settings, "NITRO_EMAIL_BACKEND", nitro_defaults.NITRO_EMAIL_BACKEND)
    connection = get_connection(nitro_email_backend)
    with transaction.atomic():
        for email_obj in queryset.select_for_update(nowait=True):
            email_message = email_obj.email
            if email_obj.email:
                if send_email_message(email_message, connection):
                    email_obj.delete()
                    result.success_count += 1
                else:
                    result.failure_count += 1
            else:
                logger.error("Unable to deserialize email", extra={"email_id": email_obj.id})
                result.failure_count += 1

            throttle_email_delivery()

    return result


def retry_deferred() -> SendEmailsResult:
    deferred_emails = Email.objects.filter(priority=Email.Priorities.DEFERRED)
    return send_emails(deferred_emails)
