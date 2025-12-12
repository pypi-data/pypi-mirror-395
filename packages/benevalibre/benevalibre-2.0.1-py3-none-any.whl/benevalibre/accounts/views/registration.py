import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import INTERNAL_RESET_SESSION_TOKEN
from django.contrib.messages.views import SuccessMessageMixin
from django.core import signing
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from benevalibre.accounts.forms import ActivationResendForm, RegisterForm
from benevalibre.accounts.models import User
from benevalibre.accounts.utils import user_to_uidb64
from benevalibre.models import InstanceSettings
from benevalibre.views.generic import PageContextMixin

from .account import PasswordResetConfirmView

REGISTRATION_SALT = "benevalibre.accounts.registration"

logger = logging.getLogger("benevalibre.accounts")


def send_activation_mail(
    user,
    request,
    extra_context={},
    email_template_name="accounts/registration/activation_email.txt",
    subject_template_name="accounts/registration/activation_email_subject.txt",
):
    context = {
        "user": user,
        "expiration_days": int(settings.USER_ACTIVATION_TIMEOUT / 86400),
        "activation_url": request.build_absolute_uri(
            reverse(
                "account:activate",
                kwargs={
                    "uidb64": user_to_uidb64(user),
                    "token": signing.dumps(user.email, salt=REGISTRATION_SALT),
                },
            )
        ),
        "site_name": InstanceSettings.for_request(request).site_name,
    }
    context.update(extra_context)

    subject = render_to_string(subject_template_name, context)
    subject = "".join(subject.splitlines())

    body = render_to_string(email_template_name, context)

    try:
        user.email_user(subject, body)
    except Exception:
        logger.exception("Failed to send activation email to %r", user)
    else:
        return True

    return False


class RegisterView(PageContextMixin, SuccessMessageMixin, FormView):
    form_class = RegisterForm
    closed_url = reverse_lazy("account:registration_closed")
    success_url = settings.LOGIN_URL
    success_message = (
        "Un courriel a été envoyé à « %(email)s » avec les instructions à "
        "suivre pour activer votre compte. Une fois cette étape effectuée, "
        "vous pourrez alors vous connecter."
    )
    page_title = "Créer un compte"
    template_name = "accounts/registration/register.html"

    @method_decorator(sensitive_post_parameters("password1", "password2"))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if not getattr(settings, "USER_REGISTRATION_OPEN", True):
            return HttpResponseRedirect(self.closed_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()

        send_activation_mail(self.object, request=self.request)

        return super().form_valid(form)


class RegistrationClosedView(PageContextMixin, TemplateView):
    register_url = reverse_lazy("account:register")
    page_title = "Créer un compte"
    seo_title = "Création de compte indisponible"
    template_name = "accounts/registration/closed.html"

    def dispatch(self, request, *args, **kwargs):
        if getattr(settings, "USER_REGISTRATION_OPEN", True):
            return HttpResponseRedirect(self.register_url)
        return super().dispatch(request, *args, **kwargs)


class ActivateView(PageContextMixin, TemplateView):
    success_url = settings.LOGIN_URL
    page_title = "Activation du compte"
    seo_title = "Activation du compte impossible"
    template_name = "accounts/registration/activation_failed.html"

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None and not self.user.is_active:
            try:
                email = signing.loads(
                    kwargs["token"],
                    salt=REGISTRATION_SALT,
                    max_age=settings.USER_ACTIVATION_TIMEOUT,
                )
            except signing.BadSignature:
                pass
            else:
                if email == self.user.email:
                    return self.activate_to_response()

        return super().dispatch(*args, **kwargs)

    def activate_to_response(self):
        """
        Active le compte utilisateur et redirige vers la page de connexion.
        """
        self.user.is_active = True
        self.user.save(update_fields=["is_active"])

        # Le mot de passe du compte n'est pas importé avec les données de
        # l'association et n'est pas utilisable dans ce cas, on redirige vers
        # sa réinitialisation en passant par la session pour le token
        if not self.user.has_usable_password():
            redirect_url = reverse(
                "accounts:password_reset_confirm",
                kwargs={
                    "uidb64": user_to_uidb64(self.user),
                    "token": PasswordResetConfirmView.reset_url_token,
                },
            )
            self.request.session[INTERNAL_RESET_SESSION_TOKEN] = (
                PasswordResetConfirmView.token_generator.make_token(self.user)
            )

            messages.success(
                self.request,
                "Votre compte est désormais activé ! Vous pouvez maintenant "
                "définir votre mot de passe avant de vous connecter avec votre "
                "adresse mail « %s »." % self.user.email,
            )

            return HttpResponseRedirect(redirect_url)

        messages.success(
            self.request,
            "Votre compte est désormais activé ! Vous pouvez maintenant vous "
            "connecter avec votre adresse mail « %s »." % self.user.email,
        )

        return HttpResponseRedirect(self.success_url)

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            pk = User._meta.pk.to_python(uid)
            user = User.objects.get(pk=pk)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return context


class ActivationResendView(PageContextMixin, SuccessMessageMixin, FormView):
    form_class = ActivationResendForm
    success_url = settings.LOGIN_URL
    success_message = (
        "Un courriel a été envoyé à « %(email)s » avec les instructions à "
        "suivre pour activer le compte."
    )
    page_title = "Activation du compte"
    seo_title = "Renvoyer le courriel d'activation du compte"
    template_name = "accounts/registration/activation_resend.html"

    def form_valid(self, form):
        if user := form.get_user():
            send_activation_mail(user, request=self.request)

        return super().form_valid(form)
