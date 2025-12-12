from benevalibre.associations.models import DefaultBenevaloLevel
from benevalibre.views import generic
from benevalibre.viewsets import ModelViewSet

from . import AdminViewMixin


class IndexView(AdminViewMixin, generic.IndexView):
    page_title = "Niveaux de bénévolat par défaut"
    seo_title = "Liste des niveaux de bénévolat par défaut"
    create_item_label = "Ajouter un niveau"

    default_ordering = "name"
    list_display = ("name", "description")


class CreateView(AdminViewMixin, generic.CreateView):
    page_title = "Nouveau niveau de bénévolat par défaut"
    success_message = "Niveau de bénévolat « %(object)s » créé."


class UpdateView(AdminViewMixin, generic.UpdateView):
    page_title = "Modification du niveau de bénévolat par défaut"
    success_message = "Niveau de bénévolat « %(object)s » mis à jour."


class DeleteView(AdminViewMixin, generic.DeleteView):
    page_title = "Suppression du niveau de bénévolat par défaut"
    success_message = "Niveau de bénévolat « %(object)s » supprimé."


class ViewSet(ModelViewSet):
    model = DefaultBenevaloLevel
    form_fields = ["name", "description"]
    views_classes = {
        "index": IndexView,
        "create": CreateView,
        "update": UpdateView,
        "delete": DeleteView,
    }
