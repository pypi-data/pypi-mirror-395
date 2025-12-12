from django.conf import settings
from django.db.models import Q
from django.db.models.signals import post_save
from django.urls import reverse

from django_cleanup.signals import cleanup_pre_delete
from sorl.thumbnail import delete as thumbnail_delete

from benevalibre.accounts.models import User
from benevalibre.associations.models import Association, AssociationMembership
from benevalibre.models import Benevalo
from benevalibre.notifications import notify_users
from benevalibre.utils import get_absolute_uri


def on_moderated_association_created(sender, instance, created, **kwargs):
    if (
        not created
        or instance.is_active
        or not settings.ASSOCIATION_REGISTRATION_MODERATED
    ):
        return

    context = {
        "association": instance,
        "manage_url": get_absolute_uri(
            reverse("associations:update", args=(instance.pk,))
        ),
    }
    users = User.objects.active().filter(is_superuser=True)

    notify_users(users, "moderated_association_created", context)


def on_moderated_membership_created(sender, instance, created, **kwargs):
    if (
        not created
        or instance.is_active
        or not instance.association.moderate_membership
    ):
        return

    context = {
        "association": instance.association,
        "user": instance.user,
        "manage_url": get_absolute_uri(
            reverse(
                "association_members:update",
                kwargs={
                    "association": instance.association_id,
                    "pk": instance.pk,
                },
            )
        ),
    }
    users = User.objects.active().filter(
        Q(membership__role__manage_members=True)
        | Q(membership__role__manage_association=True),
        membership__association=instance.association_id,
        membership__is_active=True,
    )

    notify_users(users, "moderated_membership_created", context)


def on_moderated_benevalo_created(sender, instance, created, **kwargs):
    if (
        not created
        or instance.is_active
        or not instance.association.moderate_benevalo
    ):
        return

    context = {
        "benevalo": instance,
        "association": instance.association,
        "user": instance.user,
        "manage_url": get_absolute_uri(
            reverse(
                "association_benevalos:update",
                kwargs={
                    "association": instance.association_id,
                    "pk": instance.pk,
                },
            )
        ),
    }
    users = User.objects.active().filter(
        Q(membership__role__manage_benevalos=True)
        | Q(membership__role__manage_association=True),
        membership__association=instance.association_id,
        membership__is_active=True,
    )

    notify_users(users, "moderated_benevalo_created", context)


def on_cleanup_pre_delete(**kwargs):
    thumbnail_delete(kwargs["file"])


def connect_signal_handlers():
    post_save.connect(
        on_moderated_association_created,
        dispatch_uid="notify_on_moderated_association_created",
        sender=Association,
    )
    post_save.connect(
        on_moderated_membership_created,
        dispatch_uid="notify_on_moderated_membership_created",
        sender=AssociationMembership,
    )
    post_save.connect(
        on_moderated_benevalo_created,
        dispatch_uid="notify_on_moderated_benevalo_created",
        sender=Benevalo,
    )

    cleanup_pre_delete.connect(on_cleanup_pre_delete)
