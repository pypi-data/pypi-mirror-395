from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html
from django.views.decorators.debug import sensitive_variables

from benevalibre.forms.widgets import TogglePasswordInput

from .models import User


class AuthenticationForm(auth_forms.AuthenticationForm):
    """
    Formulaire d'authentification.
    """

    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=TogglePasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": (
            "L'adresse mail et le mot de passe ne correspondent pas, "
            "veuillez réessayer."
        ),
    }


class UpdateForm(forms.ModelForm):
    """
    Formulaire d'édition du compte utilisat⋅eur⋅rice.
    """

    template_name = "forms/layouts/user_update.html"

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "pseudo",
            "avatar",
            "theme",
        ]


class DeleteForm(forms.Form):
    """
    Formulaire de suppression du compte utilisat⋅eur⋅rice.
    """

    current_password = forms.CharField(
        label="Mot de passe actuel",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    @sensitive_variables("current_password")
    def clean_current_password(self):
        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise ValidationError(
                "Le mot de passe ne correspond pas.",
                code="password_incorrect",
            )
        return current_password


class PasswordResetForm(forms.Form):
    """
    Formulaire de demande de réinitialisation du mot de passe.
    """

    email = forms.EmailField(
        label="Adresse mail",
        error_messages={
            "invalid": "Saisissez une adresse mail valide.",
        },
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            self.user_cache = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(
                "Cette adresse mail n'est associée à aucun compte.",
                code="unknown",
            )

        return email

    def clean(self):
        if self.user_cache and not self.user_cache.is_active:
            raise ValidationError(
                format_html(
                    "Ce compte est bien enregistré mais il n'est pas activé. "
                    "Si vous n'avez pas effectué cette étape à sa création, "
                    "vous pouvez demander le <a href='{}'>renvoi d'un lien "
                    "d'activation</a>.",
                    reverse("account:activation_resend"),
                ),
                code="inactive_user",
            )

        return self.cleaned_data

    def get_user(self):
        """
        Vérifie que le compte utilisateur en cache peut recevoir le lien et le
        retourne, l'adresse mail étant unique.
        """
        if (
            self.user_cache
            and self.user_cache.is_active
            and self.user_cache.has_usable_password()
        ):
            return self.user_cache


class RegisterForm(auth_forms.UserCreationForm):
    """
    Formulaire de demande de création d'un compte.
    """

    email = forms.EmailField(
        label="Adresse mail",
        error_messages={
            "invalid": "Saisissez une adresse mail valide.",
        },
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    template_name = "forms/layouts/user_register.html"

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "pseudo"]

    def save(self, commit=True):
        self.instance.is_active = False
        return super().save(commit=commit)


class ActivationResendForm(forms.Form):
    """
    Formulaire de demande de renvoi du lien d'activation du compte.
    """

    email = forms.EmailField(
        label="Adresse mail",
        error_messages={
            "invalid": "Saisissez une adresse mail valide.",
        },
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            self.user_cache = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(
                "Cette adresse mail n'est associée à aucun compte.",
                code="unknown",
            )

        return email

    def get_user(self):
        """
        Vérifie que le compte utilisateur en cache peut recevoir le lien et le
        retourne.
        """
        if (
            self.user_cache
            and not self.user_cache.is_active
            and self.user_cache.has_usable_password()
        ):
            return self.user_cache
