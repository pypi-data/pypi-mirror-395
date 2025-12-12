from django.conf import settings
from django.urls import include, path
from django.views.generic.base import RedirectView

from benevalibre.accounts import urls as accounts_urls
from benevalibre.api import api
from benevalibre.associations import urls as associations_urls
from benevalibre.urls import admin as admin_urls
from benevalibre.views import home, user_benevalos

urlpatterns = [
    path("api/v1/", api.urls),
    path("admin/", include(admin_urls)),
    path("account/", include(accounts_urls, namespace="account")),
    path("associations/", include(associations_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views import defaults as default_views

    from benevalibre.views.styleguide import StyleGuideView

    urlpatterns += [
        path(
            "styleguide/",
            StyleGuideView.as_view(),
            name="styleguide",
        ),
        # Sers les pages d'erreurs afin de les mettre en forme
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

    # Sers les médias et les fichiers statiques
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns.insert(0, path("__debug__/", include("debug_toolbar.urls")))

urlpatterns += [
    path(
        "my-benevalos/",
        user_benevalos.ViewSet.as_view(
            url_namespace="user_benevalos",
        ),
    ),
    path("dashboard/", home.DashboardView.as_view(), name="dashboard"),
    path("", home.WelcomeView.as_view(), name="welcome"),
]

# FIXME: Redirige les URLs les plus utilisées de la version 1.x vers les
# nouvelles. Ces redirections seront à supprimer lors de la version 3.x.
urlpatterns += [
    path(
        "association/<int:pk>/",
        RedirectView.as_view(
            pattern_name="associations:detail",
            permanent=True,
        ),
    ),
    path(
        "board/",
        RedirectView.as_view(
            pattern_name="dashboard",
            permanent=True,
        ),
    ),
    path(
        "docs/",
        RedirectView.as_view(
            url="https://docs.benevalibre.org",
            permanent=True,
        ),
    ),
    path(
        "docs/<path:path>",
        RedirectView.as_view(url="https://docs.benevalibre.org"),
    ),
]
