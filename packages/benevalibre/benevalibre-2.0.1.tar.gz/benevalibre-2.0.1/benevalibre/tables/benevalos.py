import django_tables2 as tables

from benevalibre.models import Benevalo
from benevalibre.utils.formats import distance_format, duration_format

from .base import BaseExportTable, BaseTable


class BaseBenevaloTable(BaseTable):
    duration = tables.Column(verbose_name="Durée")
    distance = tables.Column(verbose_name="Distance")

    class Meta:
        model = Benevalo
        fields = [
            "title",
            "date",
            "duration",
            "distance",
            "is_active",
        ]

    def render_duration(self, value):
        return duration_format(value, empty_text=self.default)

    def render_distance(self, value):
        return distance_format(value, empty_text=self.default)

    def before_render(self, request):
        if "is_active" in self.filterset.active_filters:
            self.columns.hide("is_active")


class UserBenevaloTable(BaseBenevaloTable):
    class Meta(BaseBenevaloTable.Meta):
        fields = ["association"] + BaseBenevaloTable.Meta.fields


class BenevaloExportTable(BaseExportTable):
    duration_hours = tables.Column(
        accessor="duration",
        verbose_name="Durée (en heures)",
    )
    is_pending = tables.Column(
        accessor="is_active",
        verbose_name="En attente de modération",
    )

    class Meta:
        model = Benevalo
        fields = [
            "user__first_name",
            "user__last_name",
            "user__pseudo",
            "association",
            "title",
            "description",
            "date",
            "end_date",
            "duration",
            "duration_hours",
            "is_pending",
            "distance",
            "category",
            "project",
            "level",
        ]

    def render_duration_hours(self, value):
        return 24 * value.days + value.seconds / 3600

    def render_is_pending(self, value):
        return not bool(value)
