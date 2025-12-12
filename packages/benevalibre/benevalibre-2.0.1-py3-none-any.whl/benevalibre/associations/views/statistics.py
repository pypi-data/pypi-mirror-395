from benevalibre.associations.tables import (
    AssociationBenevaloCategoryReportTable,
    AssociationBenevaloLevelReportTable,
    AssociationProjectReportTable,
)
from benevalibre.views.base import BaseStatisticsView

from .mixins import AssociationRelatedManagementViewMixin


class StatisticsView(AssociationRelatedManagementViewMixin, BaseStatisticsView):
    permission_required = "associations.view_statistics"
    page_title = "Statistiques"
    seo_title = "Statistiques de l'association"
    template_name = "associations/statistics.html"

    benevalo_categories_ordering_kwarg = "benevalo_categories_ordering"
    benevalo_levels_ordering_kwarg = "benevalo_levels_ordering"
    projects_ordering_kwarg = "projects_ordering"

    def get_benevalo_queryset(self):
        return self.association.benevalos.active()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.has_benevalos:
            context["benevalo_categories_report"] = self.get_report_table(
                AssociationBenevaloCategoryReportTable,
                self.association.benevalo_categories.all(),
                self.benevalo_categories_ordering_kwarg,
            )
            context["benevalo_levels_report"] = self.get_report_table(
                AssociationBenevaloLevelReportTable,
                self.association.benevalo_levels.all(),
                self.benevalo_levels_ordering_kwarg,
            )
            context["projects_report"] = self.get_report_table(
                AssociationProjectReportTable,
                self.association.projects.all(),
                self.projects_ordering_kwarg,
            )
        return context
