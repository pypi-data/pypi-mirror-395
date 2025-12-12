import datetime
import logging

from django.core import serializers
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.urls import reverse
from django.utils import timezone

import requests
from packaging.version import Version
from pydantic import UUID4, BaseModel, field_validator
from requests.exceptions import RequestException

from benevalibre import __version__
from benevalibre.accounts.models import User
from benevalibre.associations.models import (
    Association,
    AssociationAnonymousMember,
    AssociationBenevaloCategory,
    AssociationBenevaloLevel,
    AssociationMembership,
    AssociationProject,
    AssociationRole,
)
from benevalibre.models import Benevalo
from benevalibre.utils import get_absolute_uri
from benevalibre.utils.types import HttpUrl

logger = logging.getLogger("benevalibre.associations")

current_version = Version(__version__)


class MigrationImportError(Exception):
    pass


class MigrationMetadata(BaseModel):
    app_version: str
    date: datetime.datetime
    endpoint: HttpUrl
    token: UUID4

    @field_validator("app_version", mode="after")
    @classmethod
    def validate_app_version(cls, value: str) -> Version:
        return Version(value)

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value: str) -> datetime.datetime:
        date = datetime.datetime.fromisoformat(value)

        if date > timezone.now():
            raise ValueError("date is in the future")

        return date


def export_association_data(migration):
    """
    Sérialise les données de l'association correspondant à la migration donnée
    et les retourne sous forme d'un dictionnaire prêt à être encodé en JSON.
    """
    association = migration.association

    # Le logo n'est pas exporté
    association.logo = None

    return {
        "objects": (
            serializers.serialize(
                "python",
                association.members.all(),
                fields=["first_name", "last_name", "pseudo", "email"],
                use_natural_primary_keys=True,
            )
            + serializers.serialize(
                "python",
                [
                    association,
                    *association.benevalo_categories.all(),
                    *association.benevalo_levels.all(),
                    *association.projects.all(),
                    *association.roles.all(),
                    *association.memberships.all(),
                    *association.anonymous_members.all(),
                    *association.benevalos.all(),
                ],
                use_natural_foreign_keys=True,
                use_natural_primary_keys=True,
            )
        ),
        "metadata": {
            "app_version": __version__,
            "date": timezone.now().isoformat(timespec="seconds"),
            "endpoint": get_absolute_uri(
                reverse("api:association_migrate", args=(association.pk,))
            ),
            "token": migration.token,
        },
    }


def import_association_data(data):
    """
    Tente d'importer les données de l'association depuis le dictionnaire donné
    après avoir validé son format. En cas de réussite, l'instance d'origine en
    est informée afin de terminer la migration, et un 2-tuple avec l'association
    et les comptes créés est retourné.
    """
    if "benevalibre_version" in data:
        raise MigrationImportError(
            "Cette instance ne prends pas en charge la version de "
            "l'application à l'origine de ce fichier (%s / version "
            "requise : %d.%d.x)."
            % (
                data["benevalibre_version"],
                current_version.major,
                current_version.minor,
            )
        )
    elif (
        not isinstance(data, dict)
        or data.keys() != {"objects", "metadata"}
        or not isinstance(data["objects"], list)
        or not isinstance(data["metadata"], dict)
    ):
        raise ValueError("Le contenu du fichier est incomplet ou inattendu.")

    validate_metadata(data["metadata"])
    check_migration_status(data["metadata"]["endpoint"])

    association, new_users = deserialize_and_save_objects(data["objects"])

    complete_migration(association, data["metadata"])

    return (association, new_users)


# IMPORT STEPS
# ------------------------------------------------------------------------------


def validate_metadata(metadata):
    try:
        metadata = MigrationMetadata(**metadata)
    except ValueError as e:
        logger.error("Unable to validate migration metadata : %s", str(e))
        raise ValueError("Le contenu du fichier est incomplet ou inattendu.")

    if (
        metadata.app_version.major != current_version.major
        or metadata.app_version.minor != current_version.minor
    ):
        raise MigrationImportError(
            "Cette instance ne prends pas en charge la version de "
            "l'application à l'origine de ce fichier (%s / version "
            "requise : %d.%d.x)."
            % (
                metadata.app_version,
                current_version.major,
                current_version.minor,
            )
        )

    if metadata.endpoint.scheme != "https":
        raise MigrationImportError(
            "La communication avec l'instance d'origine doit se faire en HTTPS."
        )


def check_migration_status(endpoint):
    try:
        response = requests.get(endpoint)
    except RequestException:
        logger.exception(
            "Unable to fetch migration status from endpoint %s",
            endpoint,
        )
        raise MigrationImportError(
            "Une erreur est survenue lors de la communication avec l'instance "
            "d'origine. Veuillez vérifier qu'elle est toujours opérationnelle "
            "et qu'elle n'a pas changé d'adresse."
        )
    else:
        if response.status_code != 200:
            logger.error(
                "%d Error (%s) while fetching migration status at %s",
                response.status_code,
                response.reason,
                response.url,
            )
            if response.status_code == 404:
                raise MigrationImportError(
                    "L'association n'est pas ou plus à l'état de migration sur "
                    "l'instance d'origine, ou a été supprimée."
                )
            raise MigrationImportError(
                "Une erreur inattendue est survenue lors de la communication "
                "avec l'instance d'origine."
            )

    try:
        data = response.json()
    except RequestException:
        logger.exception(
            "Unable to parse JSON response from migration status at %s",
            response.url,
        )
        raise MigrationImportError(
            "Une erreur inattendue est survenue lors de la communication "
            "avec l'instance d'origine."
        )
    else:
        if data["is_done"]:
            raise MigrationImportError(
                "La migration de l'association est déjà terminée sur "
                "l'instance d'origine."
            )


def deserialize_and_save_objects(objects):
    association = None
    new_users = set()

    for deserialized_obj in serializers.deserialize(
        "python", objects, handle_forward_references=True
    ):
        obj = deserialized_obj.object
        model_class = obj._meta.model

        if model_class == User:
            if obj.pk is not None:
                continue

            obj.is_active = False
            obj.set_unusable_password()

        elif model_class == Association:
            if association is not None:
                logger.error("Multiple association objects found at import")
                raise ValueError("Le contenu du fichier semble corrompu.")

            if obj.pk is not None:
                raise MigrationImportError(
                    "Une association avec le nom « %s » existe déjà." % obj.name
                )

        elif model_class in (
            AssociationBenevaloCategory,
            AssociationBenevaloLevel,
            AssociationProject,
            AssociationRole,
            AssociationMembership,
            AssociationAnonymousMember,
            Benevalo,
        ):
            if obj.association != association:
                logger.error(
                    "%r is not for the right association (%s != %s)",
                    obj,
                    obj.association.name,
                    association.name,
                )
                raise ValueError("Le contenu du fichier semble corrompu.")

            if model_class == Benevalo:
                # Ce modèle n'a pas de clé naturelle, la clé primaire de l'objet
                # sur l'instance d'origine sera donc incluse. Vu qu'il n'est pas
                # possible de vérifier s'il existe déjà, on en crée un nouveau.
                obj.pk = None
            elif obj.pk is not None:
                logger.error(
                    "%r exists before import or provides an unexpected 'pk'",
                    obj,
                )
                raise ValueError("Le contenu du fichier semble corrompu.")

        else:
            logger.error("Unexpected model to import %r", obj)
            raise ValueError("Le contenu du fichier semble corrompu.")

        # Vérifie que toutes les relation ont pu être résolues, ce qui devrait
        # toujours être le cas étant donné l'ordre des objets du fichier
        if deserialized_obj.deferred_fields:
            if (
                model_class == AssociationBenevaloCategory
                and len(deserialized_obj.deferred_fields) == 1
                and list(deserialized_obj.deferred_fields.keys())[0].name
                == "default_category"
            ):
                default_category_name = list(
                    deserialized_obj.deferred_fields.values()
                )[0][0]
                logger.error(
                    "Unable to find DefaultBenevaloCategory with name='%s'",
                    default_category_name,
                )
                raise MigrationImportError(
                    "La catégorie de bénévolat par défaut « %s » définis par "
                    "« %s » n'existe pas sur cette instance."
                    % (default_category_name, obj.name)
                )

            logger.error(
                "Unexpected deferred fields for %r at import: %s",
                obj,
                {
                    k.name: v
                    for k, v in deserialized_obj.deferred_fields.items()
                },
            )
            raise ValueError("Le contenu du fichier semble corrompu.")

        try:
            deserialized_obj.object.full_clean()
        except ValidationError as e:
            if (
                model_class == Association
                and hasattr(e, "error_dict")
                and NON_FIELD_ERRORS in e.error_dict
                and e.error_dict[NON_FIELD_ERRORS][0].code == "unique_name"
            ):
                raise MigrationImportError(
                    "Une association avec le nom « %s » existe déjà." % obj.name
                )
            # L'objet n'est pas valide, ce qui pourrait arriver dans de rares
            # cas où les contraintes ont évolué après la création de l'objet
            logger.exception(
                "Unable to clean deserialized object %r for import", obj
            )
            raise MigrationImportError(
                "L'objet « %s » de type '%s' n'est pas valide. Veuillez le "
                "vérifier sur l'instance d'origine en l'enregistrant à nouveau."
                % (obj, obj._meta.verbose_name)
            )
        else:
            deserialized_obj.save()

        if model_class == User:
            new_users.add(User.objects.get(email=obj.email))
        elif model_class == Association:
            association = Association.objects.get(name=obj.name)

    return (association, new_users)


def complete_migration(association, metadata):
    try:
        requests.post(
            metadata["endpoint"],
            data={
                "token": metadata["token"],
                "destination_url": get_absolute_uri(
                    reverse("associations:detail", args=(association.pk,))
                ),
            },
        ).raise_for_status()
    except RequestException:
        logger.exception(
            "Unable to call migration endpoint for '%s' at %s",
            association,
            metadata["endpoint"],
        )
        raise MigrationImportError(
            "Une erreur est survenue lors de la communication avec l'instance "
            "d'origine. Veuillez vérifier qu'elle est toujours opérationnelle "
            "et qu'elle n'a pas changé d'adresse."
        )
