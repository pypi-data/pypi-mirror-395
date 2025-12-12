from django import forms
from django.forms.renderers import TemplatesSetting

from .fields import *  # noqa: F403
from .widgets import *  # noqa: F403


class BoundField(forms.BoundField):
    def label_tag(self, tag=None):
        context = {
            "field": self,
            "label": self.label,
            "tag": tag or "label",
            "id_for_label": self.id_for_label,
        }
        return self.form.render("forms/label.html", context)

    def legend_tag(self):
        return self.label_tag("legend")

    @property
    def is_checkbox(self):
        return self.field.widget.__class__ == forms.CheckboxInput

    @property
    def is_required(self):
        return self.field.required


class FormRenderer(TemplatesSetting):
    form_template_name = "forms/layouts/default.html"
    field_template_name = "forms/field.html"
    bound_field_class = BoundField
