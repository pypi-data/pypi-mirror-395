from django.db.models import Count, Sum
from django.utils import timezone
from django.views.generic.base import TemplateView

from benevalibre.menus import BoundMenuItem
from benevalibre.models import Benevalo
from benevalibre.utils.formats import distance_format, duration_format

from .mixins import PageContextMixin


class BaseStatisticsView(PageContextMixin, TemplateView):
    year_kwarg = "year"

    def get(self, request, *args, **kwargs):
        self.current_year = None
        self.available_years = []
        self.first_benevalo_date = self.get_first_benevalo_date()
        self.has_benevalos = self.first_benevalo_date is not None

        if self.has_benevalos:
            self.available_years = list(
                range(self.first_benevalo_date.year, timezone.now().year + 1)
            )
            if year := self.request.GET.get(self.year_kwarg, None):
                if int(year) in self.available_years:
                    self.current_year = int(year)

        return super().get(request, *args, **kwargs)

    def get_benevalo_queryset(self):
        """
        Retourne l'objet QuerySet pour le modèle Benevalo à utiliser dans les
        méthodes de cette vue.
        """
        return Benevalo.objects.active()

    def get_first_benevalo_date(self):
        try:
            return self.get_benevalo_queryset().order_by("date")[0].date
        except IndexError:
            return None

    def get_benevalos_stats(self):
        queryset = self.get_benevalo_queryset()

        if self.current_year:
            queryset = queryset.filter(date__year=self.current_year)

        values = queryset.aggregate(
            count=Count("*"),
            duration=Sum("duration"),
            distance=Sum("distance"),
        )

        return {
            "count": values["count"],
            "total_duration": duration_format(values["duration"]),
            "total_distance": distance_format(values["distance"]),
        }

    def get_report_table(self, table_class, queryset, ordering_kwarg):
        return table_class(
            queryset,
            year=self.current_year,
            order_by=self.request.GET.get(ordering_kwarg, "name"),
            order_by_field=ordering_kwarg,
        )

    def get_year_menu_item(self, year, label):
        params = self.request.GET.copy()

        if year:
            params[self.year_kwarg] = year
        elif self.year_kwarg in params:
            del params[self.year_kwarg]

        return BoundMenuItem(
            label=label,
            url="?%s" % params.urlencode() if params else ".",
            is_active=self.current_year == year,
        )

    def get_year_menu_items(self):
        menu_items = [
            self.get_year_menu_item(None, "Total"),
        ]
        for year in reversed(self.available_years):
            menu_items.append(self.get_year_menu_item(year, "En %d" % year))
        return menu_items

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["has_benevalos"] = self.has_benevalos
        if self.has_benevalos:
            context["benevalos_stats"] = self.get_benevalos_stats()
            context["year_menu_items"] = self.get_year_menu_items()
            context["current_year"] = self.current_year
        return context
