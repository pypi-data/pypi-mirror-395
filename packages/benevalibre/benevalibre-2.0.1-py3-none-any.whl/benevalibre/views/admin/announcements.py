from benevalibre.forms import NativeDateTimeInput
from benevalibre.models import Announcement
from benevalibre.views import generic
from benevalibre.viewsets import ModelViewSet

from . import AdminViewMixin


class IndexView(AdminViewMixin, generic.IndexView):
    page_title = "Annonces"
    seo_title = "Liste des annonces d'instance"
    create_item_label = "Ajouter une annonce"

    default_ordering = "-publication_date"
    list_display = ("title", "publication_date", "expiration_date", "author")
    list_filter = ("target",)


class CreateView(AdminViewMixin, generic.CreateView):
    page_title = "Nouvelle annonce"
    success_message = "Annonce « %(object)s » créée."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateView(AdminViewMixin, generic.UpdateView):
    page_title = "Modification de l'annonce"
    success_message = "Annonce « %(object)s » mise à jour."


class DeleteView(AdminViewMixin, generic.DeleteView):
    page_title = "Suppression de l'annonce"
    success_message = "Annonce « %(object)s » supprimée."


class ViewSet(ModelViewSet):
    model = Announcement
    form_fields = [
        "title",
        "content",
        "target",
        "publication_date",
        "expiration_date",
    ]
    form_extra_kwargs = {
        "widgets": {
            "publication_date": NativeDateTimeInput(),
            "expiration_date": NativeDateTimeInput(),
        },
    }
    views_classes = {
        "index": IndexView,
        "create": CreateView,
        "update": UpdateView,
        "delete": DeleteView,
    }
