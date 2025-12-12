from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.views.generic.base import ContextMixin

from benevalibre.models import Announcement


class PageContextMixin(ContextMixin):
    """
    Un mixin qui définis le contexte nécessaire pour le rendu d'une page.
    """

    #: Détermine si le contenu de la page doit occuper toute la largeur.
    full_width = False

    #: Le titre de la page qui sera affiché dans l'en-tête.
    page_title = ""

    #: Le titre de la page défini dans la balise `<head>`, utilisé par les
    #: moteurs recherche notamment. S'il est vide, `page_title` est utilisé.
    seo_title = ""

    def get_announcements(self):
        """
        Retourne les annonces à afficher pour l'utilisateur⋅rice.
        """
        return Announcement.objects.active_for_user(self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(
            {
                "page_title": self.page_title,
                "seo_title": self.seo_title or self.page_title,
                "full_width": self.full_width,
                "announcements": self.get_announcements(),
            }
        )
        return context


class ObjectMixin(ContextMixin):
    """
    Un mixin qui récupère un object depuis la requête et qui le stocke, basé sur
    `django.views.generic.detail.SingleObjectMixin`.
    """

    model = None
    queryset = None
    pk_url_kwarg = "pk"
    not_found_message = "Aucun élément %(model)s trouvé pour cette requête."

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object = self.get_object()

    def get_queryset(self):
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. "
                    "Define %(cls)s.model, %(cls)s.queryset, "
                    "or override %(cls)s.get_queryset()."
                    % {"cls": self.__class__.__name__}
                )
        return self.queryset.all()

    def get_object(self):
        queryset = self.get_queryset()

        try:
            obj = queryset.get(pk=self.kwargs[self.pk_url_kwarg])
        except queryset.model.DoesNotExist:
            raise Http404(self.get_not_found_message(queryset.model))

        return obj

    def get_not_found_message(self, model):
        return self.not_found_message % {"model": model._meta.verbose_name}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.object
        return context


class ObjectPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Un mixin qui vérifie que l'utilisateur⋅rice a les permissions requises sur
    l'objet de la requête, généralement récupéré et stocké par `ObjectMixin`.
    """

    def get_permission_object(self):
        return self.object

    def has_permission(self):
        obj = self.get_permission_object()
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms, obj)
