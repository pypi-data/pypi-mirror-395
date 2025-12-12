from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count, Prefetch, Q

from benevalibre.accounts.models import User
from benevalibre.associations.models import (
    ActivityField,
    ActivityFieldGroup,
    Association,
    DefaultBenevaloCategory,
)
from benevalibre.tables.admin import DefaultBenevaloCategoryReportTable
from benevalibre.views.base import BaseStatisticsView

from . import AdminViewMixin


class StatisticsView(
    AdminViewMixin,
    UserPassesTestMixin,
    BaseStatisticsView,
):
    page_title = "Statistiques"
    seo_title = "Statistiques de l'instance"
    template_name = "admin/statistics.html"

    benevalo_categories_ordering_kwarg = "benevalo_categories_ordering"

    def test_func(self):
        return self.request.user.is_superuser

    def get_activity_field_groups(self):
        activity_fields_queryset = ActivityField.objects.annotate(
            num_associations=Count(
                "association",
                filter=Q(association__is_active=True),
            ),
        ).order_by("name")

        return (
            ActivityFieldGroup.objects.prefetch_related(
                Prefetch(
                    "activity_fields",
                    queryset=activity_fields_queryset,
                    to_attr="all_activity_fields",
                ),
            )
            .annotate(
                num_associations=Count(
                    "activity_field__association",
                    filter=Q(activity_field__association__is_active=True),
                ),
            )
            .order_by("name")
        )

    def get_global_stats(self):
        return {
            "count_associations": Association.objects.active().count(),
            "count_users": User.objects.active().count(),
            "first_benevalo_date": self.first_benevalo_date,
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["global_stats"] = self.get_global_stats()
        context["activity_field_groups"] = self.get_activity_field_groups()
        if self.has_benevalos:
            context["benevalo_categories_report"] = self.get_report_table(
                DefaultBenevaloCategoryReportTable,
                DefaultBenevaloCategory.objects.all(),
                self.benevalo_categories_ordering_kwarg,
            )
        return context
