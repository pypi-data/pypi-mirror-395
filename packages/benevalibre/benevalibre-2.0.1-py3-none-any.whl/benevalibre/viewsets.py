import copy

from django.core.exceptions import ImproperlyConfigured
from django.forms.models import modelform_factory
from django.urls import include, path
from django.utils.decorators import classonlymethod
from django.utils.functional import cached_property

from benevalibre.views import generic


class ViewSet:
    #: Le nom de cette collection, utilisé par défaut pour l'espace de noms.
    name = None

    #: La définition des vues de cette collection, comme un dictionnaire dont la
    #: clé est le nom de la vue, et la valeur sa définition attendue sous forme
    #: d'un dictionnaire avec les clés suivantes :
    #: - `class` : la classe de cette vue
    #: - `pattern` : le chemin d'URL relatif de cette vue
    views = {}

    #: La surcharge des classes de vues, comme un dictionnaire dont la clé est
    #: le nom de la vue et la valeur la classe à utiliser, venant remplacer
    #: celle définie par l'attribut `views`.
    views_classes = {}

    #: Les vues à exclure de cette collection, comme une séquence de noms de
    #: vues qui seraient définies par l'attribut `views`.
    views_excluded = []

    def __init__(self, name=None, **kwargs):
        if name:
            self.__dict__["name"] = name

        for key, value in kwargs.items():
            self.__dict__[key] = value

        self.views = copy.deepcopy(self.views)

        # Mets à jour les vues de cette collection en fonction des paramètres
        for view_name, view_class in self.views_classes.items():
            self.views[view_name]["class"] = view_class
        for view_name in self.views_excluded:
            del self.views[view_name]

    def get_common_view_kwargs(self, **kwargs):
        """
        Retourne un dictionnaire des arguments nommés à passer à toutes les vues
        de cette collection.
        """
        return kwargs

    def construct_view(self, view_class, view_name):
        """
        Appel et retourne `view_class.as_view()` en passant les arguments nommés
        de `get_common_view_kwargs()` ainsi que tous ceux passés à cette méthode
        en filtrant ceux qui nous sont pas attendus par la vue.
        """
        kwargs = {
            key: value
            for key, value in self.get_common_view_kwargs().items()
            if hasattr(view_class, key)
        }

        if get_view_kwargs := getattr(
            self, f"get_{view_name}_view_kwargs", None
        ):
            kwargs.update(get_view_kwargs())

        return view_class.as_view(**kwargs)

    @cached_property
    def url_namespace(self):
        """
        L'espace de noms d'URL des vues de cette collection, qui sera utilisé
        pour l'espace de noms d'application ainsi que celui d'instance.

        Par défaut, l'attribut `name` de cette collection.
        """
        if not self.name:
            raise ImproperlyConfigured(
                "Les sous-classes de benevalibre.viewsets.ViewSet doivent "
                "définir un attribut `name`."
            )
        return self.name

    def get_urlpatterns(self):
        """
        Retourne la séquence de chemins d'URL de cette collection.
        """
        return [
            path(
                view_dict["pattern"],
                self.construct_view(view_dict["class"], view_name),
                name=view_name,
            )
            for view_name, view_dict in self.views.items()
        ]

    def get_url_name(self, view_name):
        """
        Retourne l'URL avec espace de noms à résoudre pour la vue donnée.
        """
        return f"{self.url_namespace:s}:{view_name:s}"

    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Instancie la collection avec les arguments nommés donnés et retourne
        sa configuration d'URL incluse, à utiliser comme argument `view` de la
        méthode `django.urls.path`.
        """
        self = cls(**initkwargs)

        if urlpatterns := self.get_urlpatterns():
            return include(
                (urlpatterns, self.url_namespace),
                namespace=self.url_namespace,
            )

        raise ImproperlyConfigured(
            "Aucun chemin d'URL n'est défini pour la collection %r." % cls
        )


class ModelViewSet(ViewSet):
    views = {
        "index": {
            "class": generic.IndexView,
            "pattern": "",
        },
        "create": {
            "class": generic.CreateView,
            "pattern": "create/",
        },
        "update": {
            "class": generic.UpdateView,
            "pattern": "<int:pk>/update/",
        },
        "delete": {
            "class": generic.DeleteView,
            "pattern": "<int:pk>/delete/",
        },
    }

    #: La classe à utiliser pour le formulaire de création et de modification.
    #: Il est possible de définir à la place `form_fields` pour générer
    #: automatiquement cette classe.
    form_class = None

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)

        if not self.model:
            raise ImproperlyConfigured(
                "Les sous-classes de benevalibre.viewsets.ModelViewSet doivent "
                "définir un attribut `model`."
            )

        self.model_opts = self.model._meta
        self.model_name = self.model_opts.model_name

    @cached_property
    def name(self):
        """
        Le nom de cette collection, utilisé par défaut pour l'espace de noms.

        Par défaut, le nom du modèle.
        """
        return self.model_name

    def get_common_view_kwargs(self, **kwargs):
        common_kwargs = {
            f"{view_name}_url_name": self.get_url_name(view_name)
            for view_name in self.views.keys()
        }
        common_kwargs.update(kwargs)
        return super().get_common_view_kwargs(model=self.model, **common_kwargs)

    def get_create_view_kwargs(self, **kwargs):
        return {"form_class": self.get_form_class(), **kwargs}

    def get_update_view_kwargs(self, **kwargs):
        return {"form_class": self.get_form_class(for_update=True), **kwargs}

    def get_form_class(self, for_update=False):
        """
        Retourne la classe à utiliser pour les formulaires de création et de
        modification.
        """
        if self.form_class is not None:
            return self.form_class
        if fields := self.get_form_fields():
            return modelform_factory(
                self.model,
                fields=fields,
                **self.get_form_extra_kwargs(),
            )
        raise ImproperlyConfigured(
            "%(cls)s is missing a form class. "
            "Define `form_class`, `form_fields`, "
            "or override `get_form_class()`." % {"cls": self.__class__}
        )

    def get_form_fields(self):
        """
        Retourne la séquence des champs du modèle à inclure dans les formulaires
        de création et de modification.
        """
        return getattr(self, "form_fields", None)

    def get_form_extra_kwargs(self):
        """
        Retourne un dictionnaire d'arguments nommés à passer à la méthode
        `django.forms.models.modelform_factory`, autre que `model`, `fields` et
        `exclude` déjà définis par la méthode `get_form_class`.
        """
        return getattr(self, "form_extra_kwargs", {})
