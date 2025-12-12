"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env, var_dir

BASE_URL = "https://benevalibre.local"

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#debug
DEBUG = False

# https://docs.djangoproject.com/en/stable/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY", default="CHANGEME!!!")

# https://docs.djangoproject.com/en/stable/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
# https://docs.djangoproject.com/en/stable/ref/settings/#email-host
EMAIL_HOST = "localhost"
# https://docs.djangoproject.com/en/stable/ref/settings/#email-port
EMAIL_PORT = 1025

# MEDIA
# ------------------------------------------------------------------------------
# Use a different folder to prevent conflicts
MEDIA_ROOT = str(var_dir / "test-media")

# ------------------------------------------------------------------------------
# APPLICATION AND 3RD PARTY LIBRARY SETTINGS
# ------------------------------------------------------------------------------
# Force the default values instead of those defined in config.env
ASSOCIATION_REGISTRATION_OPEN = True
ASSOCIATION_REGISTRATION_MODERATED = False
USER_REGISTRATION_OPEN = True
