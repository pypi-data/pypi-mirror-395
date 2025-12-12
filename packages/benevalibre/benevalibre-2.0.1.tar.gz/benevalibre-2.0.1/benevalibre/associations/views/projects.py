from benevalibre.associations.forms import AssociationProjectForm
from benevalibre.associations.models import AssociationProject
from benevalibre.views import generic
from benevalibre.viewsets import ModelViewSet

from .mixins import AssociationRelatedManagementViewMixin


class ManagementViewMixin(AssociationRelatedManagementViewMixin):
    permission_required = "associations.manage_projects"


class IndexView(ManagementViewMixin, generic.IndexView):
    page_title = "Projets"
    seo_title = "Liste des projets de l'association"
    create_item_label = "Ajouter un projet"

    default_ordering = "name"
    list_display = ("name", "description")


class CreateView(ManagementViewMixin, generic.CreateView):
    page_title = "Nouveau projet"
    success_message = "Projet « %(object)s » créé."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = AssociationProject(
            association=self.association,
        )
        return kwargs


class UpdateView(ManagementViewMixin, generic.UpdateView):
    page_title = "Modification du projet"
    success_message = "Projet « %(object)s » mis à jour."


class DeleteView(ManagementViewMixin, generic.DeleteView):
    page_title = "Suppression du projet"
    success_message = "Projet « %(object)s » supprimé."


class ViewSet(ModelViewSet):
    model = AssociationProject
    form_class = AssociationProjectForm
    views_classes = {
        "index": IndexView,
        "create": CreateView,
        "update": UpdateView,
        "delete": DeleteView,
    }
