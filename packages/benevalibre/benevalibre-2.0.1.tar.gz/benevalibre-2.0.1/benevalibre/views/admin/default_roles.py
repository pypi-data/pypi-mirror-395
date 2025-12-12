from django.core.exceptions import PermissionDenied
from django.forms.models import modelform_factory

from benevalibre.associations.forms import BaseRoleForm
from benevalibre.associations.models import DefaultRole
from benevalibre.views import generic
from benevalibre.viewsets import ModelViewSet

from . import AdminViewMixin


class IndexView(AdminViewMixin, generic.IndexView):
    page_title = "Rôles par défaut"
    seo_title = "Liste des rôles par défaut"
    create_item_label = "Ajouter un rôle"

    default_ordering = ("-is_default", "name")
    list_display = ("name", "description", "is_default")


class CreateView(AdminViewMixin, generic.CreateView):
    page_title = "Nouveau rôle par défaut"
    success_message = "Rôle « %(object)s » créé."


class UpdateView(AdminViewMixin, generic.UpdateView):
    page_title = "Modification du rôle par défaut"
    success_message = "Rôle « %(object)s » mis à jour."


class DeleteView(AdminViewMixin, generic.DeleteView):
    page_title = "Suppression du rôle par défaut"
    success_message = "Rôle « %(object)s » supprimé."

    def test_func(self):
        if not super().test_func():
            return False
        default_roles_id = DefaultRole.objects.default().values_list(
            "id", flat=True
        )
        if set(default_roles_id) == {self.kwargs.get(self.pk_url_kwarg)}:
            raise PermissionDenied(
                "Le rôle par défaut ne peut pas être supprimé."
            )
        return True


class ViewSet(ModelViewSet):
    model = DefaultRole
    views_classes = {
        "index": IndexView,
        "create": CreateView,
        "update": UpdateView,
        "delete": DeleteView,
    }

    def get_form_class(self, for_update=False):
        return modelform_factory(self.model, form=BaseRoleForm)
