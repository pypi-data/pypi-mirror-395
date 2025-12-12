from django.db.models import Count, Q, Sum

import django_tables2 as tables

from benevalibre.associations.models import (
    AssociationAnonymousMember,
    AssociationMembership,
)
from benevalibre.tables.base import BaseTable
from benevalibre.tables.benevalos import BaseBenevaloTable
from benevalibre.tables.columns import UserColumn
from benevalibre.utils.formats import distance_format, duration_format


class AssociationMembershipTable(BaseTable):
    class Meta:
        model = AssociationMembership
        fields = ["user", "role", "is_active"]

    user = UserColumn()

    def before_render(self, request):
        if "is_active" in self.filterset.active_filters:
            self.columns.hide("is_active")


class AssociationAnonymousMemberTable(BaseTable):
    class Meta:
        model = AssociationAnonymousMember
        fields = [
            "title",
            "count_benevalos",
            "last_visit",
            "expiration_date",
            "is_active",
        ]

    title = tables.Column(empty_values=(), orderable=False, verbose_name="Nom")
    count_benevalos = tables.Column(verbose_name="Nombre de saisies")

    def render_title(self, record):
        return str(record)


class AssociationBenevaloTable(BaseBenevaloTable):
    author = UserColumn(verbose_name="Membre")

    class Meta(BaseBenevaloTable.Meta):
        fields = ["author"] + BaseBenevaloTable.Meta.fields


# STATISTICS
# ------------------------------------------------------------------------------


class BaseBenevaloReportTable(tables.Table):
    count_benevalos = tables.Column(verbose_name="Nombre de saisies")
    count_members = tables.Column(verbose_name="Membres concerné⋅es")
    total_duration = tables.Column(verbose_name="Temps consacré")
    total_distance = tables.Column(verbose_name="Distance parcourue")

    def __init__(self, queryset, year=None, **kwargs):
        super().__init__(self.annotate_queryset(queryset, year=year), **kwargs)

    def annotate_queryset(self, queryset, year=None):
        benevalo_filter = Q(benevalo__is_active=True)
        if year:
            benevalo_filter &= Q(benevalo__date__year=year)

        queryset = queryset.annotate(
            count_benevalos=Count(
                "benevalo",
                distinct=True,
                filter=benevalo_filter,
            ),
            count_members=Count(
                "benevalo__user",
                distinct=True,
                filter=benevalo_filter & Q(benevalo__user__isnull=False),
            ),
            total_distance=Sum(
                "benevalo__distance",
                filter=benevalo_filter,
            ),
            total_duration=Sum(
                "benevalo__duration",
                filter=benevalo_filter,
            ),
        )

        return queryset

    def render_total_duration(self, value):
        return duration_format(value)

    def render_total_distance(self, value):
        return distance_format(value)


class AssociationBenevaloCategoryReportTable(BaseBenevaloReportTable):
    class Meta:
        sequence = ("name", "...")

    name = tables.Column(verbose_name="Catégorie de bénévolat")


class AssociationBenevaloLevelReportTable(BaseBenevaloReportTable):
    class Meta:
        sequence = ("name", "...")

    name = tables.Column(verbose_name="Niveau de bénévolat")


class AssociationProjectReportTable(BaseBenevaloReportTable):
    class Meta:
        sequence = ("name", "...")

    name = tables.Column(verbose_name="Projet")
