from typing import Any, Self

from django import forms
from django.template import Context, Template
from django.utils.translation import gettext_lazy

from django_nitro_mailer.array_field import SimpleArrayField
from django_nitro_mailer.models import Email
from django_nitro_mailer.utils import create_email_message


class EmailAdminForm(forms.ModelForm):
    recipients = SimpleArrayField(
        label=gettext_lazy("Recipients"),
        base_field=forms.EmailField(),
        widget=forms.TextInput(attrs={"class": "vTextField"}),
    )
    subject = forms.CharField(label=gettext_lazy("Subject"), widget=forms.TextInput(attrs={"class": "vTextField"}))
    text_content = forms.CharField(label=gettext_lazy("Text content"), widget=forms.Textarea, required=False)
    html_content = forms.CharField(label=gettext_lazy("HTML content"), widget=forms.Textarea, required=False)
    context = forms.JSONField(
        label=gettext_lazy("Context"),
        required=False,
        initial={},
        help_text=gettext_lazy(
            "JSON context for rendering the email content. "
            "Use double brackets '{{ variable }}' for variable substitution."
        ),
    )

    class Meta:
        model = Email
        fields = ("recipients", "subject", "text_content", "html_content", "context")

    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        if instance := kwargs.get("instance"):
            instance: Email
            kwargs["initial"] = {
                "recipients": instance.recipients,
                "subject": instance.subject,
                "text_content": instance.text_content,
                "html_content": instance.html_content,
            }
        super().__init__(*args, **kwargs)

    def save(self: Self, commit: bool = True) -> Any:
        recipients = self.cleaned_data["recipients"]
        subject = self.cleaned_data["subject"]
        context = Context(self.cleaned_data["context"])
        text_content = Template(self.cleaned_data["text_content"]).render(context)
        html_content = Template(self.cleaned_data["html_content"]).render(context)
        kwargs = {
            "subject": subject,
            "recipients": recipients,
            "html_content": html_content,
            "text_content": text_content,
        }

        self.instance.set_email(create_email_message(**kwargs))

        return super().save(commit)
