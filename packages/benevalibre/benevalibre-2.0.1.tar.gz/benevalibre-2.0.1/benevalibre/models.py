import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.functions import Concat
from django.utils import timezone
from django.utils.formats import date_format

import reversion

from benevalibre.validators import FileTypeValidator


class BenevaloQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def order_by_user_full_name(self, is_descending=False):
        return self.annotate(
            user_full_name=Concat(
                "user__first_name",
                "user__last_name",
                "user__pseudo",
            )
        ).order_by("-user_full_name" if is_descending else "user_full_name")


@reversion.register()
class Benevalo(models.Model):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        related_name="benevalos",
        related_query_name="benevalo",
        blank=True,
        null=True,
        verbose_name="utilisateur⋅rice",
    )
    anonymous_member = models.ForeignKey(
        "associations.AssociationAnonymousMember",
        on_delete=models.SET_NULL,
        related_name="benevalos",
        related_query_name="benevalo",
        blank=True,
        null=True,
        verbose_name="membre anonyme",
    )
    association = models.ForeignKey(
        "associations.Association",
        on_delete=models.CASCADE,
        related_name="benevalos",
        related_query_name="benevalo",
        null=True,
        verbose_name="association",
    )

    project = models.ForeignKey(
        "associations.AssociationProject",
        on_delete=models.SET_NULL,
        related_name="benevalos",
        related_query_name="benevalo",
        blank=True,
        null=True,
        verbose_name="projet",
    )
    level = models.ForeignKey(
        "associations.AssociationBenevaloLevel",
        on_delete=models.SET_NULL,
        related_name="benevalos",
        related_query_name="benevalo",
        blank=True,
        null=True,
        verbose_name="niveau",
    )
    category = models.ForeignKey(
        "associations.AssociationBenevaloCategory",
        on_delete=models.RESTRICT,
        related_name="benevalos",
        related_query_name="benevalo",
        null=True,
        verbose_name="catégorie",
    )

    date = models.DateField(
        default=datetime.date.today,
        validators=[
            MinValueValidator(
                datetime.date(2000, 1, 1),
                message="Veuillez choisir une date à partir du 01/01/2000.",
            ),
            MaxValueValidator(
                datetime.date.today,
                message="Veuillez choisir une date antérieure à demain.",
            ),
        ],
        verbose_name="date",
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="date de fin",
        help_text="Dans le cas où cette action se passe sur plusieurs jours.",
    )

    title = models.CharField(
        max_length=127,
        verbose_name="titre",
        help_text="Une courte description de cette action.",
    )
    description = models.TextField(blank=True, verbose_name="description")

    distance = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name="distance (en km)",
        help_text="La distance parcourue lors de cette action.",
    )
    duration = models.DurationField(
        verbose_name="durée",
        help_text="Le temps consacré à cette action.",
    )

    is_active = models.BooleanField(
        default=True,
        editable=False,
        verbose_name="validée",
    )

    objects = BenevaloQuerySet.as_manager()

    class Meta:
        verbose_name = "action de bénévolat"
        verbose_name_plural = "actions de bénévolat"

    def __str__(self):
        return self.title

    @property
    def author(self):
        return self.user or self.anonymous_member

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)

        errors = {}

        if self.end_date and self.end_date <= self.date:
            errors["end_date"] = ValidationError(
                "Cette date doit être après le %(date)s.",
                params={"date": date_format(self.date, "SHORT_DATE_FORMAT")},
                code="after_date",
            )

        if self.duration is not None and not (self.duration or self.distance):
            errors["distance"] = ValidationError(
                "Ce champ est requis si la durée est nulle.",
                code="required_without_duration",
            )

        if errors:
            raise ValidationError(errors)


class InstanceSettingsManager(models.Manager):
    def get_current(self):
        """Retourne l'objet actuel pour l'instance ou le crée."""
        # FIXME: On prend jusque là le dernier objet créé en base, hérité
        # de la façon dont était codé TermsOfUse que InstanceSettings vient
        # remplacer. Ce comportement pourra à terme évoluer ici sans
        # impacter le reste du code, tant qu'on passe par cette méthode
        # pour récupérer le bon objet.
        return self.last() or self.create()


class InstanceSettings(models.Model):
    site_name = models.CharField(
        max_length=150,
        default="Bénévalibre",
        verbose_name="nom de l'instance",
        help_text=(
            "Ce nom est notamment utilisé dans les courriels envoyés par "
            "l'application, ainsi que dans l'en-tête des pages."
        ),
    )
    terms_of_use_file = models.FileField(
        upload_to="terms",
        blank=True,
        null=True,
        validators=[
            FileTypeValidator(
                allowed_types=["application/pdf"],
                message="Veuillez choisir un fichier PDF valide.",
            ),
        ],
        verbose_name="charte d'utilisation",
    )

    objects = InstanceSettingsManager()

    class Meta:
        verbose_name = "paramètres de l'instance"

    def __str__(self):
        return self.site_name

    @staticmethod
    def for_request(request):
        """
        Retourne les paramètres de l'instance pour la requête donnée, soit
        en cache si l'objet approprié a déjà été récupéré, soit en base ou
        depuis un nouvel objet.
        """
        if not hasattr(request, "_instance_settings"):
            instance_settings = InstanceSettings.objects.get_current()
            setattr(request, "_instance_settings", instance_settings)
        return request._instance_settings


class AnnouncementQuerySet(models.QuerySet):
    def active(self):
        now = timezone.now()
        return self.filter(
            Q(expiration_date__isnull=True) | Q(expiration_date__gt=now),
            publication_date__lte=now,
        )

    def active_for_user(self, user):
        queryset = self.active()
        if (
            not user.is_authenticated
            or not user.memberships.active().management_role().exists()
        ):
            queryset = queryset.exclude(target=self.model.Target.MANAGERS)
        return queryset


class Announcement(models.Model):
    class Target(models.TextChoices):
        ALL = "ALL", "Tout le monde"
        MANAGERS = "MNG", "Les responsables d'association"

    title = models.CharField(max_length=200, verbose_name="titre")
    content = models.TextField(blank=True, verbose_name="contenu")

    target = models.CharField(
        max_length=3,
        choices=Target,
        default=Target.ALL,
        verbose_name="cible",
    )

    publication_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="date de publication",
    )
    expiration_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="date d'expiration",
    )

    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="auteur·e",
    )

    objects = AnnouncementQuerySet.as_manager()

    class Meta:
        verbose_name = "annonce"
        verbose_name_plural = "annonces"

    def __str__(self):
        return self.title

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)

        if (
            self.expiration_date
            and self.expiration_date <= self.publication_date
        ):
            raise ValidationError(
                {
                    "expiration_date": ValidationError(
                        "Cette date doit être après la date de publication.",
                        code="after_publication_date",
                    ),
                }
            )
