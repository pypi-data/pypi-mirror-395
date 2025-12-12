from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from benevalibre.accounts.models import User


def user_to_uidb64(user):
    """
    Retourne l'identifiant de l'utilisateur encodé en base64 et prêt pour une
    utilisation dans une URL.
    """
    user_pk_bytes = force_bytes(User._meta.pk.value_to_string(user))
    return urlsafe_base64_encode(user_pk_bytes)
