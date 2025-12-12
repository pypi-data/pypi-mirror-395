from typing import Self

from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import URLPattern, path
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from django_nitro_mailer.emails import send_emails
from django_nitro_mailer.forms import EmailAdminForm
from django_nitro_mailer.models import Email, EmailLog


@admin.action(description=_("Send selected emails"))
def send_selected_emails(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    result = send_emails(queryset)
    msg = gettext("Successfully sent %(success_count)d email(s).") % {"success_count": result.success_count}
    if result.failure_count > 0:
        msg += " "
        msg += gettext("Failed to send %(failure_count)d email(s).") % {"failure_count": result.failure_count}
        messages.warning(request, msg)
    else:
        messages.success(request, msg)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    change_form_template = "django_nitro_mailer/admin/email_change_form.html"

    form = EmailAdminForm
    list_display = ("subject", "recipients", "created_at", "priority")
    actions = (send_selected_emails,)

    def get_urls(self: Self) -> list[URLPattern]:
        urls = super().get_urls()
        custom_urls = [
            path(
                "send-email/<int:email_id>/",
                self.admin_site.admin_view(self.send_email),
                name="send_email",
            ),
        ]
        return custom_urls + urls

    def send_email(self: Self, request: HttpRequest, email_id: int) -> HttpResponse:
        email = Email.objects.filter(id=email_id)
        result = send_emails(queryset=email)
        if result.success_count > 0:
            messages.success(request, gettext("Email sent successfully."))
        else:
            messages.error(request, gettext("Failed to send email."))

        app_label = self.opts.app_label
        model_name = self.opts.model_name
        return redirect(f"admin:{app_label}_{model_name}_changelist")


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("subject", "recipients", "result", "created_at")
    fieldsets = (
        (
            None,
            {"fields": ["result", "extra", "created_at"]},
        ),
        (
            _("Email data"),
            {"fields": ["subject", "recipients", "text_content", "html_content"]},
        ),
    )

    @admin.display(description=_("Subject"))
    def subject(self: Self, obj: EmailLog) -> str:
        return obj.subject

    @admin.display(description=_("Recipients"))
    def recipients(self: Self, obj: EmailLog) -> str:
        return ", ".join(obj.recipients)

    @admin.display(description=_("Text content"))
    def text_content(self: Self, obj: EmailLog) -> str:
        return obj.text_content

    @admin.display(description=_("HTML content"))
    def html_content(self: Self, obj: EmailLog) -> str:
        return obj.html_content

    def has_add_permission(self: Self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self: Self, request: HttpRequest, obj: EmailLog | None = None) -> bool:
        return False
