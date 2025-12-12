from django import forms

from benevalibre.models import Benevalo

from . import NativeDateInput, SplitDurationField


class BenevaloForm(forms.ModelForm):
    class Meta:
        model = Benevalo
        fields = [
            "title",
            "date",
            "end_date",
            "duration",
            "distance",
            "category",
            "project",
            "level",
            "description",
        ]
        field_classes = {
            "duration": SplitDurationField,
        }
        error_messages = {
            "duration": {
                "required": "Le nombre d'heures et/ou de minutes est requis.",
            },
        }
        widgets = {
            "date": NativeDateInput(),
            "end_date": NativeDateInput(),
        }

    template_name = "forms/layouts/benevalo.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert self.instance.association

        self.fields["category"].queryset = (
            self.instance.association.benevalo_categories.all()
        )  # fmt: skip

        if self.instance.association.projects.exists():
            self.fields["project"].queryset = (
                self.instance.association.projects.all().order_by("name")
            )  # fmt: skip
        else:
            del self.fields["project"]

        if self.instance.association.benevalo_levels.exists():
            self.fields["level"].queryset = (
                self.instance.association.benevalo_levels.all().order_by("name")
            )  # fmt: skip
        else:
            del self.fields["level"]
