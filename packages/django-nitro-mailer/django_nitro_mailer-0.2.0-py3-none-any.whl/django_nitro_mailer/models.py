import pickle
from typing import ClassVar, Self

from django.core.mail import EmailMessage
from django.db import models
from django.utils.functional import cached_property
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _


class EmailDataMixin(models.Model):
    email_data = models.BinaryField(verbose_name=_("email data"))

    class Meta:
        abstract = True

    def set_email(self: Self, email: EmailMessage) -> None:
        self.email_data = pickle.dumps(email)

    @cached_property
    def email(self: Self) -> EmailMessage | None:
        if self.email_data is not None:
            return pickle.loads(self.email_data)  # noqa: S301
        else:
            return None

    @cached_property
    def text_content(self: Self) -> str | None:
        if self.email is not None:
            return self.email.body
        else:
            return None

    @cached_property
    def html_content(self: Self) -> str | None:
        if self.email is not None:
            return escape(self.email.alternatives[0][0]) if getattr(self.email, "alternatives", None) else ""
        else:
            return None

    @cached_property
    def recipients(self: Self) -> list[str]:
        email = self.email
        if email is not None:
            return email.to
        else:
            return []

    @cached_property
    def subject(self: Self) -> str:
        email = self.email
        if email is not None:
            return email.subject
        else:
            return ""


class Email(EmailDataMixin, models.Model):
    class Priorities(models.IntegerChoices):
        DEFERRED = 0, _("Deferred")
        LOW = 10, _("Low")
        MEDIUM = 20, _("Medium")
        HIGH = 30, _("High")

    DEFAULT_PRIORITY = Priorities.MEDIUM

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    priority = models.PositiveSmallIntegerField(
        choices=Priorities.choices,
        default=DEFAULT_PRIORITY,
        verbose_name=_("priority"),
        help_text=_("Determines the order in which emails are sent."),
    )

    class Meta:
        verbose_name = _("email")
        verbose_name_plural = _("emails")

    def __str__(self: Self) -> str:
        return f"{self.subject} [{self.created_at}]"


class EmailLog(EmailDataMixin, models.Model):
    class Results(models.IntegerChoices):
        SUCCESS = 0, _("Success")
        FAILURE = 1, _("Failure")

    result = models.PositiveSmallIntegerField(choices=Results.choices, verbose_name=_("result"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    extra = models.JSONField(default=dict, verbose_name=_("extra"))

    class Meta:
        verbose_name = _("email log")
        verbose_name_plural = _("email logs")

        ordering: ClassVar[list[str]] = ["-created_at"]

    def __str__(self: Self) -> str:
        return f"{self.result}: {self.subject} [{self.created_at}]"

    @classmethod
    def log(cls: type[Self], email: EmailMessage, result: Results, extra: dict | None = None) -> None:
        create_kwargs = {
            "email_data": pickle.dumps(email),
            "result": result,
        }
        if extra:
            create_kwargs["extra"] = extra

        cls.objects.create(**create_kwargs)
