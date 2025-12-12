from django.urls import reverse
from django.utils.functional import cached_property

from benevalibre.associations.filters import AssociationMembershipFilterSet
from benevalibre.associations.forms import AssociationMembershipForm
from benevalibre.associations.models import AssociationMembership
from benevalibre.associations.tables import AssociationMembershipTable
from benevalibre.notifications import notify_user
from benevalibre.views import generic
from benevalibre.viewsets import ModelViewSet

from .mixins import AssociationRelatedManagementViewMixin


class ManagementViewMixin(AssociationRelatedManagementViewMixin):
    permission_required = "associations.manage_benevalos"


class IndexView(ManagementViewMixin, generic.IndexView):
    queryset = AssociationMembership.objects.select_related("user", "role")
    page_title = "Membres"
    seo_title = "Liste des membres de l'association"

    default_ordering = ("is_active", "user")
    table_class = AssociationMembershipTable
    title_column_name = "user"
    filterset_class = AssociationMembershipFilterSet

    def get_filterset_kwargs(self):
        kwargs = super().get_filterset_kwargs()
        kwargs["association"] = self.association
        return kwargs


class UpdateView(ManagementViewMixin, generic.UpdateView):
    template_name = "associations/members/update.html"

    @cached_property
    def page_title(self):
        return (
            "Modification du membre"
            if self.object.is_active
            else "Validation du membre"
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

        notify_user(
            instance.user,
            "membership_approved",
            {
                "association": instance.association,
                "role": instance.role,
                "dashboard_url": self.request.build_absolute_uri(
                    reverse("dashboard")
                ),
            },
        )

        return instance

    def get_success_message(self):
        return "Membre « %s » mis à jour." % self.object.user


class DeleteView(ManagementViewMixin, generic.DeleteView):
    page_title = "Suppression du membre"

    def get_confirmation_message(self):
        return (
            "Voulez-vous vraiment supprimer de l'association le membre « %s » "
            "ayant comme rôle « %s » ? Cette action n'entraînera pas la "
            "suppression de ses actions de bénévolat."
        ) % (self.object.user, self.object.role)

    def get_success_message(self):
        return "Membre « %s » supprimé de l'association." % self.object.user


class ViewSet(ModelViewSet):
    model = AssociationMembership
    form_class = AssociationMembershipForm
    views_classes = {
        "index": IndexView,
        "update": UpdateView,
        "delete": DeleteView,
    }
    views_excluded = ["create"]
