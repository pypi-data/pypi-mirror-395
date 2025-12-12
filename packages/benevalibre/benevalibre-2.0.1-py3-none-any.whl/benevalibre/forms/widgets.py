from django import forms

__all__ = (
    "NativeDateInput",
    "NativeDateTimeInput",
    "SplitDurationWidget",
    "TogglePasswordInput",
)


class NativeDateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, attrs=None):
        super().__init__(attrs=attrs, format="%Y-%m-%d")


class NativeDateTimeInput(forms.DateInput):
    input_type = "datetime-local"

    def __init__(self, attrs=None):
        super().__init__(attrs=attrs, format="%Y-%m-%dT%H:%M")


class SplitDurationWidget(forms.MultiWidget):
    template_name = "django/forms/widgets/split_duration.html"

    def __init__(self, attrs=None):
        widgets = {
            "hours": forms.NumberInput(
                attrs={"min": 0, "step": 1},
            ),
            "minutes": forms.NumberInput(
                attrs={"max": 59, "min": 0, "step": 1},
            ),
        }
        super().__init__(widgets, attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["subwidgets"][0] = self.get_subwidget_context(
            context["widget"]["subwidgets"][0], "h"
        )
        context["widget"]["subwidgets"][1] = self.get_subwidget_context(
            context["widget"]["subwidgets"][1], "min"
        )
        return context

    def get_subwidget_context(self, widget_context, label):
        unit_context = {
            "label": label,
            "id": "%s_unit" % widget_context["attrs"]["id"],
        }
        widget_context["attrs"]["aria-describedby"] = unit_context["id"]
        return (widget_context, unit_context)

    def decompress(self, value):
        if value:
            seconds = value.total_seconds()
            hours = int(seconds // 3600)
            seconds = seconds - hours * 3600
            minutes = int(seconds // 60)
            return [hours, minutes]
        return [None, None]


class TogglePasswordInput(forms.PasswordInput):
    template_name = "django/forms/widgets/toggle_password.html"
