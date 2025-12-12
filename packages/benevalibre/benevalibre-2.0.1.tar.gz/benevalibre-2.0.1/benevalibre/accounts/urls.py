from django.urls import path

from benevalibre.accounts.views import account as account_views
from benevalibre.accounts.views import registration as registration_views

app_name = "accounts"

urlpatterns = [
    path("login/", account_views.LoginView.as_view(), name="login"),
    path("logout/", account_views.LogoutView.as_view(), name="logout"),
    path("update/", account_views.UpdateView.as_view(), name="update"),
    path("delete/", account_views.DeleteView.as_view(), name="delete"),
    path(
        "password/change/",
        account_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password/reset/",
        account_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password/reset/<uidb64>/<token>/",
        account_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "register/",
        registration_views.RegisterView.as_view(),
        name="register",
    ),
    path(
        "register/closed/",
        registration_views.RegistrationClosedView.as_view(),
        name="registration_closed",
    ),
    path(
        "activate/<uidb64>/<token>/",
        registration_views.ActivateView.as_view(),
        name="activate",
    ),
    path(
        "activate/resend/",
        registration_views.ActivationResendView.as_view(),
        name="activation_resend",
    ),
]
