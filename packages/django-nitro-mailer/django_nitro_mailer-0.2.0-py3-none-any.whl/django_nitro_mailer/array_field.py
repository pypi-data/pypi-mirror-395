"""
Copied over from django.contrib.postgres.forms.array - cannot be used directly
as it required psycopg2 to be installed when importing.
"""

from typing import Any, ClassVar, Self

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.functional import SimpleLazyObject
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy


class ArrayMaxLengthValidator(MaxLengthValidator):
    message = ngettext_lazy(
        "List contains %(show_value)d item, it should contain no more than %(limit_value)d.",
        "List contains %(show_value)d items, it should contain no more than %(limit_value)d.",
        "limit_value",
    )


class ArrayMinLengthValidator(MinLengthValidator):
    message = ngettext_lazy(
        "List contains %(show_value)d item, it should contain no fewer than %(limit_value)d.",
        "List contains %(show_value)d items, it should contain no fewer than %(limit_value)d.",
        "limit_value",
    )


def prefix_validation_error(error: ValidationError, prefix: str, code: str, params: dict) -> ValidationError:
    """
    Prefix a validation error message while maintaining the existing
    validation data structure.
    """
    if error.error_list == [error]:
        error_params = error.params or {}
        return ValidationError(
            # We can't simply concatenate messages since they might require
            # their associated parameters to be expressed correctly which
            # is not something `format_lazy` does. For example, proxied
            # ngettext calls require a count parameter and are converted
            # to an empty string if they are missing it.
            message=format_lazy(
                "{} {}",
                SimpleLazyObject(lambda: prefix % params),
                SimpleLazyObject(lambda: error.message % error_params),
            ),
            code=code,
            params={**error_params, **params},
        )
    return ValidationError([prefix_validation_error(e, prefix, code, params) for e in error.error_list])


class SimpleArrayField(forms.CharField):
    default_error_messages: ClassVar = {
        "item_invalid": _("Item %(nth)s in the array did not validate:"),
    }

    def __init__(
        self: Self,
        base_field: forms.Field,
        *,
        delimiter: str = ",",
        max_length: int | None = None,
        min_length: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.base_field = base_field
        self.delimiter = delimiter
        super().__init__(**kwargs)
        if min_length is not None:
            self.min_length = min_length
            self.validators.append(ArrayMinLengthValidator(int(min_length)))
        if max_length is not None:
            self.max_length = max_length
            self.validators.append(ArrayMaxLengthValidator(int(max_length)))

    def clean(self: Self, value: str) -> list[Any]:
        value = super().clean(value)
        return [self.base_field.clean(val) for val in value]

    def prepare_value(self: Self, value: str | list[Any]) -> str:
        if isinstance(value, list):
            return self.delimiter.join(str(self.base_field.prepare_value(v)) for v in value)
        return value

    def to_python(self: Self, value: str) -> list[Any]:
        if isinstance(value, list):
            items = value
        elif value:
            items = value.split(self.delimiter)
        else:
            items = []
        errors = []
        values = []
        for index, item in enumerate(items):
            try:
                values.append(self.base_field.to_python(item))
            except ValidationError as error:
                errors.append(
                    prefix_validation_error(
                        error,
                        prefix=self.error_messages["item_invalid"],
                        code="item_invalid",
                        params={"nth": index + 1},
                    )
                )
        if errors:
            raise ValidationError(errors)
        return values

    def validate(self: Self, value: list[Any]) -> None:
        super().validate(value)
        errors = []
        for index, item in enumerate(value):
            try:
                self.base_field.validate(item)
            except ValidationError as error:
                errors.append(
                    prefix_validation_error(
                        error,
                        prefix=self.error_messages["item_invalid"],
                        code="item_invalid",
                        params={"nth": index + 1},
                    )
                )
        if errors:
            raise ValidationError(errors)

    def run_validators(self: Self, value: list[Any]) -> None:
        super().run_validators(value)
        errors = []
        for index, item in enumerate(value):
            try:
                self.base_field.run_validators(item)
            except ValidationError as error:
                errors.append(
                    prefix_validation_error(
                        error,
                        prefix=self.error_messages["item_invalid"],
                        code="item_invalid",
                        params={"nth": index + 1},
                    )
                )
        if errors:
            raise ValidationError(errors)

    def has_changed(self: Self, initial: str, data: str) -> bool:
        try:
            value = self.to_python(data)
        except ValidationError:
            pass
        else:
            if initial in self.empty_values and value in self.empty_values:
                return False
        return super().has_changed(initial, data)
