from django import forms
from django.utils.functional import cached_property

import django_filters


class BaseFilterSetForm(forms.Form):
    template_name = "forms/layouts/filters.html"


class BaseFilterSet(django_filters.FilterSet):
    class Meta:
        form = BaseFilterSetForm

    @cached_property
    def active_filters(self):
        filters = []

        for field_name in self.form.changed_data:
            bound_field = self.form[field_name]

            try:
                value = self.form.cleaned_data[field_name]
            except KeyError:
                continue

            if value == bound_field.initial:
                continue

            filters.append(field_name)

        return filters
