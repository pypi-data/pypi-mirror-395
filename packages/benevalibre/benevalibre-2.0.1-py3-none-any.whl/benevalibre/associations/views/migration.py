from django.conf import settings
from django.contrib import messages
from django.core.exceptions import BadRequest
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.http import content_disposition_header
from django.views.generic import FormView

from benevalibre.accounts.views.registration import send_activation_mail
from benevalibre.associations.forms import (
    AssociationImportForm,
    AssociationMigrateForm,
)
from benevalibre.associations.migration import (
    MigrationImportError,
    export_association_data,
    import_association_data,
)
from benevalibre.associations.models import AssociationMigration
from benevalibre.notifications import notify_users
from benevalibre.views.mixins import (
    ObjectMixin,
    PageContextMixin,
    PermissionRequiredMixin,
)

from .mixins import AssociationManagementViewMixin


class AssociationImportView(
    PermissionRequiredMixin,
    PageContextMixin,
    FormView,
):
    permission_required = "associations.add_association"
    form_class = AssociationImportForm
    page_title = "Importer une association"
    template_name = "associations/migration/import.html"

    creation_closed_url_name = None
    detail_url_name = None
    import_url_name = None

    @cached_property
    def creation_closed_url(self):
        return reverse(self.creation_closed_url_name)

    @cached_property
    def import_url(self):
        return reverse(self.import_url_name)

    def dispatch(self, request, *args, **kwargs):
        if not getattr(settings, "ASSOCIATION_REGISTRATION_OPEN", True):
            return HttpResponseRedirect(self.creation_closed_url)
        return super().dispatch(request, *args, **kwargs)

    def get_detail_url(self, obj):
        return reverse(self.detail_url_name, args=(obj.pk,))

    def get_success_url(self):
        return self.get_detail_url(self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = self.import_url
        return context

    def form_valid(self, form):
        data = form.cleaned_data["data"]

        try:
            with transaction.atomic():
                self.object, new_users = import_association_data(data)
        except MigrationImportError as e:
            form.add_error(None, str(e))
        except ValueError as e:
            form.add_error("file", str(e))
        else:
            if settings.ASSOCIATION_REGISTRATION_MODERATED:
                self.object.is_active = False
                self.object.save(update_fields=["is_active"])
            self.notify_users(new_users)
            return super().form_valid(form)

        return self.form_invalid(form)

    def notify_users(self, new_users):
        extra_context = {
            "association": self.object,
            "dashboard_url": self.request.build_absolute_uri(
                reverse("dashboard")
            ),
        }

        for user in new_users:
            send_activation_mail(
                user,
                request=self.request,
                extra_context=extra_context,
                email_template_name=(
                    "associations/migration/user_activation_email.txt"
                ),
                subject_template_name=(
                    "associations/migration/user_activation_email_subject.txt"
                ),
            )

        notify_users(
            self.object.members.exclude(pk__in=[u.pk for u in new_users]),
            "association_migrated",
            extra_context,
        )


class AssociationMigrateView(
    AssociationManagementViewMixin,
    PageContextMixin,
    ObjectMixin,
    FormView,
):
    permission_required = "associations.migrate_association"
    form_class = AssociationMigrateForm
    page_title = "Migration de l'association"
    template_name = "associations/migration/migrate.html"

    migrate_url_name = None
    update_url_name = None
    delete_url_name = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.migration = getattr(self.object, "migration", None)

    def post(self, request, *args, **kwargs):
        if action := request.POST.get("action", None):
            if action in {"download", "cancel"}:
                if not self.migration:
                    raise BadRequest(
                        "L'association « %s » n'est pas en cours de migration."
                        % self.object
                    )
                if self.migration.is_done:
                    raise BadRequest(
                        "La migration de l'association « %s » est terminée."
                        % self.object
                    )
                if action == "download":
                    return self.download_to_response()
                return self.cancel_to_response()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.migration or AssociationMigration(
            association=self.object,
            author=self.request.user,
        )
        return kwargs

    def get_migrate_url(self):
        return reverse(self.migrate_url_name, args=(self.object.pk,))

    def get_update_url(self):
        return reverse(self.update_url_name, args=(self.object.pk,))

    def get_delete_url(self):
        return reverse(self.delete_url_name, args=(self.object.pk,))

    def get_success_url(self):
        return self.get_migrate_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = self.get_migrate_url()
        context["delete_url"] = self.get_delete_url()
        context["migration"] = self.migration
        return context

    def download_to_response(self):
        return JsonResponse(
            export_association_data(self.migration),
            headers={
                "Content-Disposition": content_disposition_header(
                    as_attachment=True,
                    filename="association-%d_data.json" % self.object.pk,
                ),
            },
        )

    def cancel_to_response(self):
        self.migration.delete()

        messages.success(
            self.request,
            "La migration de l'association « %s » a été annulée." % self.object,
        )

        return HttpResponseRedirect(self.get_update_url())

    def form_valid(self, form):
        is_new = self.migration is None

        if is_new:
            form.instance.author = self.request.user

        self.migration = form.save()

        if not is_new:
            messages.success(
                self.request,
                "Message de migration de l'association « %s » mis à jour."
                % self.object,
            )

        return super().form_valid(form)
