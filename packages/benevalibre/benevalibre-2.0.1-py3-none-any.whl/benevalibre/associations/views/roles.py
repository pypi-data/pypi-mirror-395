from django.core.exceptions import PermissionDenied

from benevalibre.associations.forms import AssociationRoleForm
from benevalibre.associations.models import AssociationRole
from benevalibre.views import generic
from benevalibre.viewsets import ModelViewSet

from .mixins import AssociationRelatedManagementViewMixin


class ManagementViewMixin(AssociationRelatedManagementViewMixin):
    permission_required = "associations.manage_roles"


class IndexView(ManagementViewMixin, generic.IndexView):
    page_title = "Rôles"
    seo_title = "Liste des rôles de l'association"
    create_item_label = "Ajouter un rôle"

    default_ordering = ("-is_default", "name")
    list_display = ("name", "description", "is_default")


class CreateView(ManagementViewMixin, generic.CreateView):
    page_title = "Nouveau rôle"
    success_message = "Rôle « %(object)s » créé."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = AssociationRole(
            association=self.association,
        )
        return kwargs


class UpdateView(ManagementViewMixin, generic.UpdateView):
    page_title = "Modification du rôle"
    success_message = "Rôle « %(object)s » mis à jour."


class DeleteView(ManagementViewMixin, generic.DeleteView):
    page_title = "Suppression du rôle"
    success_message = "Rôle « %(object)s » supprimé."

    def has_permission(self):
        if not super().has_permission():
            return False
        default_roles_id = self.association.roles.default().values_list(
            "id", flat=True
        )
        if set(default_roles_id) == {self.kwargs.get(self.pk_url_kwarg)}:
            raise PermissionDenied(
                "Le rôle par défaut de l'association ne peut pas être supprimé."
            )
        return True


class ViewSet(ModelViewSet):
    model = AssociationRole
    form_class = AssociationRoleForm
    views_classes = {
        "index": IndexView,
        "create": CreateView,
        "update": UpdateView,
        "delete": DeleteView,
    }
