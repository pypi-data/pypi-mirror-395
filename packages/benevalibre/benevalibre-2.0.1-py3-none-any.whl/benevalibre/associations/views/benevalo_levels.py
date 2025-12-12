from benevalibre.associations.forms import AssociationBenevaloLevelForm
from benevalibre.associations.models import AssociationBenevaloLevel
from benevalibre.views import generic
from benevalibre.viewsets import ModelViewSet

from .mixins import AssociationRelatedManagementViewMixin


class ManagementViewMixin(AssociationRelatedManagementViewMixin):
    permission_required = "associations.manage_benevalo_levels"


class IndexView(ManagementViewMixin, generic.IndexView):
    page_title = "Niveaux de bénévolat"
    seo_title = "Liste des niveaux de bénévolat de l'association"
    create_item_label = "Ajouter un niveau"

    default_ordering = "name"
    list_display = ("name", "description")


class CreateView(ManagementViewMixin, generic.CreateView):
    page_title = "Nouveau niveau de bénévolat"
    success_message = "Niveau de bénévolat « %(object)s » créé."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = AssociationBenevaloLevel(
            association=self.association,
        )
        return kwargs


class UpdateView(ManagementViewMixin, generic.UpdateView):
    page_title = "Modification du niveau de bénévolat"
    success_message = "Niveau de bénévolat « %(object)s » mis à jour."


class DeleteView(ManagementViewMixin, generic.DeleteView):
    page_title = "Suppression du niveau de bénévolat"
    success_message = "Niveau de bénévolat « %(object)s » supprimé."


class ViewSet(ModelViewSet):
    model = AssociationBenevaloLevel
    form_class = AssociationBenevaloLevelForm
    views_classes = {
        "index": IndexView,
        "create": CreateView,
        "update": UpdateView,
        "delete": DeleteView,
    }
