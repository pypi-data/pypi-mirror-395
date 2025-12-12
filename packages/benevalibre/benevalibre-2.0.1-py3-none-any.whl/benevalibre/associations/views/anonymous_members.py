from django.db.models import Count

from benevalibre.associations.forms import AssociationAnonymousMemberForm
from benevalibre.associations.models import AssociationAnonymousMember
from benevalibre.associations.tables import AssociationAnonymousMemberTable
from benevalibre.views import generic
from benevalibre.viewsets import ModelViewSet

from .mixins import AssociationRelatedManagementViewMixin


class ManagementViewMixin(AssociationRelatedManagementViewMixin):
    permission_required = "associations.manage_members"


class IndexView(ManagementViewMixin, generic.IndexView):
    page_title = "Membres anonymes"
    seo_title = "Liste des membres anonymes de l'association"
    create_item_label = "Ajouter un membre"

    default_ordering = ("-is_active", "-last_visit")
    table_class = AssociationAnonymousMemberTable
    title_column_name = "title"

    def get_base_queryset(self):
        return (
            super()
            .get_base_queryset()
            .annotate(
                count_benevalos=Count(
                    "benevalo",
                    distinct=True,
                ),
            )
        )


class CreateView(ManagementViewMixin, generic.CreateView):
    page_title = "Nouveau membre anonyme"
    success_message = "Membre anonyme créé."

    update_url_name = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = AssociationAnonymousMember(
            association=self.association,
        )
        return kwargs

    def get_success_url(self):
        return self.get_update_url()


class UpdateView(ManagementViewMixin, generic.UpdateView):
    page_title = "Modification du membre anonyme"
    success_message = "Membre anonyme mis à jour."
    template_name = "associations/anonymous_members/update.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                count_benevalos=Count(
                    "benevalo",
                    distinct=True,
                ),
            )
        )


class DeleteView(ManagementViewMixin, generic.DeleteView):
    page_title = "Suppression du membre anonyme"
    confirmation_message = (
        "Voulez-vous vraiment supprimer le membre anonyme « %(object)s » ? "
        "Cette action n'entraînera pas la suppression de ses actions de "
        "bénévolat."
    )
    success_message = "Membre anonyme supprimé."


class ViewSet(ModelViewSet):
    model = AssociationAnonymousMember
    form_class = AssociationAnonymousMemberForm
    views_classes = {
        "index": IndexView,
        "create": CreateView,
        "update": UpdateView,
        "delete": DeleteView,
    }
