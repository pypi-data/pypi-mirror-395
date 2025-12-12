import uuid

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.db.models import F, Q
from django.db.models.functions import Concat, Lower
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property

import reversion
from django_countries.fields import CountryField
from dynamic_filenames import FilePattern

from benevalibre.associations import ANONYMOUS_MEMBER_QUERY_KEY

from .base import (
    BaseBenevaloCategory,
    BaseBenevaloLevel,
    BaseRole,
    BaseRoleManager,
)
from .defaults import DefaultBenevaloCategory, DefaultBenevaloLevel, DefaultRole

upload_logo_to = FilePattern(filename_pattern="logos/{uuid:x}{ext}")


def is_registration_opened():
    return not settings.ASSOCIATION_REGISTRATION_MODERATED


class ActivityFieldGroup(models.Model):
    name = models.CharField("nom", max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_activity_field_group_name",
                violation_error_code="unique_name",
                violation_error_message=(
                    "Un groupe de champs d'activité avec ce nom existe déjà."
                ),
            ),
        ]
        verbose_name = "groupe de champs d'activité"
        verbose_name_plural = "groupes de champs d'activité"

    def __str__(self):
        return self.name


class ActivityFieldManager(models.Manager):
    def get_by_natural_key(self, name, group_name=None):
        if not group_name:
            return self.get(name=name)
        return self.get(name=name, activity_field_group__name=group_name)


class ActivityField(models.Model):
    name = models.CharField("nom", max_length=255)
    activity_field_group = models.ForeignKey(
        ActivityFieldGroup,
        on_delete=models.SET_NULL,
        related_name="activity_fields",
        related_query_name="activity_field",
        blank=True,
        null=True,
        verbose_name="groupe de champs d'activité",
    )

    objects = ActivityFieldManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "activity_field_group",
                name="unique_activity_field_name",
                violation_error_code="unique_name",
                violation_error_message=(
                    "Un champ d'activité avec ce nom existe déjà dans ce "
                    "groupe."
                ),
            ),
        ]
        verbose_name = "champ d'activité"
        verbose_name_plural = "champs d'activité"

    def __str__(self):
        return self.name

    def natural_key(self):
        if not hasattr(self, "activity_field_group"):
            return (self.name,)
        return (self.name, self.activity_field_group.name)


class AssociationQuerySet(models.QuerySet):
    def get_by_natural_key(self, name):
        return self.get(name=name)

    def active(self):
        return self.filter(is_active=True)

    def with_active_member(self, user):
        return self.filter(
            membership__user=user,
            membership__is_active=True,
        )

    def without_migration(self):
        return self.filter(migration__isnull=True)


@reversion.register()
class Association(models.Model):
    name = models.CharField(max_length=127, verbose_name="nom")
    description = models.TextField(blank=True, verbose_name="description")

    website_url = models.URLField(
        blank=True,
        verbose_name="adresse du site web",
    )

    activity_field = models.ForeignKey(
        ActivityField,
        on_delete=models.SET_NULL,
        related_name="associations",
        related_query_name="association",
        blank=True,
        null=True,
        verbose_name="champ d'activité",
    )

    logo = models.ImageField(
        upload_to=upload_logo_to,
        blank=True,
        null=True,
        verbose_name="logo",
    )

    is_hidden = models.BooleanField(
        default=False,
        verbose_name="cachée",
        help_text=(
            "L'association n'apparaitra pas dans la liste, il faudra connaître "
            "son URL pour la rejoindre."
        ),
    )
    moderate_membership = models.BooleanField(
        default=False,
        verbose_name="modérer l'inscription des bénévoles",
        help_text=(
            "Une modération est nécessaire avant qu'un⋅e utilisateur⋅rice "
            "ne devienne membre de l'association."
        ),
    )
    moderate_benevalo = models.BooleanField(
        default=False,
        verbose_name="modérer la saisie des actions de bénévolats",
        help_text=(
            "Une modération est nécessaire avant qu'un⋅e bénévole "
            "n'enregistre du bénévolat pour l'association."
        ),
    )

    country = CountryField(
        blank=True,
        default="FR",
        verbose_name="pays",
    )
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="code postal",
    )
    has_employees = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="a au moins un·e salarié·e",
    )
    income = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="revenus moyens annuels (en euros)",
    )

    is_active = models.BooleanField(
        default=is_registration_opened,
        editable=False,
        verbose_name="validée",
    )

    members = models.ManyToManyField(
        "accounts.User",
        related_name="associations",
        related_query_name="association",
        through="AssociationMembership",
    )

    objects = AssociationQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_association_name",
                violation_error_code="unique_name",
                violation_error_message=(
                    "Une association avec ce nom existe déjà."
                ),
            ),
        ]
        verbose_name = "association"
        verbose_name_plural = "associations"

    def __str__(self):
        return self.name

    def save(self, *args, create_initial_data=True, **kwargs):
        if not self._state.adding:
            create_initial_data = False
        super().save(*args, **kwargs)

        if create_initial_data:
            AssociationBenevaloCategory.objects.bulk_create(
                AssociationBenevaloCategory(association_id=self.pk, **obj_dict)
                for obj_dict in DefaultBenevaloCategory.objects.values(
                    *{f.name for f in BaseBenevaloCategory._meta.fields},
                    default_category_id=F("id"),
                )
            )

            AssociationBenevaloLevel.objects.bulk_create(
                AssociationBenevaloCategory(association_id=self.pk, **obj_dict)
                for obj_dict in DefaultBenevaloLevel.objects.values(
                    *{f.name for f in BaseBenevaloLevel._meta.fields},
                )
            )

            AssociationRole.objects.bulk_create(
                AssociationRole(association_id=self.pk, **obj_dict)
                for obj_dict in DefaultRole.objects.values(
                    *{f.name for f in BaseRole._meta.fields},
                )
            )

    def natural_key(self):
        return (self.name,)

    @cached_property
    def has_migration(self):
        """
        Détermine si l'association est en cours de migration ou a été migrée
        vers une autre instance.
        """
        return AssociationMigration.objects.filter(association=self).exists()

    def has_member(self, user):
        """
        Détermine si l'utilisateur⋅rice donné est un membre actif de
        l'association.
        """
        if user.is_anonymous_member:
            return user.association == self
        return (
            user.is_authenticated
            and self.memberships.active().filter(user=user).exists()
        )


class AssociationMigration(models.Model):  # noqa: DJ008
    association = models.OneToOneField(
        Association,
        on_delete=models.CASCADE,
        related_name="migration",
        primary_key=True,
    )
    message = models.TextField(
        blank=True,
        verbose_name="message",
        help_text=(
            "Ce message sera présenté sur la page de l'association pendant et "
            "après la migration."
        ),
    )

    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
    )
    created_at = models.DateField(auto_now_add=True)
    done_at = models.DateField(null=True)

    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_done = models.BooleanField(default=False, editable=False)
    destination_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "migration d'association"
        verbose_name_plural = "migrations d'associations"


class AssociationProjectManager(models.Manager):
    def get_by_natural_key(self, name, association_name):
        return self.get(name=name, association__name=association_name)


@reversion.register()
class AssociationProject(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="nom",
    )
    description = models.TextField(
        blank=True,
        verbose_name="description",
    )

    association = models.ForeignKey(
        Association,
        on_delete=models.CASCADE,
        related_name="projects",
        related_query_name="project",
        verbose_name="association",
    )

    objects = AssociationProjectManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "association",
                name="unique_association_project_name",
                violation_error_code="unique_name",
                violation_error_message="Un projet avec ce nom existe déjà.",
            ),
        ]
        verbose_name = "projet"
        verbose_name_plural = "projets"

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name, self.association.name)

    natural_key.dependencies = ["associations.association"]


class AssociationBenevaloLevelManager(models.Manager):
    def get_by_natural_key(self, name, association_name):
        return self.get(name=name, association__name=association_name)


@reversion.register()
class AssociationBenevaloLevel(BaseBenevaloLevel):
    association = models.ForeignKey(
        Association,
        on_delete=models.CASCADE,
        related_name="benevalo_levels",
        related_query_name="benevalo_level",
        verbose_name="association",
    )

    objects = AssociationBenevaloLevelManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "association",
                name="unique_association_benevalo_level_name",
                violation_error_code="unique_name",
                violation_error_message=(
                    "Un niveau de bénévolat avec ce nom existe déjà."
                ),
            ),
        ]
        verbose_name = "niveau de bénévolat"
        verbose_name_plural = "niveaux de bénévolat"

    def natural_key(self):
        return (self.name, self.association.name)

    natural_key.dependencies = ["associations.association"]


class AssociationBenevaloCategoryManager(models.Manager):
    def get_by_natural_key(self, name, association_name):
        return self.get(name=name, association__name=association_name)


@reversion.register()
class AssociationBenevaloCategory(BaseBenevaloCategory):
    association = models.ForeignKey(
        Association,
        on_delete=models.CASCADE,
        related_name="benevalo_categories",
        related_query_name="benevalo_category",
        verbose_name="association",
    )

    default_category = models.ForeignKey(
        DefaultBenevaloCategory,
        on_delete=models.PROTECT,
        related_name="association_categories",
        related_query_name="association_category",
        verbose_name="catégorie rattachée",
        help_text=(
            "Ces catégories sont celles proposées par défaut et permettent "
            "d'avoir une base commune pour toutes les associations. Si vous "
            "êtes amené⋅es à adapter certaines de ces catégories pour votre "
            "association, veuillez sélectionner celle dont elle se rattache."
        ),
    )

    objects = AssociationBenevaloCategoryManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "association",
                name="unique_association_benevalo_category_name",
                violation_error_code="unique_name",
                violation_error_message=(
                    "Une catégorie de bénévolat avec ce nom existe déjà."
                ),
            ),
        ]
        verbose_name = "catégorie de bénévolat"
        verbose_name_plural = "catégories de bénévolat"

    def natural_key(self):
        return (self.name, self.association.name)

    natural_key.dependencies = ["associations.association"]


class AssociationRoleManager(BaseRoleManager):
    def get_by_natural_key(self, name, association_name):
        return self.get(name=name, association__name=association_name)

    def get_for_user(self, user, association_id):
        """
        Retourne le rôle de l'utilisateur⋅rice au sein de l'association donnés,
        ou `None` si aucun n'est défini. Tous les rôles de l'utilisateur⋅rice
        sont récupérés et mis en cache au premier appel de cette méthode.
        """
        if not user.is_authenticated:
            return None
        if not hasattr(user, "_roles"):
            user._roles = {
                role.association_id: role
                for role in self.filter(
                    membership__is_active=True,
                    membership__user=user,
                    # On s'assure ici de la bonne consistance entre les modèles,
                    # même si à priori il n'est pas possible que l'association
                    # d'un rôle change en cours de route
                    membership__association=F("association"),
                )
            }
        return user._roles.get(association_id, None)


@reversion.register()
class AssociationRole(BaseRole):
    association = models.ForeignKey(
        Association,
        on_delete=models.CASCADE,
        related_name="roles",
        related_query_name="role",
        verbose_name="association",
    )

    objects = AssociationRoleManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "association",
                name="unique_association_role_name",
                violation_error_code="unique_name",
                violation_error_message="Un rôle avec ce nom existe déjà.",
            ),
            models.UniqueConstraint(
                fields=["association"],
                condition=Q(is_default=True),
                name="unique_association_role_default",
                violation_error_code="unique_default",
                violation_error_message=(
                    "Il ne peut y avoir qu'un rôle par défaut pour "
                    "l'association."
                ),
            ),
        ]
        verbose_name = "rôle"
        verbose_name_plural = "rôles"

    def natural_key(self):
        return (self.name, self.association.name)

    natural_key.dependencies = ["associations.association"]

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)

        errors = {}

        if not self.is_default:
            try:
                default = AssociationRole.objects.default().get(
                    association=self.association
                )
            except AssociationRole.DoesNotExist:
                errors["is_default"] = (
                    "Veuillez définir un rôle par défaut pour l'association."
                )
            else:
                if self.pk == default.pk:
                    errors["is_default"] = (
                        "Veuillez garder un rôle par défaut pour l'association."
                    )

        if self.pk is not None and not self.manage_association:
            try:
                management = AssociationRole.objects.get(
                    association=self.association,
                    manage_association=True,
                    membership__is_active=True,
                )
            except AssociationRole.DoesNotExist:
                # Aucun rôle de gestion attribué à au moins un membre existe, on
                # laisse passer l'erreur qui devrait être reportée autre part.
                pass
            except AssociationRole.MultipleObjectsReturned:
                pass
            else:
                if self.pk == management.pk:
                    errors["manage_association"] = (
                        "Ce rôle est actuellement le seul attribué à un membre "
                        "avec cette permission. Pour vous éviter de perdre la "
                        "gestion de votre association, elle ne peut être "
                        "retirée en l'état."
                    )

        if errors:
            raise ValidationError(errors)


class AssociationMembershipQuerySet(models.QuerySet):
    def get_by_natural_key(self, user_email, association_name):
        return self.get(
            user__email=user_email,
            association__name=association_name,
        )

    def active(self):
        return self.filter(is_active=True)

    def management_role(self):
        """
        Restreins les objets avec ceux dont le rôle permet la gestion de
        l'association.
        """
        return self.filter(role__manage_association=True)

    def order_by_user_full_name(self, is_descending=False):
        return self.annotate(
            user_full_name=Concat(
                "user__first_name",
                "user__last_name",
                "user__pseudo",
            )
        ).order_by("-user_full_name" if is_descending else "user_full_name")


@reversion.register()
class AssociationMembership(models.Model):
    """
    Relation intermédiaire pour caractériser le rôle d'un membre dans une
    association.
    """

    association = models.ForeignKey(
        Association,
        on_delete=models.CASCADE,
        related_name="memberships",
        related_query_name="membership",
        verbose_name="association",
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="memberships",
        related_query_name="membership",
        verbose_name="bénévole",
    )
    role = models.ForeignKey(
        AssociationRole,
        on_delete=models.RESTRICT,
        related_name="memberships",
        related_query_name="membership",
        verbose_name="rôle",
    )

    is_active = models.BooleanField(
        default=True,
        editable=False,
        verbose_name="validé",
    )

    objects = AssociationMembershipQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["association", "user"],
                name="unique_association_membership",
            ),
        ]
        verbose_name = "membre d'association"
        verbose_name_plural = "membres d'associations"

    def __str__(self):
        return "%s – %s (%s)" % (self.user, self.association, self.role)

    def natural_key(self):
        return (self.user.email, self.association.name)

    natural_key.dependencies = ["accounts.user", "associations.association"]

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)

        errors = {}

        if self.pk is not None and not self.role.manage_association:
            try:
                manager = (
                    AssociationMembership.objects.active()
                    .management_role()
                    .get(association=self.association)
                )
            except AssociationMembership.DoesNotExist:
                # Aucun membre actif n'a d'attribué le rôle de gestion, on
                # laisse passer l'erreur qui devrait être reportée autre part.
                pass
            except AssociationMembership.MultipleObjectsReturned:
                pass
            else:
                if self.pk == manager.pk:
                    errors["role"] = (
                        "Ce membre est actuellement le seul à avoir le rôle "
                        "« %s », donnant la permission de gérer l'association. "
                        "Veuillez d'abord attribuer ce rôle à un autre membre "
                        "pour vous éviter de perdre la gestion de votre "
                        "association."
                    ) % manager.role

        if errors:
            raise ValidationError(errors)

    def delete(self):
        if (
            self.is_active
            and self.role.manage_association
            and not (
                AssociationMembership.objects.active()
                .management_role()
                .filter(association=self.association)
                .exclude(pk=self.pk)
                .exists()
            )
        ):
            raise IntegrityError(
                "Ce membre est actuellement le seul à avoir la permission de "
                "gérer l'association, par le rôle « %s ». Veuillez d'abord "
                "attribuer un tel rôle à un autre membre pour vous éviter de "
                "perdre la gestion de votre association." % self.role
            )

        return super().delete()


class AssociationAnonymousMemberQuerySet(models.QuerySet):
    def get_by_natural_key(self, uuid, association_name):
        return self.get(uuid=uuid, association__name=association_name)

    def active(self):
        return self.filter(
            Q(expiration_date__isnull=True)
            | Q(expiration_date__gt=timezone.now()),
            is_active=True,
        )


@reversion.register()
class AssociationAnonymousMember(models.Model, AnonymousUser):
    association = models.ForeignKey(
        Association,
        on_delete=models.CASCADE,
        related_name="anonymous_members",
        related_query_name="anonymous_member",
        verbose_name="association",
    )
    uuid = models.UUIDField(default=uuid.uuid4)

    name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="nom",
    )

    expiration_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="date d'expiration",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="actif",
        help_text=(
            "Détermine si l'accès de ce membre anonyme est actif, dans le cas "
            "où il n'a pas encore expiré."
        ),
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="créé le",
    )
    last_visit = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="dernière visite",
    )

    objects = AssociationAnonymousMemberQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["association", "uuid"],
                name="unique_association_member_uuid",
            ),
        ]
        verbose_name = "membre anonyme"
        verbose_name_plural = "membres anonymes"

    def __str__(self):
        return self.name or "Membre anonyme #%d" % self.pk

    def get_absolute_url(self):
        return "%s%s?%s=%s" % (
            settings.BASE_URL,
            reverse("dashboard"),
            ANONYMOUS_MEMBER_QUERY_KEY,
            self.uuid,
        )

    def natural_key(self):
        return (self.uuid, self.association.name)

    @property
    def is_anonymous_member(self):
        return True
