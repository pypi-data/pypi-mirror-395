from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property

from benevalibre.associations.models import Association
from benevalibre.views.mixins import ObjectPermissionRequiredMixin


class AssociationRelatedViewMixin:
    @cached_property
    def association(self):
        return self.get_association()

    def get_association(self):
        return get_object_or_404(
            self.get_association_queryset(),
            pk=self.kwargs["association"],
        )

    def get_association_queryset(self):
        return Association.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(association=self.association)

    # Surcharge les méthodes de récupération d'URL afin d'inclure l'argument
    # 'association' requis dans ces vues. Attention, les permissions ne sont
    # alors plus vérifiées à ce moment contrairement aux méthodes initiales.

    def get_index_url(self):
        if self.index_url_name:
            return reverse(
                self.index_url_name,
                kwargs={"association": self.association.id},
            )

    def get_create_url(self):
        if self.create_url_name:
            return reverse(
                self.create_url_name,
                kwargs={"association": self.association.id},
            )

    def get_update_url(self, instance=None):
        if self.update_url_name:
            if instance is None:
                instance = self.object
            return reverse(
                self.update_url_name,
                kwargs={"association": self.association.id, "pk": instance.pk},
            )

    def get_delete_url(self, instance=None):
        if self.delete_url_name:
            if instance is None:
                instance = self.object
            return reverse(
                self.delete_url_name,
                kwargs={"association": self.association.id, "pk": instance.pk},
            )


class AssociationRelatedManagementViewMixin(
    AssociationRelatedViewMixin,
    ObjectPermissionRequiredMixin,
):
    base_template_name = "associations/base_management.html"

    def get_permission_object(self):
        return self.association

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["association"] = self.association
        return context


class AssociationManagementViewMixin(ObjectPermissionRequiredMixin):
    base_template_name = "associations/base_management.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["association"] = self.object
        return context
