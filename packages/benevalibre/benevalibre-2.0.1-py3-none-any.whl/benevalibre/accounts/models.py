from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.db.models.functions import Concat
from django.utils import timezone

from dynamic_filenames import FilePattern

upload_avatar_to = FilePattern(filename_pattern="avatars/{uuid:x}{ext}")


class Theme(models.TextChoices):
    LIGHT = "light", "Clair"
    DARK = "dark", "Sombre"

    __empty__ = "Automatique"


class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def order_by_full_name(self, is_descending=False):
        return self.annotate(
            full_name=Concat(
                "first_name",
                "last_name",
                "pseudo",
            )
        ).order_by("-full_name" if is_descending else "full_name")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    @classmethod
    def normalize_email(cls, email):
        """
        Normalise l'adresse mail en supprimant les espaces et en la mettant
        en minuscules.
        """
        return email.strip().lower() if email else ""

    def _create_user(self, email, password, **extra_fields):
        """
        Crée et enregistre un compte utilisateur avec l'adresse mail et le
        mot de passe donnés.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_superuser") is not True:  # pragma: no cover
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        "adresse mail",
        unique=True,
        error_messages={
            "unique": "Un compte avec cette adresse mail existe déjà."
        },
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="prénom",
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="nom",
    )
    pseudo = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="pseudo",
    )

    avatar = models.ImageField(
        upload_to=upload_avatar_to,
        blank=True,
        null=True,
        verbose_name="avatar",
    )

    theme = models.CharField(
        max_length=5,
        choices=Theme,
        blank=True,
        verbose_name="thème",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="actif",
        help_text=(
            "Détermine si le compte utilisat⋅eur⋅rice doit être considéré "
            "comme actif dans l'application. Vous pouvez le désactiver plutôt "
            "que de le supprimer."
        ),
    )

    date_joined = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name="date d'inscription",
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "compte utilisateur⋅rice"
        verbose_name_plural = "comptes utilisateur⋅rices"

    def __str__(self):
        return self.get_full_name() or self.email

    def clean(self):
        super().clean()

        if not any([self.first_name, self.last_name, self.pseudo]):
            raise ValidationError(
                "Au moins le prénom, le nom ou le pseudo est requis.",
                code="name_required",
            )

        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def is_staff(self):
        # Détermine si le compte a accès à l'administration de Django, qu'on
        # vise à ne pas utiliser dans l'application.
        return self.is_superuser

    def get_full_name(self):
        """Retourne le prénom et le nom de la personne, et/ou son pseudo."""
        if not self.first_name and not self.last_name:
            return self.pseudo
        full_name = ("%s %s" % (self.first_name, self.last_name)).strip()
        return (
            full_name
            if not self.pseudo
            else "%s (%s)" % (full_name, self.pseudo)
        )

    def get_short_name(self):
        """Retourne le prénom, le nom ou le pseudo de la personne."""
        return self.first_name or self.last_name or self.pseudo

    def get_initials(self):
        """
        Retourne les initiales de la personne, à afficher à la place de l'avatar
        s'il n'est pas défini notamment.
        """
        if self.first_name and self.last_name:
            return "%s%s" % (self.first_name[0], self.last_name[0])
        return str(self.get_short_name() or self.email)[:2]

    def get_avatar_hsl_color(self):
        """
        Retourne une couleur au format HSL fixe pour ce compte, à utiliser comme
        couleur de fond à la place de l'avatar s'il n'est pas défini notamment.
        """
        return "%d 75%% 65%%" % (self.date_joined.microsecond % 360)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Envoi un courriel à cette personne."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
