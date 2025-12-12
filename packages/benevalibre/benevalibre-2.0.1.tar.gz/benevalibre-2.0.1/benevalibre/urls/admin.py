from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from benevalibre.views.admin import (
    announcements,
    default_benevalo_categories,
    default_benevalo_levels,
    default_roles,
    settings,
    statistics,
)

urlpatterns = [
    path(
        "benevalo-categories/",
        default_benevalo_categories.ViewSet.as_view(
            url_namespace="default_benevalo_categories",
        ),
    ),
    path(
        "benevalo-levels/",
        default_benevalo_levels.ViewSet.as_view(
            url_namespace="default_benevalo_levels",
        ),
    ),
    path(
        "roles/",
        default_roles.ViewSet.as_view(
            url_namespace="default_roles",
        ),
    ),
    path(
        "announcements/",
        announcements.ViewSet.as_view(
            url_namespace="announcements",
        ),
    ),
    path(
        "settings/",
        settings.UpdateView.as_view(),
        name="instance_settings",
    ),
    path(
        "statistics/",
        statistics.StatisticsView.as_view(),
        name="instance_statistics",
    ),
    path(
        "",
        RedirectView.as_view(url=reverse_lazy("instance_settings")),
        name="instance_admin",
    ),
]
