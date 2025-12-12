from django.db.models import Count, Q, Sum

import django_tables2 as tables

from benevalibre.utils.formats import distance_format, duration_format


class DefaultBenevaloCategoryReportTable(tables.Table):
    name = tables.Column(verbose_name="Catégorie de bénévolat")
    count_benevalos = tables.Column(verbose_name="Nombre de saisies")
    count_associations = tables.Column(verbose_name="Associations concernées")
    count_members = tables.Column(verbose_name="Membres concerné⋅es")
    total_duration = tables.Column(verbose_name="Temps consacré")
    total_distance = tables.Column(verbose_name="Distance parcourue")

    def __init__(self, queryset, year=None, **kwargs):
        super().__init__(self.annotate_queryset(queryset, year=year), **kwargs)

    def annotate_queryset(self, queryset, year=None):
        association_benevalo_category_filter = (
            Q(association_category__association__is_active=True)
            & Q(association_category__benevalo__is_active=True)
        )  # fmt: skip
        if year:
            association_benevalo_category_filter &= Q(
                association_category__benevalo__date__year=year
            )

        return queryset.annotate(
            count_associations=Count(
                "association_category",
                distinct=True,
                filter=association_benevalo_category_filter,
            ),
            count_benevalos=Count(
                "association_category__benevalo",
                distinct=True,
                filter=association_benevalo_category_filter,
            ),
            count_members=Count(
                "association_category__benevalo__user",
                distinct=True,
                filter=(
                    association_benevalo_category_filter
                    & Q(association_category__benevalo__user__isnull=False)
                ),
            ),
            total_duration=Sum(
                "association_category__benevalo__duration",
                filter=association_benevalo_category_filter,
            ),
            total_distance=Sum(
                "association_category__benevalo__distance",
                filter=association_benevalo_category_filter,
            ),
        ).order_by("name")

    def render_total_duration(self, value):
        return duration_format(value)

    def render_total_distance(self, value):
        return distance_format(value)
