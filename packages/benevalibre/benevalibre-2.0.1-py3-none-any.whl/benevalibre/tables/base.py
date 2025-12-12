import django_tables2 as tables

# On s'assure que les colonnes surchargées sont bien enregistrées
from . import columns  # noqa: F401


class BaseTable(tables.Table):
    def __init__(self, *args, **kwargs):
        self.filterset = kwargs.pop("filterset", None)
        super().__init__(*args, **kwargs)


class BaseExportTable(tables.Table):
    def __init__(self, *args, **kwargs):
        # Utilise une valeur nulle plutôt que "—"
        kwargs.setdefault("default", None)
        super().__init__(*args, **kwargs)
