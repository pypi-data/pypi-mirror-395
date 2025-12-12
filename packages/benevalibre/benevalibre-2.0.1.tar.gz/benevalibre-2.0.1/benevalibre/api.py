from django.conf import settings

from ninja import NinjaAPI
from ninja.throttling import AnonRateThrottle

from benevalibre.associations.api import router as associations_router

api = NinjaAPI(
    version="1.0.0",
    urls_namespace="api",
    docs_url="/docs" if settings.DEBUG else None,
    # Utilise la valeur définis dans les settings
    throttle=[AnonRateThrottle()],
)
api.add_router("/associations/", associations_router)
