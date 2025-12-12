from benevalibre import __version__
from benevalibre.models import InstanceSettings


def app_version(request):
    return {"app_version": __version__}


def instance(request):
    return {
        "instance_settings": InstanceSettings.for_request(request),
    }
