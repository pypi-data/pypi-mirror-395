from django import forms
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import BadRequest, PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe

from benevalibre.associations.models import Association
from benevalibre.filters.benevalos import UserBenevaloFilterSet
from benevalibre.forms.benevalos import BenevaloForm
from benevalibre.models import Benevalo
from benevalibre.tables.benevalos import BenevaloExportTable, UserBenevaloTable
from benevalibre.views import generic
from benevalibre.views.mixins import ObjectPermissionRequiredMixin
from benevalibre.viewsets import ModelViewSet


class AssociationSelectForm(forms.Form):
    association = forms.ModelChoiceField(queryset=None)

    def __init__(self, associations, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["association"].queryset = associations.order_by("name")


class IndexView(AccessMixin, generic.IndexView):
    full_width = False
    page_title = "Mes actions de bénévolat"
    seo_title = "Liste de mes actions de bénévolat"
    create_item_label = "Ajouter une action"

    default_ordering = ("is_active", "-date")
    table_class = UserBenevaloTable
    title_column_name = "title"
    filterset_class = UserBenevaloFilterSet
    export_table_class = BenevaloExportTable

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_active:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_base_queryset(self):
        queryset = Benevalo.objects.all()
        if self.request.user.is_anonymous_member:
            queryset = queryset.filter(anonymous_member=self.request.user)
        else:
            queryset = queryset.filter(user=self.request.user)
        return queryset.select_related("association")

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        if (
            self.request.user.is_anonymous_member
            or self.request.user.associations.count() < 2
        ):
            kwargs["exclude"] = ["association"]
        return kwargs

    def get_filterset_kwargs(self):
        kwargs = super().get_filterset_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_create_url(self):
        if self.request.user.has_perm("benevalibre.add_benevalo"):
            return super().get_create_url()


class CreateView(AccessMixin, generic.CreateView):
    page_title = "Nouvelle action de bénévolat"
    template_name = "user_benevalos/create.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_active:
            return self.handle_no_permission()

        if request.user.is_anonymous_member:
            # Un membre anonyme ne fait parti que d'une association
            self.association = request.user.association
        elif association_id := request.GET.get("association"):
            # L'association pour laquelle créer l'action est spécifiée
            self.association = get_object_or_404(
                Association.objects.active(),
                pk=int(association_id),
            )
        else:
            # Récupère les associations actives du membre et retourne un
            # formulaire de sélection s'il y en a plusieurs
            associations = (
                Association.objects.active()
                .with_active_member(request.user)
                .without_migration()
            )
            if len(associations) > 1:
                if request.method != "GET":
                    raise BadRequest(
                        "L'association pour laquelle ajouter une action de "
                        "bénévolat est manquante."
                    )

                self.object = None
                self.association = None

                return self.render_to_response(
                    self.get_context_data(
                        is_select_form=True,
                        form=AssociationSelectForm(
                            associations=associations.order_by("name"),
                        ),
                    )
                )
            elif len(associations) == 0:
                raise PermissionDenied(
                    "Vous devez être membre d'une association pour ajouter "
                    "une action de bénévolat."
                )

            # La personne n'est membre que d'une association, on la positionne
            self.association = associations[0]

        if not request.user.has_perm(
            "benevalibre.add_benevalo", self.association
        ):
            raise PermissionDenied(
                mark_safe(
                    "Vous n'avez pas les permissions requises pour saisir une "
                    'action de bénévolat pour l\'association <a href="%s">%s'
                    "</a>, assurez-vous d'en être membre."
                    % (
                        reverse(
                            "associations:detail",
                            args=(self.association.pk,),
                        ),
                        self.association.name,
                    )
                )
            )
        return super().dispatch(request, *args, **kwargs)

    def get_create_url(self):
        create_url = super().get_create_url()
        if self.association is None:
            return create_url
        return "%s?association=%d" % (create_url, self.association.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def get_object(self):
        obj = Benevalo(
            association=self.association,
            is_active=not self.association.moderate_benevalo,
        )
        if self.request.user.is_anonymous_member:
            obj.anonymous_member = self.request.user
        else:
            obj.user = self.request.user
        return obj

    def get_success_message(self):
        return (
            (
                "Votre action de bénévolat « %(object)s » a été créée mais "
                "elle doit être validée par un⋅e responsable de l'association. "
                "Vous serez notifié⋅e une fois votre saisie traitée."
            )
            if not self.object.is_active
            else "Action de bénévolat « %(object)s » créée."
        ) % {"object": self.object}


class UpdateView(ObjectPermissionRequiredMixin, generic.UpdateView):
    permission_required = "benevalibre.change_benevalo"
    page_title = "Modification de l'action de bénévolat"
    success_message = "Action de bénévolat « %(object)s » mise à jour."
    template_name = "user_benevalos/update.html"

    def get_queryset(self):
        return super().get_queryset().select_related("association")


class DeleteView(ObjectPermissionRequiredMixin, generic.DeleteView):
    permission_required = "benevalibre.delete_benevalo"
    page_title = "Suppression de l'action de bénévolat"
    success_message = "Action de bénévolat « %(object)s » supprimée."

    def get_queryset(self):
        return super().get_queryset().select_related("association")

    def get_confirmation_message(self):
        return (
            "Voulez-vous vraiment supprimer votre action de bénévolat "
            "« %s » pour l'association « %s » ?"
            % (self.object, self.object.association)
        )


class ViewSet(ModelViewSet):
    model = Benevalo
    form_class = BenevaloForm
    views_classes = {
        "index": IndexView,
        "create": CreateView,
        "update": UpdateView,
        "delete": DeleteView,
    }
