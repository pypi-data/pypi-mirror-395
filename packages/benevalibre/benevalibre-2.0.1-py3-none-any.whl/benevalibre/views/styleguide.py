from django import forms
from django.urls import reverse_lazy
from django.views.generic import FormView

from benevalibre.views.mixins import PageContextMixin


class ShowcaseForm(forms.Form):
    name = forms.CharField(
        label="Nom",
        help_text="Un message d'aide pour ce champ.",
    )
    email = forms.EmailField(label="Adresse mail", required=False)
    subject = forms.ChoiceField(
        label="Objet",
        choices=(
            ("option1", "Option 1"),
            ("option2", "Option 2"),
            ("option3", "Option 3"),
        ),
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"rows": "3"}),
    )
    attachment = forms.FileField(label="Fichier attaché", required=False)
    multiple_options = forms.MultipleChoiceField(
        label="Choix multiples",
        choices=(
            ("option1", "Option 1"),
            ("option2", "Option 2"),
            ("option3", "Option 3"),
        ),
    )
    choose_options = forms.ChoiceField(
        label="Choix radio",
        choices=(
            ("option1", "Option 1"),
            ("option2", "Option 2"),
            ("option3", "Option 3"),
        ),
        widget=forms.RadioSelect,
    )
    confirm = forms.BooleanField(
        label="Veuillez confirmer",
        help_text="Un message d'aide pour ce champ.",
    )


class StyleGuideView(PageContextMixin, FormView):
    template_name = "styleguide.html"
    form_class = ShowcaseForm
    success_url = reverse_lazy("styleguide")

    page_title = "Guide des styles"
