from django.conf import settings


def get_absolute_uri(location):
    return "%s%s" % (settings.BASE_URL.rstrip("/"), location)
