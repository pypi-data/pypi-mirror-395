import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError, transaction
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView, UpdateView

from benevalibre.accounts.forms import (
    AuthenticationForm,
    DeleteForm,
    PasswordResetForm,
    UpdateForm,
)
from benevalibre.accounts.utils import user_to_uidb64
from benevalibre.models import InstanceSettings
from benevalibre.views.generic import PageContextMixin

logger = logging.getLogger("benevalibre.accounts")


class LoginView(PageContextMixin, auth_views.LoginView):
    authentication_form = AuthenticationForm
    # Il ne devrait pas y avoir de risque de boucle tant qu'une exception est
    # levée en cas de permission requise pour accéder à une vue. Voir :
    # https://docs.djangoproject.com/en/stable/topics/auth/default/#django.contrib.auth.views.LoginView.redirect_authenticated_user
    redirect_authenticated_user = True
    page_title = "Connexion"
    template_name = "accounts/login.html"


class LogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Vous avez été déconnecté.")
        return response


class UpdateView(
    PageContextMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    form_class = UpdateForm
    success_url = reverse_lazy("account:update")
    success_message = "Votre compte a été mis à jour."
    page_title = "Mon compte"
    seo_title = "Modifier mon compte"
    template_name = "accounts/update.html"

    def get_object(self):
        return self.request.user


class DeleteView(
    PageContextMixin, LoginRequiredMixin, SuccessMessageMixin, FormView
):
    form_class = DeleteForm
    success_url = settings.LOGIN_URL
    success_message = "Votre compte a été supprimé."
    page_title = "Supprimer mon compte"
    template_name = "accounts/confirm_delete.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        try:
            with transaction.atomic():
                for membership in self.request.user.memberships.all():
                    membership.delete()
                self.request.user.delete()
        except IntegrityError:
            return self.render_to_response(
                self.get_context_data(
                    error_message=(
                        "Vous êtes actuellement le seul à avoir la permission "
                        "de gérer l'association « %s » par le rôle « %s ». "
                        "Veuillez d'abord attribuer ce rôle à un autre membre "
                        "pour éviter de rendre la gestion de cette association "
                        "impossible."
                    )
                    % (membership.association, membership.role),
                ),
            )

        auth_logout(self.request)

        return super().form_valid(form)


class PasswordChangeView(
    PageContextMixin, SuccessMessageMixin, auth_views.PasswordChangeView
):
    success_url = reverse_lazy("account:update")
    success_message = "Votre mot de passe a été modifié."
    page_title = "Mon mot de passe"
    seo_title = "Modifier mon mot de passe"
    template_name = "accounts/password_change.html"


# PASSWORD RESET
# ------------------------------------------------------------------------------


class PasswordResetView(PageContextMixin, SuccessMessageMixin, FormView):
    form_class = PasswordResetForm
    token_generator = default_token_generator
    success_url = settings.LOGIN_URL
    success_message = (
        "Un courriel a été envoyé à « %(email)s » avec les instructions à "
        "suivre pour réinitialiser le mot de passe."
    )
    page_title = "Réinitialiser mon mot de passe"
    template_name = "accounts/password_reset/form.html"
    email_template_name = "accounts/password_reset/email.txt"
    subject_template_name = "accounts/password_reset/email_subject.txt"

    def form_valid(self, form):
        if user := form.get_user():
            self.send_mail(user)

        return super().form_valid(form)

    def send_mail(self, user):
        context = {
            "user": user,
            "reset_url": self.request.build_absolute_uri(
                reverse(
                    "account:password_reset_confirm",
                    kwargs={
                        "uidb64": user_to_uidb64(user),
                        "token": self.token_generator.make_token(user),
                    },
                )
            ),
            "site_name": InstanceSettings.for_request(self.request).site_name,
        }

        subject = render_to_string(self.subject_template_name, context)
        subject = "".join(subject.splitlines())

        body = render_to_string(self.email_template_name, context)

        try:
            user.email_user(subject, body)
        except Exception:
            logger.exception("Failed to send password reset email to %r", user)
        else:
            return True

        return False


class PasswordResetConfirmView(
    PageContextMixin, SuccessMessageMixin, auth_views.PasswordResetConfirmView
):
    token_generator = default_token_generator
    success_url = settings.LOGIN_URL
    success_message = "Votre mot de passe a été réinitialisé."
    page_title = "Réinitialiser mon mot de passe"
    template_name = "accounts/password_reset/confirm.html"
