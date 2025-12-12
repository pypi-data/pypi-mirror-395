from benevalibre.associations.models import DefaultBenevaloCategory
from benevalibre.views import generic
from benevalibre.viewsets import ModelViewSet

from . import AdminViewMixin


class IndexView(AdminViewMixin, generic.IndexView):
    page_title = "Catégories de bénévolat par défaut"
    seo_title = "Liste des catégories de bénévolat par défaut"
    create_item_label = "Ajouter une catégorie"

    list_display = ("name",)


class CreateView(AdminViewMixin, generic.CreateView):
    page_title = "Nouvelle catégorie de bénévolat par défaut"
    success_message = "Catégorie de bénévolat « %(object)s » créée."


class UpdateView(AdminViewMixin, generic.UpdateView):
    page_title = "Modification de la catégorie de bénévolat par défaut"
    success_message = "Catégorie de bénévolat « %(object)s » mise à jour."


class DeleteView(AdminViewMixin, generic.DeleteView):
    page_title = "Suppression de la catégorie de bénévolat par défaut"
    success_message = "Catégorie de bénévolat « %(object)s » supprimée."


class ViewSet(ModelViewSet):
    model = DefaultBenevaloCategory
    form_fields = ["name", "description"]
    views_classes = {
        "index": IndexView,
        "create": CreateView,
        "update": UpdateView,
        "delete": DeleteView,
    }
