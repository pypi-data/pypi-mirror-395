import rules

from benevalibre.associations.models import AssociationRole


def has_any_association_role_perms(*perms):
    @rules.predicate
    def predicate(user, association):
        if not association.is_active:
            return False
        if role := AssociationRole.objects.get_for_user(user, association.pk):
            return any(getattr(role, perm) for perm in perms)
        return False

    return predicate


@rules.predicate
def association_has_migration(user, association):
    return association.has_migration


@rules.predicate
def can_view_association(user, association):
    if not association.is_active and not association.has_member(user):
        return False
    if user.is_anonymous_member:
        return association == user.association
    # Une association masquée n'est visible que connecté
    return not association.is_hidden or user.is_authenticated


rules.add_perm(
    "associations.add_association",
    rules.is_authenticated,
)
rules.add_perm(
    "associations.change_association",
    ~association_has_migration
    & has_any_association_role_perms("manage_association"),
)
rules.add_perm(
    "associations.delete_association",
    has_any_association_role_perms("manage_association"),
)
rules.add_perm(
    "associations.migrate_association",
    has_any_association_role_perms("manage_association"),
)
rules.add_perm(
    "associations.view_association",
    can_view_association,
)

rules.add_perm(
    "associations.list_members",
    has_any_association_role_perms(
        "list_members",
        "manage_benevalos",
        "manage_association",
    ),
)

# Gestion de l'association

rules.add_perm(
    "associations.manage_members",
    ~association_has_migration
    & has_any_association_role_perms(
        "manage_members",
        "manage_association",
    ),
)
rules.add_perm(
    "associations.manage_benevalos",
    ~association_has_migration
    & has_any_association_role_perms(
        "manage_benevalos",
        "manage_association",
    ),
)
rules.add_perm(
    "associations.manage_benevalo_levels",
    ~association_has_migration
    & has_any_association_role_perms(
        "manage_benevalo_levels",
        "manage_association",
    ),
)
rules.add_perm(
    "associations.manage_benevalo_categories",
    ~association_has_migration
    & has_any_association_role_perms(
        "manage_benevalo_categories",
        "manage_association",
    ),
)
rules.add_perm(
    "associations.manage_projects",
    ~association_has_migration
    & has_any_association_role_perms(
        "manage_projects",
        "manage_association",
    ),
)
rules.add_perm(
    "associations.manage_roles",
    ~association_has_migration
    & has_any_association_role_perms(
        "manage_roles",
        "manage_association",
    ),
)
rules.add_perm(
    "associations.view_statistics",
    has_any_association_role_perms(
        "manage_benevalos",
        "manage_association",
    ),
)
