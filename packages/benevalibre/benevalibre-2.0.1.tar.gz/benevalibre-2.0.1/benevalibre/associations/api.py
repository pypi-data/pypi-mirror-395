from typing import Optional

from django.utils import timezone

from ninja import Router, Schema
from ninja.errors import HttpError
from pydantic import UUID4, field_validator

from benevalibre.associations.models import AssociationMigration
from benevalibre.utils.types import HttpUrl

router = Router()


class AssociationMigrationSchema(Schema):
    is_done: bool
    destination_url: Optional[HttpUrl] = None

    @field_validator("destination_url", mode="before")
    @classmethod
    def blank_destination_url(cls, value: str) -> str | None:
        return value or None


class AssociationMigrationToken(Schema):
    token: UUID4
    destination_url: HttpUrl


@router.post(
    "/{int:association_id}/migrate",
    response={204: None},
    tags=["associations"],
    url_name="association_migrate",
)
def migrate_association(
    request,
    association_id: int,
    payload: AssociationMigrationToken,
):
    try:
        migration = AssociationMigration.objects.get(
            association_id=association_id,
            token=payload.token,
        )
    except AssociationMigration.DoesNotExist:
        raise HttpError(404, "Aucune association trouvée pour ces paramètres.")
    else:
        if migration.is_done:
            raise HttpError(410, "L'association a déjà été migrée.")

    migration.is_done = True
    migration.done_at = timezone.now().date()
    migration.destination_url = payload.destination_url

    migration.full_clean()
    migration.save()

    return 204, None


@router.get(
    "/{int:association_id}/migrate",
    response=AssociationMigrationSchema,
    tags=["associations"],
    url_name="association_migrate",
)
def get_association_migration(request, association_id: int):
    try:
        migration = AssociationMigration.objects.get(
            association_id=association_id,
        )
    except AssociationMigration.DoesNotExist:
        raise HttpError(404, "Aucune association trouvée pour ces paramètres.")

    return migration
