from django import forms

from benevalibre.models import InstanceSettings


class InstanceSettingsForm(forms.ModelForm):
    class Meta:
        model = InstanceSettings
        fields = ["site_name", "terms_of_use_file"]
        widgets = {
            "terms_of_use_file": forms.ClearableFileInput(
                attrs={"accept": ".pdf,application/pdf"},
            ),
        }
