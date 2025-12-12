from benevalibre.associations.forms import AssociationBenevaloCategoryForm
from benevalibre.associations.models import AssociationBenevaloCategory
from benevalibre.views import generic
from benevalibre.viewsets import ModelViewSet

from .mixins import AssociationRelatedManagementViewMixin


class ManagementViewMixin(AssociationRelatedManagementViewMixin):
    permission_required = "associations.manage_benevalo_categories"


class IndexView(ManagementViewMixin, generic.IndexView):
    page_title = "Catégories de bénévolat"
    seo_title = "Liste des catégories de bénévolat de l'association"
    create_item_label = "Ajouter une catégorie"

    list_display = ("name",)


class CreateView(ManagementViewMixin, generic.CreateView):
    page_title = "Nouvelle catégorie de bénévolat"
    success_message = "Catégorie de bénévolat « %(object)s » créée."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = AssociationBenevaloCategory(
            association=self.association,
        )
        return kwargs


class UpdateView(ManagementViewMixin, generic.UpdateView):
    page_title = "Modification de la catégorie de bénévolat"
    success_message = "Catégorie de bénévolat « %(object)s » mise à jour."


class DeleteView(ManagementViewMixin, generic.DeleteView):
    page_title = "Suppression de la catégorie de bénévolat"
    success_message = "Catégorie de bénévolat « %(object)s » supprimée."


class ViewSet(ModelViewSet):
    model = AssociationBenevaloCategory
    form_class = AssociationBenevaloCategoryForm
    views_classes = {
        "index": IndexView,
        "create": CreateView,
        "update": UpdateView,
        "delete": DeleteView,
    }
