from django.core.mail import EmailMessage
from django.test import Client
from django.urls import reverse

from django_nitro_mailer.models import Email


def test_admin_email_list_view(admin_client: Client, nitro_database_backend_settings: None) -> None:
    email_message = EmailMessage(
        subject="Test Subject",
        body="Test Body",
        from_email="from@example.com",
        to=["to@example.com"],
    )
    email_message.send()

    url = reverse("admin:django_nitro_mailer_email_changelist")
    response = admin_client.get(url)

    assert response.status_code == 200
    assert "Test Subject" in response.content.decode()


def test_admin_email_detail_view(admin_client: Client, nitro_database_backend_settings: None) -> None:
    email_message = EmailMessage(
        subject="Test Subject",
        body="Test Body",
        from_email="from@example.com",
        to=["to@example.com"],
    )
    email_message.send()

    email_instance = Email.objects.first()

    url = reverse("admin:django_nitro_mailer_email_change", args=[email_instance.id])
    response = admin_client.get(url)

    assert response.status_code == 200
    decoded_content = response.content.decode()
    assert "Test Subject" in decoded_content
    assert "Test Body" in decoded_content
