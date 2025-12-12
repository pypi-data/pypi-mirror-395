from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.db import IntegrityError, models, transaction
from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.http import content_disposition_header
from django.utils.text import capfirst
from django.views.generic import FormView, View
from django.views.generic.base import TemplateResponseMixin

import tablib
from django_filters.filterset import filterset_factory
from django_tables2 import table_factory
from django_tables2.columns.base import LinkTransform

from benevalibre.filters.base import BaseFilterSet
from benevalibre.menus import BoundMenuItem
from benevalibre.tables.base import BaseExportTable, BaseTable
from benevalibre.tables.columns import ActionsColumn

from .mixins import ObjectMixin, PageContextMixin


class ExportFormat(models.TextChoices):
    CSV = "csv", "Comme tableur (CSV)"
    XLSX = "xlsx", "Comme tableur (XLSX)"
    JSON = "json", "Données brutes (JSON)"

    @classmethod
    def get_content_type(cls, format):
        if format == cls.CSV:
            return "text/csv; charset=utf-8"
        if format == cls.XLSX:
            return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # noqa: E501
        if format == cls.JSON:
            return "application/json"
        raise ValueError(f"Unexpected format '{format}'")


class IndexView(
    PageContextMixin,
    TemplateResponseMixin,
    View,
):
    full_width = True
    template_name = "generic/index.html"
    base_template_name = "base.html"

    #: La liste des noms de champs du modèle à afficher comme colonnes du
    #: tableau, utilisée si `table_class` n'est pas défini.
    list_display = None

    #: La liste des noms de champs du modèle sur lesquels il sera possible de
    #: filtrer les données, utilisée si `filterset_class` n'est pas défini. Les
    #: filtres seront désactivés si aucun de ces attributs n'est défini.
    list_filter = None

    #: La liste des noms de champs du modèle à inclure lors de l'export des
    #: données, utilisée si `export_table_class` n'est pas défini. L'export ne
    #: sera pas proposé si aucun de ces attributs n'est défini.
    list_export = None

    model = None
    queryset = None
    default_ordering = None
    ordering_kwarg = "ordering"
    page_kwarg = "page"
    paginate_by = 20

    index_url_name = None
    create_url_name = None
    update_url_name = None
    delete_url_name = None

    create_item_label = "Ajouter"
    delete_item_label = "Supprimer"

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        if self.has_export and request.GET.get("export") in ExportFormat:
            return self.export_to_response(request.GET.get("export"))

        context = self.get_context_data()
        return self.render_to_response(context)

    @cached_property
    def filterset_class(self):
        if self.model and self.list_filter:
            return filterset_factory(
                self.model,
                filterset=BaseFilterSet,
                fields=self.list_filter,
            )

    @cached_property
    def filterset(self):
        if self.filterset_class:
            filterset = self.filterset_class(**self.get_filterset_kwargs())
            # Active les filtres que si au moins un champ est défini
            if filterset.form.fields:
                return filterset

    @cached_property
    def is_filtering(self):
        return (
            self.filterset
            and self.filterset.is_valid()
            and self.filterset.form.has_changed()
        )

    def get_filterset_kwargs(self):
        return {
            "data": self.request.GET,
            "request": self.request,
        }

    def filter_queryset(self, queryset):
        if self.filterset and self.filterset.is_valid():
            return self.filterset.filter_queryset(queryset)
        return queryset

    def get_ordering(self):
        """
        Retourne l'ordre de tri actuel ou celui par défaut, défini par
        l'attribut `default_ordering`.
        """
        return self.request.GET.get(self.ordering_kwarg, self.default_ordering)

    def get_base_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, models.QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_base_queryset()."
                % {"cls": self.__class__.__name__}
            )
        return queryset

    def get_queryset(self):
        # La logique initiale de django.views.generic.list.MultipleObjectMixin
        # est déplacée dans get_base_queryset(), le reste est découpé dans
        # différentes méthodes pour plus de souplesse
        queryset = self.get_base_queryset()
        queryset = self.filter_queryset(queryset)
        return queryset

    @property
    def has_export(self):
        return bool(self.export_table_class)

    @cached_property
    def export_table_class(self):
        if self.model and self.list_export:
            return table_factory(
                self.model,
                table=BaseExportTable,
                fields=self.list_export,
            )

    def get_export_filename(self):
        return "%s-export" % self.model._meta.model_name

    def get_export_dataset(self, object_list):
        dataset = tablib.Dataset()
        table = self.export_table_class(data=object_list)
        table_values = table.as_values()
        dataset.headers = next(table_values)
        for row in table_values:
            dataset.append(row)
        return dataset

    def export_to_response(self, format):
        dataset = self.get_export_dataset(self.object_list)

        return HttpResponse(
            dataset.export(format),
            headers={
                "Content-Type": ExportFormat.get_content_type(format),
                "Content-Disposition": content_disposition_header(
                    as_attachment=True,
                    filename=f"{self.get_export_filename()}.{format}",
                ),
            },
        )

    @cached_property
    def table_class(self):
        if not self.model or not self.list_display:
            raise ImproperlyConfigured(
                "%(cls)s is missing a table class. "
                "Define %(cls)s.table_class, "
                "or %(cls)s.model and %(cls)s.list_display."
                % {"cls": self.__class__.__name__}
            )
        return table_factory(
            self.model,
            table=BaseTable,
            fields=self.list_display,
        )

    def get_table(self, object_list):
        table = self.table_class(data=object_list, **self.get_table_kwargs())

        if title_column := self._get_title_column_name():

            def get_update_url(record):
                return self.get_update_url(record)

            table.columns[title_column].link = LinkTransform(
                attrs={"class": "title"},
                url=get_update_url,
            )

        if self.paginate_by:
            page_number = self.request.GET.get(self.page_kwarg, default=1)

            try:
                table.paginate(per_page=self.paginate_by, page=page_number)
            except PageNotAnInteger:
                table.page = table.paginator.page(1)
            except EmptyPage:
                table.page = table.paginator.page(table.paginator.num_pages)

        return table

    def get_table_kwargs(self):
        return {
            "order_by": self.get_ordering(),
            "order_by_field": self.ordering_kwarg,
            "page_field": self.page_kwarg,
            "empty_text": (
                "Aucun élément à afficher."
                if not self.is_filtering
                else "Aucun élément ne correspond à ces filtres."
            ),
            "extra_columns": [
                ("actions", self._get_actions_column()),
            ],
            "filterset": self.filterset,
        }

    def _get_actions_column(self):
        def get_menu_items(column, record):
            return self.get_action_menu_items(record)

        column_class = type(
            "ActionsColumn",
            (ActionsColumn,),
            {"get_menu_items": get_menu_items},
        )

        return column_class()

    def _get_title_column_name(self):
        if hasattr(self, "title_column_name"):
            return self.title_column_name
        if self.list_display:
            return self.list_display[0]

    def get_export_url(self, format):
        params = self.request.GET.copy()
        params["export"] = format
        return self.request.path + "?" + params.urlencode()

    def get_index_url(self):
        if not self.index_url_name:
            raise ImproperlyConfigured(
                "%(cls)s is missing index URL. "
                "Define %(cls)s.index_url_name "
                "or override %(cls)s.get_index_url()."
                % {"cls": self.__class__.__name__}
            )
        return reverse(self.index_url_name)

    @cached_property
    def index_url(self):
        return self.get_index_url()

    def get_create_url(self):
        if self.create_url_name:
            return reverse(self.create_url_name)

    @cached_property
    def create_url(self):
        return self.get_create_url()

    def get_update_url(self, instance):
        if self.update_url_name:
            return reverse(self.update_url_name, args=(instance.pk,))

    def get_delete_url(self, instance):
        if self.delete_url_name:
            return reverse(self.delete_url_name, args=(instance.pk,))

    def get_action_menu_items(self, instance):
        items = []

        if update_url := self.get_update_url(instance):
            items.append(
                BoundMenuItem(
                    label="Modifier",
                    url=update_url,
                    icon_name="edit",
                    attrs={
                        "aria-label": "Modifier « %(title)s »"
                        % {"title": str(instance)},
                    },
                )
            )

        if delete_url := self.get_delete_url(instance):
            items.append(
                BoundMenuItem(
                    label="Supprimer",
                    url=delete_url,
                    icon_name="trash",
                    attrs={
                        "aria-label": "Supprimer « %(title)s »"
                        % {"title": str(instance)},
                    },
                )
            )

        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table"] = self.get_table(self.object_list)
        context["index_url"] = self.index_url
        if self.create_url:
            context["create_url"] = self.create_url
            context["create_item_label"] = self.create_item_label
        if self.filterset:
            context["filterset"] = self.filterset
            context["is_filtering"] = self.is_filtering
        if self.has_export:
            context["export_menu_items"] = [
                BoundMenuItem(
                    label=export_format.label,
                    url=self.get_export_url(export_format.value),
                )
                for export_format in ExportFormat
            ]
        return context


class CreateView(PageContextMixin, FormView):
    """Vue de création d'un objet.

    Cette vue générique est prévue pour être initialisée depuis une classe
    héritant de `benevalibre.viewsets.ModelViewSet`. Contrairement à la vue
    générique de Django, celle-ci s'attend donc à une propriété `form_class`.
    """

    template_name = "generic/create.html"
    base_template_name = "base.html"

    model = None
    form_class = None
    index_url_name = None
    create_url_name = None
    submit_button_label = "Créer"
    success_message = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object = None

    def get_index_url(self):
        if self.index_url_name:
            return reverse(self.index_url_name)

    def get_create_url(self):
        if not self.create_url_name:
            raise ImproperlyConfigured(
                "%(cls)s is missing create URL. "
                "Define %(cls)s.create_url_name "
                "or override %(cls)s.get_create_url()."
                % {"cls": self.__class__.__name__}
            )
        return reverse(self.create_url_name)

    @cached_property
    def create_url(self):
        return self.get_create_url()

    def get_success_url(self):
        if self.success_url:
            return str(self.success_url)
        if index_url := self.get_index_url():
            return index_url
        raise ImproperlyConfigured(
            "%(cls)s is missing success URL. "
            "Define `index_url_name`, `success_url`, "
            "or override `get_success_url()`." % {"cls": self.__class__}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = self.create_url
        context["submit_button_label"] = self.submit_button_label
        return context

    def save_object(self):
        return self.form.save()

    def form_valid(self, form):
        self.form = form

        with transaction.atomic():
            self.object = self.save_object()

        if success_message := self.get_success_message():
            messages.success(self.request, success_message)

        return redirect(self.get_success_url())

    def get_success_message(self):
        if self.success_message:
            return self.success_message % {"object": self.object}


class UpdateView(PageContextMixin, ObjectMixin, FormView):
    """Vue de modification d'un objet.

    L'objet est récupéré et stocké lors de l'appel à `setup()`.

    Cette vue générique est prévue pour être initialisée depuis une classe
    héritant de `benevalibre.viewsets.ModelViewSet`. Contrairement à la vue
    générique de Django, celle-ci s'attend donc à une propriété `form_class`.
    """

    template_name = "generic/update.html"
    base_template_name = "base.html"

    form_class = None
    index_url_name = None
    update_url_name = None
    delete_url_name = None
    submit_button_label = "Enregistrer"
    delete_item_label = "Supprimer"
    success_message = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def get_index_url(self):
        if self.index_url_name:
            return reverse(self.index_url_name)

    def get_update_url(self):
        if not self.update_url_name:
            raise ImproperlyConfigured(
                "%(cls)s is missing update URL. "
                "Define %(cls)s.update_url_name "
                "or override %(cls)s.get_update_url()."
                % {"cls": self.__class__.__name__}
            )
        return reverse(self.update_url_name, args=(self.object.pk,))

    def get_delete_url(self):
        if self.delete_url_name:
            return reverse(self.delete_url_name, args=(self.object.pk,))

    def get_success_url(self):
        if self.success_url:
            return str(self.success_url)
        if index_url := self.get_index_url():
            return index_url
        raise ImproperlyConfigured(
            "%(cls)s is missing success URL. "
            "Define %(cls)s.index_url_name, %(cls)s.success_url, "
            "or override %(cls)s.get_success_url()."
            % {"cls": self.__class__.__name__}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = self.get_update_url()
        context["submit_button_label"] = self.submit_button_label
        context["delete_url"] = self.get_delete_url()
        context["delete_item_label"] = self.delete_item_label
        return context

    def save_object(self):
        return self.form.save()

    def form_valid(self, form):
        self.form = form

        with transaction.atomic():
            self.object = self.save_object()

        if success_message := self.get_success_message():
            messages.success(self.request, success_message)

        return redirect(self.get_success_url())

    def get_success_message(self):
        if self.success_message:
            return self.success_message % {"object": self.object}


class DeleteView(PageContextMixin, ObjectMixin, FormView):
    """Vue de suppression d'un objet.

    L'objet est récupéré et stocké lors de l'appel à `setup()`. Les objets liés
    qui pourraient bloquer sa suppression sont attrapés et présentés à l'envoi
    du formulaire.

    Cette vue générique est prévue pour être initialisée depuis une classe
    héritant de `benevalibre.viewsets.ModelViewSet`. Contrairement à la vue
    générique de Django, le traîtement ne se fait que depuis la méthode POST,
    étant donné qu'un formulaire ne peut pas être envoyé avec DELETE.
    """

    form_class = Form
    template_name = "generic/confirm_delete.html"
    base_template_name = "base.html"

    index_url_name = None
    delete_url_name = None
    submit_button_label = "Supprimer"
    confirmation_message = (
        "Voulez-vous vraiment supprimer l'élément « %(object)s » ?"
    )
    protected_error_message = (
        "L'élément « %(object)s » est actuellement lié à d'autres objets et ne "
        "peut être supprimé en l'état sans compromettre l'intégrité des "
        "données."
    )
    success_message = None

    def get_index_url(self):
        if self.index_url_name:
            return reverse(self.index_url_name)

    def get_delete_url(self):
        if not self.delete_url_name:
            raise ImproperlyConfigured(
                "%(cls)s is missing delete URL. "
                "Define %(cls)s.delete_url_name "
                "or override %(cls)s.get_delete_url()."
                % {"cls": self.__class__.__name__}
            )
        return reverse(self.delete_url_name, args=(self.object.pk,))

    def get_success_url(self):
        if self.success_url:
            return str(self.success_url)
        if index_url := self.get_index_url():
            return index_url
        raise ImproperlyConfigured(
            "%(cls)s is missing success URL. "
            "Define %(cls)s.index_url_name, %(cls)s.success_url, "
            "or override %(cls)s.get_success_url()."
            % {"cls": self.__class__.__name__}
        )

    def get_cancel_url(self):
        return self.get_success_url()

    def get_confirmation_message(self):
        return self.confirmation_message % {"object": self.object}

    def get_protected_error_message(self, exc):
        return self.protected_error_message % {"object": self.object}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = self.get_delete_url()
        context["cancel_url"] = self.get_cancel_url()
        if "error_message" in context:
            context["submit_button_label"] = "Réessayer"
        else:
            context["confirmation_message"] = self.get_confirmation_message()
            context["submit_button_label"] = self.submit_button_label
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object.delete()
        except models.ProtectedError as exc:
            return self.render_to_response(
                self.get_context_data(
                    error_message=self.get_protected_error_message(exc),
                    related_objects=self.format_related_objects(
                        exc.protected_objects
                    ),
                )
            )
        except models.RestrictedError as exc:
            return self.render_to_response(
                self.get_context_data(
                    error_message=self.get_protected_error_message(exc),
                    related_objects=self.format_related_objects(
                        exc.restricted_objects
                    ),
                )
            )
        except IntegrityError as exc:
            return self.render_to_response(
                self.get_context_data(
                    error_message=exc.args[0],
                )
            )

        if success_message := self.get_success_message():
            messages.success(self.request, success_message)

        return redirect(self.get_success_url())

    def get_success_message(self):
        if self.success_message:
            return self.success_message % {"object": self.object}

    def format_related_objects(self, objects):
        """
        Retourne une liste de 2-tuple `(modèle, objet)` pour les objets donnés.
        """
        return [
            (capfirst(obj.__class__._meta.verbose_name), obj) for obj in objects
        ]
