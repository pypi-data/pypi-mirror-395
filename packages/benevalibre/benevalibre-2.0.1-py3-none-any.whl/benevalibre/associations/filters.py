from django import forms

import django_filters

from benevalibre.associations.models import AssociationMembership
from benevalibre.filters.base import BaseFilterSet
from benevalibre.filters.benevalos import BaseBenevaloFilterSet


class AssociationMembershipFilterSet(BaseFilterSet):
    class Meta(BaseFilterSet.Meta):
        model = AssociationMembership
        fields = ["role", "is_active"]

    is_active = django_filters.BooleanFilter(
        label="Validé",
        widget=forms.Select(
            choices=[
                ("", "---------"),
                (True, "Oui"),
                (False, "Non"),
            ],
        ),
    )

    def __init__(self, *args, **kwargs):
        association = kwargs.pop("association")

        super().__init__(*args, **kwargs)

        self.filters["role"].queryset = association.roles.all().order_by("name")


class AssociationBenevaloFilterSet(BaseBenevaloFilterSet):
    class Meta(BaseBenevaloFilterSet.Meta):
        fields = ["user", "project", "is_active"]

    def __init__(self, *args, **kwargs):
        association = kwargs.pop("association")

        super().__init__(*args, **kwargs)

        self.filters["user"].queryset = (
            association.members.all().order_by_full_name()
        )  # fmt: skip

        if association.projects.exists():
            self.filters["project"].queryset = (
                association.projects.all().order_by("name")
            )  # fmt: skip
        else:
            del self.filters["project"]
