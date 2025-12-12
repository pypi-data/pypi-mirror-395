from django import forms

import django_filters

from benevalibre.forms import NativeDateInput
from benevalibre.models import Benevalo

from .base import BaseFilterSet


class BaseBenevaloFilterSet(BaseFilterSet):
    is_active = django_filters.BooleanFilter(
        label="Validée",
        widget=forms.Select(
            choices=[
                ("", "---------"),
                (True, "Oui"),
                (False, "Non"),
            ],
        ),
    )
    date__gte = django_filters.DateFilter(
        field_name="date",
        lookup_expr="gte",
        label="À partir du",
        widget=NativeDateInput(),
    )
    date__lte = django_filters.DateFilter(
        field_name="date",
        lookup_expr="lte",
        label="Jusqu'au",
        widget=NativeDateInput(),
    )

    class Meta(BaseFilterSet.Meta):
        model = Benevalo
        fields = ["is_active"]


class UserBenevaloFilterSet(BaseBenevaloFilterSet):
    class Meta(BaseBenevaloFilterSet.Meta):
        fields = ["association", "is_active"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")

        super().__init__(*args, **kwargs)

        if user.is_anonymous_member:
            del self.filters["association"]
        else:
            associations = user.associations.active().with_active_member(user)

            if len(associations) > 1:
                self.filters["association"].queryset = associations.order_by(
                    "name"
                )
            else:
                del self.filters["association"]
