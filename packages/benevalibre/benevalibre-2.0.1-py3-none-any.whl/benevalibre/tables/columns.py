from django.db import models
from django.template.loader import get_template
from django.utils import timezone
from django.utils.formats import date_format, get_format_lazy

import django_tables2 as tables
from django_tables2.columns.base import library


@library.register
class BooleanColumn(tables.BooleanColumn):
    template_name = "django_tables2/columns/boolean_column.html"

    def render(self, value, record, bound_column):
        value = self._get_bool_value(record, value, bound_column)
        return get_template(self.template_name).render({"value": value})


@library.register
class DateColumn(tables.Column):
    default_format = get_format_lazy("SHORT_DATE_FORMAT")

    def __init__(self, format=None, *args, **kwargs):
        self.format = format or self.default_format
        super().__init__(*args, **kwargs)

    def render(self, value):
        return date_format(self.value(value), format=self.format)

    def value(self, value):
        return value

    @classmethod
    def from_field(cls, field, **kwargs):
        if isinstance(field, models.DateField):
            return cls(**kwargs)


@library.register
class DateTimeColumn(DateColumn):
    default_format = get_format_lazy("SHORT_DATETIME_FORMAT")

    def value(self, value):
        return timezone.localtime(value)

    @classmethod
    def from_field(cls, field, **kwargs):
        if isinstance(field, models.DateTimeField):
            return cls(**kwargs)


class ActionsColumn(tables.Column):
    attrs = {
        "th": {"width": 1},
    }
    empty_values = ()
    template_name = "django_tables2/columns/actions_column.html"

    def __init__(self, menu_items=[]):
        super().__init__(
            orderable=False,
            verbose_name="",
            exclude_from_export=True,
        )
        self.menu_items = menu_items

    def render(self, record, table, value, bound_column, **kwargs):
        if menu_items := self.get_menu_items(record):
            return get_template(self.template_name).render(
                {
                    "record": record,
                    "menu_items": menu_items,
                }
            )
        return ""

    def get_menu_items(self, record):
        return self.menu_items


class UserColumn(tables.Column):
    template_name = "django_tables2/columns/user_column.html"

    def order(self, queryset, is_descending):
        return (queryset.order_by_user_full_name(is_descending), True)

    def render(self, record, value):
        return get_template(self.template_name).render({"user": value})
