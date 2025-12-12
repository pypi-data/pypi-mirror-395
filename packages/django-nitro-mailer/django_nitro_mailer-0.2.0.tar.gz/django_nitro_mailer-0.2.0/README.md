<p align="center">
    <img src="https://raw.githubusercontent.com/majikode/django-nitro-mailer/refs/heads/main/docs/assets/django-nitro-mailer-logo.png" width="200">
    <p align="center">📨 Django mails. Supercharged.</p>
</p>
<p align="center">
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/django-nitro-mailer">
    <img alt="Test Status" src="https://github.com/majikode/django-nitro-mailer/actions/workflows/tests.yml/badge.svg"> 
</p>

## Overview

`django-nitro-mailer` is a pluggable Django app that provides extra email reliability and observability in form of email backends that can be used with Django's built-in functions and other email backend.

`django-nitro-mailer` by itself does not provide a way to send emails, but it puts an extra layer before the email backend to provide extra features like:

* priority queueing
* retrying failed emails
* logging and traces
* email throttling
* sending messages through the admin panel

## Requirements

* Python >= 3.12, < 3.14
* Django >= 5.2, <= 6.0

## Installation

Install the package using pip:

```bash
$ pip install django-nitro-mailer
```

## Usage

1. Add `django_nitro_mailer` to your `INSTALLED_APPS` in your `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "django_nitro_mailer",
    ...
]
```

2. Run `python manage.py migrate` to create the necessary tables.

3. Change the `EMAIL_BACKEND` setting in your `settings.py` to use the desired backend:

* **Database Backend**: Store emails in the database and send them asynchronously. Requires sending a cron job or some other scheduled task to send the emails.

```python
EMAIL_BACKEND = "django_nitro_mailer.backends.DatabaseBackend"
```

* **Sync Backend**: Send emails synchronously. Does not provide the reliability that the database backend provides, but still provides the logging and throttling features.

```python
EMAIL_BACKEND = "django_nitro_mailer.backends.SyncBackend"
```

## Documentation

Documentation is available [here](https://majikode.github.io/django-nitro-mailer/).

## License

`django-nitro-mailer` is under the terms of the [MIT License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](LICENSE).
