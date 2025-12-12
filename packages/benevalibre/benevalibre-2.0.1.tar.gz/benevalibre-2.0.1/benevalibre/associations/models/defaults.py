from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower

from .base import BaseBenevaloCategory, BaseBenevaloLevel, BaseRole


class AssociationBenevaloCategoryManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class DefaultBenevaloCategory(BaseBenevaloCategory):
    objects = AssociationBenevaloCategoryManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_default_benevalo_category_name",
                violation_error_code="unique_name",
                violation_error_message=(
                    "Une catégorie de bénévolat avec ce nom existe déjà."
                ),
            ),
        ]
        verbose_name = "catégorie de bénévolat par défaut"
        verbose_name_plural = "catégories de bénévolat par défaut"

    def natural_key(self):
        return (self.name,)


class DefaultBenevaloLevel(BaseBenevaloLevel):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_default_benevalo_level_name",
                violation_error_code="unique_name",
                violation_error_message=(
                    "Un niveau de bénévolat avec ce nom existe déjà."
                ),
            ),
        ]
        verbose_name = "niveau de bénévolat par défaut"
        verbose_name_plural = "niveaux de bénévolat par défaut"


class DefaultRole(BaseRole):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_default_role_name",
                violation_error_code="unique_name",
                violation_error_message="Un rôle avec ce nom existe déjà.",
            ),
        ]
        verbose_name = "rôle par défaut"
        verbose_name_plural = "rôles par défaut"

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)

        errors = {}

        try:
            default = DefaultRole.objects.default().get()
        except DefaultRole.DoesNotExist:
            if not self.is_default:
                errors["is_default"] = "Veuillez définir un rôle par défaut."
        else:
            if self.pk == default.pk:
                if not self.is_default:
                    errors["is_default"] = "Veuillez garder un rôle par défaut."
            elif self.is_default:
                errors["is_default"] = (
                    "Le rôle « %(role)s » est déjà celui par défaut, il ne "
                    "peut y en avoir qu'un." % {"role": default}
                )

        if errors:
            raise ValidationError(errors)
