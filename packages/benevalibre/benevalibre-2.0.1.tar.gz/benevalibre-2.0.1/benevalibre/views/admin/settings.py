from django.urls import reverse_lazy

from benevalibre.forms.admin import InstanceSettingsForm
from benevalibre.models import InstanceSettings
from benevalibre.views import generic

from . import AdminViewMixin


class UpdateView(AdminViewMixin, generic.UpdateView):
    form_class = InstanceSettingsForm
    success_url = reverse_lazy("instance_settings")
    success_message = "Paramètres de « %(object)s » mis à jour."

    page_title = "Paramètres"
    seo_title = "Paramètres de l'instance"

    def get_object(self):
        return InstanceSettings.for_request(self.request)

    def get_update_url(self):
        return self.get_success_url()
