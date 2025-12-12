import pickle
from unittest.mock import MagicMock, patch

import pytest
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.utils import timezone

from django_nitro_mailer.emails import retry_deferred, send_emails
from django_nitro_mailer.models import Email, EmailLog


@pytest.mark.django_db
def test_set_and_get_email() -> None:
    email_instance = Email.objects.create(email_data=b"")

    email_message = EmailMessage(
        subject="Test Subject",
        body="Test Body",
        from_email="from@example.com",
        to=["to@example.com"],
    )

    email_instance.set_email(email_message)

    assert email_instance.email.subject == "Test Subject"
    assert email_instance.email.body == "Test Body"
    assert email_instance.recipients == ["to@example.com"]


@pytest.mark.django_db
def test_send_emails_with_priorities() -> None:
    high_priority_email = EmailMessage(
        subject="High Priority",
        body="Test Body",
        from_email="from@example.com",
        to=["to@example.com"],
    )
    medium_priority_email = EmailMessage(
        subject="Medium Priority",
        body="Test Body",
        from_email="from@example.com",
        to=["to@example.com"],
    )
    low_priority_email = EmailMessage(
        subject="Low Priority",
        body="Test Body",
        from_email="from@example.com",
        to=["to@example.com"],
    )
    medium_priority_email_2 = EmailMessage(
        subject="Medium Priority",
        body="Test Body",
        from_email="from@example.com",
        to=["to@example.com"],
    )
    low_priority_email_2 = EmailMessage(
        subject="Low Priority",
        body="Test Body",
        from_email="from@example.com",
        to=["to@example.com"],
    )
    deferred_priority_email = EmailMessage(
        subject="Deferred Priority",
        body="Test Body",
        from_email="from@example.com",
        to=["to@example.com"],
    )

    Email.objects.create(email_data=pickle.dumps(high_priority_email), priority=Email.Priorities.HIGH)
    Email.objects.create(email_data=pickle.dumps(medium_priority_email), priority=Email.Priorities.MEDIUM)
    Email.objects.create(email_data=pickle.dumps(low_priority_email), priority=Email.Priorities.LOW)
    Email.objects.create(
        email_data=pickle.dumps(medium_priority_email_2),
        priority=Email.Priorities.MEDIUM,
    )
    Email.objects.create(email_data=pickle.dumps(low_priority_email_2), priority=Email.Priorities.LOW)
    Email.objects.create(
        email_data=pickle.dumps(deferred_priority_email),
        priority=Email.Priorities.DEFERRED,
    )

    assert Email.objects.count() == 6
    assert EmailLog.objects.count() == 0

    send_emails()

    assert Email.objects.count() == 1
    assert EmailLog.objects.count() == 5

    sent_emails = [log.email for log in EmailLog.objects.all().order_by("id")]
    assert sent_emails[0].subject == "High Priority"
    assert sent_emails[1].subject == "Medium Priority"
    assert sent_emails[3].subject == "Low Priority"


@pytest.mark.django_db
@patch("django.core.mail.backends.locmem.EmailBackend.send_messages")
def test_send_emails_no_emails(mock_send_messages: MagicMock) -> None:
    mock_send_messages.return_value = 1

    assert Email.objects.count() == 0
    assert EmailLog.objects.count() == 0

    send_emails()

    assert Email.objects.count() == 0
    assert EmailLog.objects.count() == 0


@pytest.mark.django_db
@patch("django_nitro_mailer.emails.get_connection")
@patch("django.core.mail.backends.locmem.EmailBackend.send_messages")
def test_send_emails_backend_error(mock_send_messages: MagicMock, mock_get_connection: MagicMock) -> None:
    mock_send_messages.side_effect = Exception("Backend error")

    mock_backend = MagicMock()
    mock_get_connection.return_value = mock_backend
    mock_backend.send_messages = mock_send_messages

    email_message = EmailMessage(
        subject="Test Subject",
        body="Test Body",
        from_email="from@example.com",
        to=["to@example.com"],
    )
    Email.objects.create(email_data=pickle.dumps(email_message), priority=Email.Priorities.HIGH)

    assert Email.objects.count() == 1
    assert EmailLog.objects.count() == 0

    send_emails()

    assert Email.objects.count() == 1
    assert EmailLog.objects.count() == 1
    email_log = EmailLog.objects.first()
    assert email_log.result == EmailLog.Results.FAILURE
    assert email_log.email_data == pickle.dumps(email_message)


@pytest.mark.django_db
def test_send_mass_email_success(nitro_database_backend_settings: None) -> None:
    message1 = (
        "Subject 1",
        "Message 1",
        "from@example.com",
        ["to1@example.com", "to2@example.com", "to3@example.com"],
    )
    message2 = ("Subject 2", "Message 2", "from@example.com", ["to2@example.com"])
    message3 = ("Subject 3", "Message 3", "from@example.com", ["to3@example.com"])

    send_mass_mail((message1, message2, message3), fail_silently=False)

    assert Email.objects.count() == 3
    assert EmailLog.objects.count() == 0

    send_emails(Email.objects.all())

    assert EmailLog.objects.filter(result=EmailLog.Results.SUCCESS).count() == 3


@pytest.mark.django_db
@patch("django.core.mail.backends.locmem.EmailBackend.send_messages")
def test_sync_backend_sends_email(mock_send_messages: MagicMock, nitro_sync_backend_settings: None) -> None:
    send_mail(
        subject="Test Subject",
        message="Test Body",
        from_email="from@example.com",
        recipient_list=["to@example.com"],
        fail_silently=False,
    )

    assert Email.objects.count() == 0
    assert EmailLog.objects.filter(result=EmailLog.Results.SUCCESS).count() == 1
    mock_send_messages.assert_called_once()


@pytest.mark.django_db
@patch("django.core.mail.backends.locmem.EmailBackend.send_messages", return_value=0)
def test_sync_backend_sends_email_failure(mock_send_messages: MagicMock, nitro_sync_backend_settings: None) -> None:
    send_mail(
        subject="Test Subject",
        message="Test Body",
        from_email="from@example.com",
        recipient_list=["to@example.com"],
        fail_silently=False,
    )

    assert Email.objects.count() == 0
    assert EmailLog.objects.filter(result=EmailLog.Results.FAILURE).count() == 1


@pytest.mark.django_db
def test_retry_deferred() -> None:
    email_message = EmailMessage(
        subject="Test Subject",
        body="This is a test email.",
        from_email="sender@example.com",
        to=["recipient@example.com"],
    )
    email_data = pickle.dumps(email_message)
    deferred_email = Email.objects.create(email_data=email_data, priority=Email.Priorities.DEFERRED)

    assert Email.objects.filter(id=deferred_email.id).exists()

    retry_deferred()

    assert not Email.objects.filter(id=deferred_email.id).exists()


@pytest.mark.django_db
def test_send_emails_called_with_deferred() -> None:
    email_message = EmailMessage(
        subject="Test Subject",
        body="This is a test email.",
        from_email="sender@example.com",
        to=["recipient@example.com"],
    )
    email_data = pickle.dumps(email_message)
    deferred_email = Email.objects.create(email_data=email_data, priority=Email.Priorities.DEFERRED)
    Email.objects.create(email_data=email_data, priority=Email.Priorities.LOW)

    assert Email.objects.filter(id=deferred_email.id).exists()

    retry_deferred()

    assert not Email.objects.filter(id=deferred_email.id).exists()

    log_entry = EmailLog.objects.filter(email_data=email_data).first()
    assert log_entry is not None
    assert log_entry.result == EmailLog.Results.SUCCESS
    assert log_entry.created_at <= timezone.now()


@pytest.mark.django_db
def test_no_deferred_emails_does_not_send_regular_emails() -> None:
    email_message = EmailMessage(
        subject="Test Subject",
        body="This is a test email.",
        from_email="sender@example.com",
        to=["recipient@example.com"],
    )
    email_data = pickle.dumps(email_message)
    Email.objects.create(email_data=email_data, priority=Email.Priorities.LOW)

    retry_deferred()

    assert Email.objects.count() == 1
