from django.utils.functional import cached_property

from benevalibre.associations.filters import AssociationBenevaloFilterSet
from benevalibre.associations.forms import AssociationBenevaloForm
from benevalibre.associations.tables import AssociationBenevaloTable
from benevalibre.models import Benevalo
from benevalibre.notifications import notify_user
from benevalibre.tables.benevalos import BenevaloExportTable
from benevalibre.views import generic
from benevalibre.viewsets import ModelViewSet

from .mixins import AssociationRelatedManagementViewMixin


class ManagementViewMixin(AssociationRelatedManagementViewMixin):
    permission_required = "associations.manage_benevalos"


class IndexView(ManagementViewMixin, generic.IndexView):
    page_title = "Actions de bénévolat"
    seo_title = "Liste des actions de bénévolat de l'association"
    create_item_label = "Ajouter une action"

    queryset = Benevalo.objects.select_related("user")
    default_ordering = ("is_active", "-date")
    table_class = AssociationBenevaloTable
    title_column_name = "title"
    filterset_class = AssociationBenevaloFilterSet
    export_table_class = BenevaloExportTable

    def get_filterset_kwargs(self):
        kwargs = super().get_filterset_kwargs()
        kwargs["association"] = self.association
        return kwargs


class CreateView(ManagementViewMixin, generic.CreateView):
    page_title = "Nouvelle action de bénévolat"
    success_message = "Action de bénévolat « %(object)s » créée."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = Benevalo(association=self.association)
        return kwargs


class UpdateView(ManagementViewMixin, generic.UpdateView):
    success_message = "Action de bénévolat « %(object)s » mise à jour."

    @cached_property
    def page_title(self):
        return (
            "Modification de l'action de bénévolat"
            if self.object.is_active
            else "Validation de l'action de bénévolat"
        )

    @cached_property
    def submit_button_label(self):
        if not self.object.is_active:
            return "Valider"
        return super().submit_button_label

    def save_object(self):
        if self.object.is_active:
            return super().save_object()

        self.form.instance.is_active = True
        instance = super().save_object()

        if instance.user is not None:
            notify_user(
                instance.user,
                "benevalo_approved",
                {
                    "benevalo": instance,
                    "association": instance.association,
                },
            )

        return instance


class DeleteView(ManagementViewMixin, generic.DeleteView):
    page_title = "Suppression de l'action de bénévolat"
    success_message = "Action de bénévolat « %(object)s » supprimée."


class ViewSet(ModelViewSet):
    model = Benevalo
    form_class = AssociationBenevaloForm
    views_classes = {
        "index": IndexView,
        "create": CreateView,
        "update": UpdateView,
        "delete": DeleteView,
    }
