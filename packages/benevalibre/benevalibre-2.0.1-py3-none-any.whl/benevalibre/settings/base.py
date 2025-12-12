"""
Django settings for Bénévalibre project.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

import os.path
import sys
from email.utils import getaddresses
from pathlib import Path
from urllib.parse import urlparse

from django.urls import reverse_lazy

import environ

env = environ.Env()

default_base_dir = Path(__file__).parents[2]

config_file = env(
    "CONFIG_FILE",
    cast=Path,
    default=Path.cwd() / "config.env",
)
if config_file.is_file():
    # Use this directory as the default one for BASE_DIR
    default_base_dir = config_file.parent
    # Load config.env and overwrite OS environment variables
    env.read_env(config_file, overwrite=True)

# Path to the base directory of the app instance
base_dir = env("BASE_DIR", cast=Path, default=default_base_dir)

# Local directory used for static and templates overrides
local_dir = base_dir / "local"

# Directory for variable stuffs, i.e. user-uploaded media
var_dir = base_dir / "var"
var_dir.mkdir(mode=0o755, exist_ok=True)

# Base URL on which the application is served without trailing slash
BASE_URL = env("BASE_URL", default="http://127.0.0.1:8000")

# Location on which the application is served
APP_PATH = urlparse(BASE_URL).path or "/"

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", default="runserver" in sys.argv)

# Local time zone for this installation
TIME_ZONE = "Europe/Paris"

# https://docs.djangoproject.com/en/stable/ref/settings/#language-code
LANGUAGE_CODE = "fr"

# https://docs.djangoproject.com/en/stable/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/stable/ref/settings/#use-tz
USE_TZ = True

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
# https://django-environ.readthedocs.io/en/stable/#supported-types
DATABASES = {
    "default": env.db(
        "DJANGO_DATABASE_URL",
        default="sqlite:///%s" % (base_dir / "sqlite.db"),
    )
}

# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#root-urlconf
ROOT_URLCONF = "benevalibre.urls"
# https://docs.djangoproject.com/en/stable/ref/settings/#wsgi-application
WSGI_APPLICATION = "benevalibre.wsgi.application"

# APP CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#installed-apps
INSTALLED_APPS = [
    "benevalibre",
    "benevalibre.accounts",
    "benevalibre.associations",
    # FIXME: anciennes applications qu'on garde pour les migrations. Elles
    # seront à supprimer lors de la version 3.x, ce qui demandera de ne plus
    # séparer `state_operations` de `database_operations` dans les migrations
    # associations.0001_initial et benevalibre.0001_initial.
    "benevalibre.deprecated.association",
    "benevalibre.deprecated.benevalo",
    "benevalibre.deprecated.instance",
    # Third party libraries
    "django_cotton",
    "django_countries",
    "django_filters",
    "django_tables2",
    "reversion",
    "rules.apps.AutodiscoverRulesConfig",
    "sorl.thumbnail",
    # Django
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    # django-cleanup doit être la dernière application chargée, voir :
    # https://github.com/un1t/django-cleanup#configuration
    "django_cleanup.apps.CleanupConfig",
]

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#auth
AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = (
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
)

LOGIN_URL = reverse_lazy("account:login")
LOGIN_REDIRECT_URL = reverse_lazy("dashboard")
LOGOUT_REDIRECT_URL = LOGIN_URL

PASSWORD_RESET_TIMEOUT = 3 * 86400  # 3 jours

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/topics/auth/passwords/#password-validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        )
    },
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "reversion.middleware.RevisionMiddleware",
    "benevalibre.associations.middleware.AnonymousMemberMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#static-files
STATIC_ROOT = str(var_dir / "static")

# https://docs.djangoproject.com/en/stable/ref/settings/#static-url
STATIC_URL = os.path.join(APP_PATH, "static/")

# https://docs.djangoproject.com/en/stable/ref/settings/#staticfiles-dirs
if (local_dir / "static").is_dir():
    STATICFILES_DIRS = [str(local_dir / "static")]

# https://docs.djangoproject.com/en/stable/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#media-root
MEDIA_ROOT = str(var_dir / "media")

# https://docs.djangoproject.com/en/stable/ref/settings/#media-url
MEDIA_URL = os.path.join(APP_PATH, "media/")

# https://docs.djangoproject.com/en/stable/ref/settings/#file-upload-directory-permissions
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
# https://docs.djangoproject.com/en/stable/ref/settings/#file-upload-permissions
FILE_UPLOAD_PERMISSIONS = 0o644

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "benevalibre.context_processors.app_version",
                "benevalibre.context_processors.instance",
            ],
            "builtins": [
                "benevalibre.templatetags.builtins",
            ],
        },
    }
]
if (local_dir / "templates").is_dir():
    TEMPLATES[0]["DIRS"] = [str(local_dir / "templates")]

# FORMS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#form-renderer
FORM_RENDERER = "benevalibre.forms.FormRenderer"

# Use "https" instead of "http" as the default value of URLField.assume_scheme
# during Django 5.x release cycle - it will be the default value in Django 6.0.
FORMS_URLFIELD_ASSUME_HTTPS = True

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/topics/email/#email-backends
# https://django-environ.readthedocs.io/en/stable/#supported-types
vars().update(env.email_url("DJANGO_EMAIL_URL", default="smtp://localhost:25"))

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="webmaster@localhost")

# Use the same email address for error messages
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ADMIN
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#admins
ADMINS = getaddresses([env("ADMINS", default="root@localhost")])

# https://docs.djangoproject.com/en/stable/ref/settings/#managers
MANAGERS = ADMINS

# SESSIONS AND COOKIES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#session-cookie-path
SESSION_COOKIE_PATH = APP_PATH

# https://docs.djangoproject.com/en/stable/ref/settings/#csrf-cookie-path
CSRF_COOKIE_PATH = APP_PATH

# ------------------------------------------------------------------------------
# APPLICATION AND 3RD PARTY LIBRARY SETTINGS
# ------------------------------------------------------------------------------

"""
A boolean that specifies whether registration by users of new associations is
currently permitted.
"""
ASSOCIATION_REGISTRATION_OPEN = env.bool(
    "ASSOCIATION_REGISTRATION_OPEN", default=True
)

"""
A boolean that specifies whether newly registered associations must be approved
and enabled by administrators.
"""
ASSOCIATION_REGISTRATION_MODERATED = env.bool(
    "ASSOCIATION_REGISTRATION_MODERATED", default=False
)

"""
A boolean that specifies whether registration of new user accounts is currently
permitted.
"""
USER_REGISTRATION_OPEN = env.bool("USER_REGISTRATION_OPEN", default=True)

"""
An integer indicating how long - in secondes - an user account activation link
is valid for.
"""
USER_ACTIVATION_TIMEOUT = PASSWORD_RESET_TIMEOUT

# DJANGO COTTON
# ------------------------------------------------------------------------------
# https://django-cotton.com/docs/configuration
COTTON_DIR = "components"
COTTON_ENABLE_CONTEXT_ISOLATION = True
