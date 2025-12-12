from typing import Any, Self

from django.core.management.base import BaseCommand

from django_nitro_mailer.utils import send_emails


class Command(BaseCommand):
    help = "Send emails using the currently selected django-nitro-mailer backend."

    def handle(self: Self, *args: Any, **options: Any) -> None:
        self.stdout.write("Sending emails")
        result = send_emails()
        msg = f"Successfully sent {result.success_count} email(s)."
        if result.failure_count > 0:
            msg += f" Failed to send {result.failure_count} email(s)."
            self.stderr.write(self.style.WARNING(msg))
        else:
            self.stdout.write(self.style.SUCCESS(msg))
