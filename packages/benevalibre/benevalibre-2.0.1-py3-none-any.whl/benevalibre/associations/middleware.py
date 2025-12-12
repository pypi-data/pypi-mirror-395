import uuid

from django.core.exceptions import BadRequest, PermissionDenied
from django.utils import timezone

from benevalibre.associations import (
    ANONYMOUS_MEMBER_QUERY_KEY,
    ANONYMOUS_MEMBER_SESSION_KEY,
)
from benevalibre.associations.models import AssociationAnonymousMember


class AnonymousMemberMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user.is_anonymous_member = False

        if value := request.GET.get(ANONYMOUS_MEMBER_QUERY_KEY, ""):
            if request.user.is_authenticated:
                raise PermissionDenied(
                    "Veuillez vous déconnecter avant d'utiliser ce lien "
                    "d'accès de membre anonyme."
                )
            try:
                anonymous_member = self.get_object(value)
            except ValueError:
                raise BadRequest(
                    "Votre lien d'accès de membre anonyme n'est pas valide."
                )
            except AssociationAnonymousMember.DoesNotExist:
                raise PermissionDenied(
                    "Votre lien d'accès de membre anonyme ne semble plus actif."
                )
            else:
                self.store_session(request, anonymous_member)
        elif value := request.session.get(ANONYMOUS_MEMBER_SESSION_KEY, ""):
            if request.user.is_authenticated:
                # Un compte utilisateur authentifié prend le dessus sur une
                # session encore active d'un membre anonyme, qu'on supprime
                del request.session[ANONYMOUS_MEMBER_SESSION_KEY]
                return self.get_response(request)
            try:
                anonymous_member = self.get_object(value)
            except (ValueError, AssociationAnonymousMember.DoesNotExist):
                # Vide silencieusement la session pas ou plus valide
                request.session.flush()
                return self.get_response(request)
        else:
            return self.get_response(request)

        request.user = anonymous_member
        return self.get_response(request)

    def get_object(self, value):
        return AssociationAnonymousMember.objects.active().get(
            uuid=uuid.UUID(value)
        )

    def store_session(self, request, anonymous_member):
        anonymous_member.last_visit = timezone.now()
        anonymous_member.save(update_fields=["last_visit"])

        request.session[ANONYMOUS_MEMBER_SESSION_KEY] = str(
            anonymous_member.uuid
        )

        # La session expirera à la fermeture du navigateur
        request.session.set_expiry(0)
