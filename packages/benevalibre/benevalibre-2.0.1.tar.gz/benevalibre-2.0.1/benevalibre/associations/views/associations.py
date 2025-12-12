from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.core.exceptions import BadRequest, ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView, TemplateView, View

from benevalibre.associations.forms import AssociationForm
from benevalibre.associations.menus import association_management_menu
from benevalibre.associations.models import Association
from benevalibre.notifications import notify_users
from benevalibre.paginator import Paginator
from benevalibre.views import generic
from benevalibre.views.mixins import (
    ObjectMixin,
    ObjectPermissionRequiredMixin,
    PageContextMixin,
    PermissionRequiredMixin,
)
from benevalibre.viewsets import ModelViewSet

from .migration import AssociationImportView, AssociationMigrateView
from .mixins import AssociationManagementViewMixin


class AssociationSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Rechercher une association…",
            },
        ),
    )

    FIELD_NAME = "query"


class AssociationListView(PageContextMixin, TemplateView):
    page_title = "Associations"
    seo_title = "Liste des associations"
    template_name = "associations/list.html"

    page_kwarg = "page"
    paginate_by = 20

    create_url_name = None
    import_url_name = None
    search_url_name = None

    @cached_property
    def create_url(self):
        return reverse(self.create_url_name)

    @cached_property
    def import_url(self):
        return reverse(self.import_url_name)

    @cached_property
    def search_url(self):
        return reverse(self.search_url_name)

    def get_search_form(self):
        return AssociationSearchForm()

    @cached_property
    def search_form(self):
        return self.get_search_form()

    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get(self.page_kwarg)
        page = paginator.get_page(page_number)
        return (paginator, page, page.object_list, page.has_other_pages())

    def get_base_queryset(self):
        if self.request.user.is_superuser:
            return Association.objects.all()

        queryset = Association.objects.active()

        if not self.request.user.is_authenticated:
            return queryset.filter(is_hidden=False)

        return queryset.filter(
            Q(is_hidden=False) | Q(is_hidden=True, members=self.request.user)
        ).distinct()

    def get_queryset(self):
        return self.get_base_queryset().order_by(Lower("name").asc())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search_form"] = self.search_form
        context["search_url"] = self.search_url

        queryset = self.get_queryset()

        if self.paginate_by:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset, self.paginate_by
            )
            context.update(
                {
                    "object_list": queryset,
                    "paginator": paginator,
                    "page_obj": page,
                    "is_paginated": is_paginated,
                }
            )
        else:
            context.update(
                {
                    "object_list": queryset,
                    "paginator": None,
                    "page_obj": None,
                    "is_paginated": False,
                }
            )

        if self.request.user.has_perm("associations.add_association"):
            context["create_url"] = self.create_url
            context["import_url"] = self.import_url

        return context


class AssociationSearchView(AssociationListView):
    page_title = "Résultats de la recherche"
    seo_title = "Recherche d'une association"
    template_name = "associations/search.html"

    search_kwarg = AssociationSearchForm.FIELD_NAME

    def get_search_form(self):
        if self.search_kwarg in self.request.GET:
            return AssociationSearchForm(self.request.GET)
        return AssociationSearchForm()

    @cached_property
    def search_query(self):
        if self.search_form.is_valid():
            return self.search_form.cleaned_data[self.search_kwarg]
        return ""

    def get_base_queryset(self):
        if not self.search_query:
            return Association.objects.none()
        return (
            super()
            .get_base_queryset()
            .filter(name__icontains=self.search_query)
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search_query"] = self.search_query
        return context


class AssociationIndexView(AssociationListView):
    page_title = "Associations"
    seo_title = "Associations"
    template_name = "associations/index.html"

    paginate_by = None

    list_url_name = None

    @cached_property
    def list_url(self):
        return reverse(self.list_url_name)

    def get_queryset(self):
        return (
            Association.objects.active()
            .filter(is_hidden=False)
            .order_by("?")[:8]
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["list_url"] = self.list_url
        return context


class AssociationDetailView(
    ObjectPermissionRequiredMixin,
    PageContextMixin,
    ObjectMixin,
    TemplateView,
):
    permission_required = "associations.view_association"
    template_name = "associations/detail.html"

    join_url_name = None
    leave_url_name = None

    @cached_property
    def page_title(self):
        return self.object.name

    def get_join_url(self):
        if not self.object.has_migration:
            return reverse(self.join_url_name, args=(self.object.pk,))

    def get_leave_url(self):
        if not self.object.has_migration:
            return reverse(self.leave_url_name, args=(self.object.pk,))

    def get_manage_url(self):
        # On retourne le premier élément du menu de gestion de l'association
        # à défaut d'avoir une page d'accueil pour sa gestion.
        for menu_item in association_management_menu.get_items_for_request(
            self.request, self.object
        ):
            return menu_item.url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            try:
                membership = self.object.memberships.get(user=self.request.user)
            except ObjectDoesNotExist:
                if self.request.user.is_superuser:
                    context["manage_url"] = self.get_manage_url()
                context["join_url"] = self.get_join_url()
            else:
                context["is_member"] = True
                context["membership"] = membership
                context["leave_url"] = self.get_leave_url()
                context["manage_url"] = self.get_manage_url()

                if self.request.user.has_perm(
                    "associations.list_members", self.object
                ):
                    context["memberships"] = (
                        self.object.memberships.active()
                        .select_related("user", "role")
                        .order_by_user_full_name()
                    )
        elif self.request.user.is_anonymous_member and self.object.has_member(
            self.request.user
        ):
            context["is_member"] = True

        if self.object.has_migration:
            context["migration"] = self.object.migration

        return context


class AssociationCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = "associations.add_association"
    page_title = "Nouvelle association"
    template_name = "associations/create.html"

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
        if not settings.ASSOCIATION_REGISTRATION_MODERATED:
            return self.get_detail_url(self.object)
        return reverse("dashboard")

    def get_success_message(self):
        return (
            (
                "L'association « %(object)s » a été créée mais demande d'être "
                "validée par un⋅e administrateur⋅rice de l'instance. Vous "
                "serez notifié⋅e une fois votre demande traitée."
            )
            if settings.ASSOCIATION_REGISTRATION_MODERATED
            else "Association « %(object)s » créée."
        ) % {"object": self.object}

    def save_object(self):
        if settings.ASSOCIATION_REGISTRATION_MODERATED:
            self.form.instance.is_active = False

        association = super().save_object()

        # Attribut le premier rôle permettant de gérer l'association au membre
        role = association.roles.filter(manage_association=True).first()
        association.memberships.create(user=self.request.user, role=role)

        return association

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["index_url"] = self.get_index_url()
        context["import_url"] = self.import_url
        return context


class AssociationCreationClosedView(
    PermissionRequiredMixin,
    PageContextMixin,
    TemplateView,
):
    permission_required = "associations.add_association"
    page_title = "Nouvelle association"
    seo_title = "Nouvelle association indisponible"
    template_name = "associations/creation_closed.html"

    create_url_name = None

    @cached_property
    def create_url(self):
        return reverse(self.create_url_name)

    def dispatch(self, request, *args, **kwargs):
        if getattr(settings, "ASSOCIATION_REGISTRATION_OPEN", True):
            return HttpResponseRedirect(self.create_url)
        return super().dispatch(request, *args, **kwargs)


class AssociationUpdateView(AssociationManagementViewMixin, generic.UpdateView):
    permission_required = "associations.change_association"
    success_message = "Association « %(object)s » mise à jour."
    template_name = "associations/update.html"

    detail_url_name = None
    migrate_url_name = None

    @cached_property
    def page_title(self):
        return (
            "Modification de l'association"
            if self.object.is_active
            else "Validation de l'association"
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

        notify_users(
            instance.members.filter(
                membership__is_active=True,
                membership__association=instance.pk,
                membership__role__manage_association=True,
            ),
            "association_approved",
            {
                "association": instance,
                "detail_url": self.request.build_absolute_uri(
                    reverse(self.detail_url_name, args=(instance.pk,))
                ),
            },
        )

        return instance

    def get_migrate_url(self):
        return reverse(self.migrate_url_name, args=(self.object.pk,))

    def get_success_url(self):
        return self.get_update_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["migrate_url"] = self.get_migrate_url()
        return context


class AssociationDeleteView(AssociationManagementViewMixin, generic.DeleteView):
    permission_required = "associations.delete_association"
    page_title = "Suppression de l'association"
    confirmation_message = (
        "Voulez-vous vraiment supprimer l'association « %(object)s » ainsi que "
        "toutes ses données associées ?"
    )
    success_message = "Association « %(object)s » supprimée."

    update_url_name = None

    def get_cancel_url(self):
        return reverse(self.update_url_name, args=(self.object.pk,))


class AssociationJoinView(LoginRequiredMixin, ObjectMixin, View):
    http_method_names = ["post", "options"]
    success_url = reverse_lazy("dashboard")

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.object.is_active:
            raise BadRequest(
                "L'association « %s » n'a pas encore été validée." % self.object
            )
        if self.object.has_migration:
            raise BadRequest(
                "L'association « %s » est en cours de migration ou a été "
                "migrée vers une autre instance." % self.object
            )
        if self.object.memberships.filter(user=request.user).exists():
            raise BadRequest(
                "Vous êtes déjà membre de l'association « %s » ou votre "
                "demande n'a pas encore été validée." % self.object
            )

        with transaction.atomic():
            self.membership = self.object.memberships.create(
                user=self.request.user,
                role=self.object.roles.default().get(),
                is_active=not self.object.moderate_membership,
            )

        messages.success(self.request, self.get_success_message())

        return HttpResponseRedirect(str(self.success_url))

    def get_success_message(self):
        return (
            (
                "Votre demande de rejoindre « %(object)s » a été prise en "
                "compte mais elle doit être validée par un⋅e responsable de "
                "l'association. Vous serez notifié⋅e une fois votre demande "
                "traitée."
            )
            if not self.membership.is_active
            else "Vous êtes désormais membre de l'association « %(object)s »."
        ) % {"object": self.object}


class AssociationLeaveView(
    AccessMixin,
    PageContextMixin,
    ObjectMixin,
    FormView,
):
    form_class = forms.Form
    success_url = reverse_lazy("dashboard")
    page_title = "Départ de l'association"
    template_name = "associations/confirm_leave.html"

    detail_url_name = None
    leave_url_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.object.is_active:
            raise BadRequest(
                "L'association « %s » n'a pas encore été validée." % self.object
            )
        if self.object.has_migration:
            raise BadRequest(
                "L'association « %s » est en cours de migration ou a été "
                "migrée vers une autre instance." % self.object
            )
        if not self.object.memberships.filter(user=request.user).exists():
            raise BadRequest(
                "Vous n'êtes pas membre de l'association « %s »." % self.object
            )
        return super().dispatch(request, *args, **kwargs)

    def get_detail_url(self):
        return reverse(self.detail_url_name, args=(self.object.pk,))

    def get_leave_url(self):
        return reverse(self.leave_url_name, args=(self.object.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = self.get_leave_url()
        context["detail_url"] = self.get_detail_url()
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.request.user.memberships.get(
                    association=self.object,
                ).delete()
        except IntegrityError:
            return self.render_to_response(
                self.get_context_data(
                    error_message=(
                        "Vous êtes actuellement le seul membre à avoir la "
                        "permission de gérer l'association « %s ». Veuillez "
                        "d'abord attribuer un rôle avec cette permission à un "
                        "autre membre pour vous éviter de perdre la gestion de "
                        "votre association." % self.object
                    ),
                )
            )

        messages.success(
            self.request,
            "Vous n'êtes plus membre de l'association « %s »." % self.object,
        )

        return HttpResponseRedirect(self.get_success_url())


class ViewSet(ModelViewSet):
    model = Association
    form_class = AssociationForm
    views = {
        **ModelViewSet.views,
        "list": {
            "class": AssociationListView,
            "pattern": "all/",
        },
        "search": {
            "class": AssociationSearchView,
            "pattern": "search/",
        },
        "creation_closed": {
            "class": AssociationCreationClosedView,
            "pattern": "create/closed/",
        },
        "import": {
            "class": AssociationImportView,
            "pattern": "import/",
        },
        "detail": {
            "class": AssociationDetailView,
            "pattern": "<int:pk>/",
        },
        "migrate": {
            "class": AssociationMigrateView,
            "pattern": "<int:pk>/migrate/",
        },
        "join": {
            "class": AssociationJoinView,
            "pattern": "<int:pk>/join/",
        },
        "leave": {
            "class": AssociationLeaveView,
            "pattern": "<int:pk>/leave/",
        },
    }
    views_classes = {
        "index": AssociationIndexView,
        "create": AssociationCreateView,
        "update": AssociationUpdateView,
        "delete": AssociationDeleteView,
    }
