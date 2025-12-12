"""
Production settings.

- validate the configuration
- disable debug mode
- load secret key from environment variables
- set other production configurations
"""

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa
from .base import env, var_dir

# CONFIGURATION VALIDATION
# ------------------------------------------------------------------------------
if not env("DJANGO_DATABASE_URL", default=None):
    raise ImproperlyConfigured(
        "Aucune configuration pour la base de données n'a été définie, "
        "veuillez vérifier la valeur de DATABASE_URL depuis le fichier de "
        "configuration ou les variables d'environnement."
    )

if not env("DEFAULT_FROM_EMAIL", default=None):
    raise ImproperlyConfigured(
        "Aucune adresse mail par défaut pour l'expédition n'a été définie, "
        "veuillez vérifier la valeur de DEFAULT_FROM_EMAIL depuis le fichier "
        "de configuration ou les variables d'environnement."
    )

if not env("BASE_URL", default=None):
    raise ImproperlyConfigured(
        "Aucune URL de base de l'application a été définie, "
        "veuillez vérifier la valeur de BASE_URL depuis le fichier de "
        "configuration ou les variables d'environnement."
    )

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

# https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

# STATICS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#storages
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
        ),
    },
}

# SESSIONS AND COOKIES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#session-cookie-samesite
SESSION_COOKIE_SAMESITE = env("COOKIE_SAMESITE", default="Lax")

# https://docs.djangoproject.com/en/stable/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/stable/ref/settings/#csrf-cookie-samesite
CSRF_COOKIE_SAMESITE = SESSION_COOKIE_SAMESITE

# https://docs.djangoproject.com/en/stable/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE

# LOGGING
# ------------------------------------------------------------------------------
log_dir = var_dir / "log"
log_dir.mkdir(mode=0o755, exist_ok=True)

# https://docs.djangoproject.com/en/stable/topics/logging/
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(levelname)s - %(module)s: %(message)s"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(log_dir / "benevalibre.log"),
            "formatter": "verbose",
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,
        },
    },
    "loggers": {
        "django": {
            "level": "WARNING",
            "handlers": ["file"],
            "propagate": True,
        },
        "django.request": {
            "level": "WARNING",
            "handlers": ["file", "mail_admins"],
            "propagate": False,
        },
        "benevalibre": {
            "level": "INFO",
            "handlers": ["file", "mail_admins"],
            "propagate": True,
        },
    },
}

# ------------------------------------------------------------------------------
# APPLICATION AND 3RD PARTY LIBRARY SETTINGS
# ------------------------------------------------------------------------------

# DJANGO NINJA
# ------------------------------------------------------------------------------
# https://django-ninja.dev/reference/settings/
NINJA_DEFAULT_THROTTLE_RATES = {
    # Limite fortement l'accès à l'API vu son usage actuel, une migration ne
    # devrait pas faire plus de 2 appels consécutifs (GET puis POST)
    "anon": "4/min",
}
