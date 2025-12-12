import rules

from benevalibre.associations.models import Association


@rules.predicate
def is_benevalo_author(user, benevalo):
    if user.is_anonymous_member:
        return benevalo.anonymous_member == user
    return user.is_authenticated and benevalo.user == user


@rules.predicate
def benevalo_association_has_migration(user, benevalo):
    return benevalo.association.has_migration


@rules.predicate
def can_add_benevalo(user, association=None):
    if association is None:
        if user.is_anonymous_member:
            return not user.association.has_migration
        return user.is_authenticated and (
            Association.objects.active()
            .with_active_member(user)
            .without_migration()
            .exists()
        )
    return (
        association.is_active
        and association.has_member(user)
        and not association.has_migration
    )


rules.add_perm(
    "benevalibre.add_benevalo",
    can_add_benevalo,
)
rules.add_perm(
    "benevalibre.change_benevalo",
    is_benevalo_author & ~benevalo_association_has_migration,
)
rules.add_perm(
    "benevalibre.delete_benevalo",
    is_benevalo_author & ~benevalo_association_has_migration,
)
