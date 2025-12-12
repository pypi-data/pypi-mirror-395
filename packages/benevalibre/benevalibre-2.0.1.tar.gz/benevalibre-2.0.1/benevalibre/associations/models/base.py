from django.db import models


class BaseBenevaloCategory(models.Model):
    """
    Modèle de base abstrait pour les catégories d'actions de bénévolat.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="nom",
    )
    description = models.TextField(
        blank=True,
        verbose_name="description",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseBenevaloLevel(models.Model):
    """
    Modèle de base abstrait pour les niveaux d'actions de bénévolat.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="nom",
    )
    description = models.TextField(
        blank=True,
        verbose_name="description",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseRoleManager(models.Manager):
    def default(self):
        return self.filter(is_default=True)


class BaseRole(models.Model):
    """
    Modèle de base abstrait pour les rôles, qui permettent de définir les
    groupes de permissions.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="nom",
    )
    description = models.TextField(
        blank=True,
        verbose_name="description",
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name="par défaut",
        help_text=(
            "Ce rôle sera attribué automatiquement à chaque nouveau membre."
        ),
    )

    list_members = models.BooleanField(
        default=False,
        verbose_name="lister les membres",
    )
    manage_members = models.BooleanField(
        default=False,
        verbose_name="gérer les membres",
    )
    manage_benevalos = models.BooleanField(
        default=False,
        verbose_name="gérer les actions de bénévolat",
    )
    manage_benevalo_categories = models.BooleanField(
        default=False,
        verbose_name="gérer les catégories de bénévolat",
    )
    manage_benevalo_levels = models.BooleanField(
        default=False,
        verbose_name="gérer les niveaux de bénévolat",
    )
    manage_projects = models.BooleanField(
        default=False,
        verbose_name="gérer les projets",
    )
    manage_roles = models.BooleanField(
        default=False,
        verbose_name="gérer les rôles",
    )
    manage_association = models.BooleanField(
        default=False,
        verbose_name="gérer l'association",
        help_text=(
            "Cette permission donne à un membre tous les droits de gestion "
            "de l'association, entraînant de fait toutes les autres."
        ),
    )

    objects = BaseRoleManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
