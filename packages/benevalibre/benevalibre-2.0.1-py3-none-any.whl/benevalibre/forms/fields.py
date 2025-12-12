import datetime

from django import forms

from .widgets import SplitDurationWidget

__all__ = ("SplitDurationField",)


class SplitDurationField(forms.MultiValueField):
    """
    Un champ de formulaire qui sépare une durée en heures et minutes.

    Les minutes doivent être comprises entre 0 et 59, tandis que les heures
    n'ont pas de limite maximale. Lorsque ce champ est requis, il est possible
    de ne saisir que les heures ou les minutes.
    """

    widget = SplitDurationWidget

    def __init__(self, **kwargs):
        fields = (
            forms.IntegerField(
                min_value=0,
                step_size=1,
                required=False,
                error_messages={
                    "invalid": "Saisissez un nombre d'heures valide.",
                },
            ),
            forms.IntegerField(
                max_value=59,
                min_value=0,
                step_size=1,
                required=False,
                error_messages={
                    "invalid": "Saisissez un nombre de minutes valide.",
                },
            ),
        )
        super().__init__(fields, require_all_fields=False, **kwargs)

    def compress(self, data_list):
        if data_list:
            return datetime.timedelta(
                hours=data_list[0] or 0,
                minutes=data_list[1] or 0,
            )
        return None
