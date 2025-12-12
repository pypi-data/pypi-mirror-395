import logging
from collections.abc import Iterable
from typing import Self

from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage

from django_nitro_mailer import defaults as nitro_defaults
from django_nitro_mailer.emails import SendEmailsResult, throttle_email_delivery
from django_nitro_mailer.models import Email
from django_nitro_mailer.utils import send_email_message

logger = logging.getLogger(__name__)


class DatabaseBackend(BaseEmailBackend):
    def send_messages(self: Self, email_messages: Iterable[EmailMessage]) -> int:
        email_list = []
        for email_obj in email_messages:
            email = Email()
            email.set_email(email_obj)
            email_list.append(email)

        email_db_list = Email.objects.bulk_create(email_list, batch_size=1000)
        return len(email_db_list)


class SyncBackend(BaseEmailBackend):
    def send_messages(self: Self, email_messages: Iterable[EmailMessage]) -> int:
        nitro_email_backend = getattr(settings, "NITRO_EMAIL_BACKEND", nitro_defaults.NITRO_EMAIL_BACKEND)
        connection = get_connection(nitro_email_backend)

        result = SendEmailsResult(success_count=0, failure_count=0)
        for email_message in email_messages:
            if send_email_message(email_message, connection):
                result.success_count += 1
            else:
                result.failure_count += 1

            throttle_email_delivery()

        return result.success_count
