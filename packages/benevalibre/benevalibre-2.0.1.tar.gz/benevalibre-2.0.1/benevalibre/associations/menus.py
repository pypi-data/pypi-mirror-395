from django.urls import reverse

from benevalibre.menus import Menu, MenuItem, PermissionRequiredMenuItem


class AssociationMigrationMenuItem(MenuItem):
    def is_shown(self, request, obj=None):
        return (
            obj is not None
            and obj.has_migration
            and request.user.has_perm("associations.migrate_association", obj)
        )


association_management_menu = Menu(
    items=[
        AssociationMigrationMenuItem(
            url=lambda request, obj: reverse(
                "associations:migrate",
                kwargs={"pk": obj.pk},
            ),
            label="Migration",
            icon_name="paper-plane",
        ),
        PermissionRequiredMenuItem(
            url=lambda request, obj: reverse(
                "associations:update",
                kwargs={"pk": obj.pk},
            ),
            label="Paramètres",
            icon_name="gear",
            permission="associations.change_association",
        ),
        PermissionRequiredMenuItem(
            url=lambda request, obj: reverse(
                "association_members:index",
                kwargs={"association": obj.pk},
            ),
            label="Membres",
            icon_name="users",
            permission="associations.manage_members",
        ),
        PermissionRequiredMenuItem(
            url=lambda request, obj: reverse(
                "association_anonymous_members:index",
                kwargs={"association": obj.pk},
            ),
            label="Membres anonymes",
            icon_name="user-secret",
            permission="associations.manage_members",
        ),
        PermissionRequiredMenuItem(
            url=lambda request, obj: reverse(
                "association_benevalos:index",
                kwargs={"association": obj.pk},
            ),
            label="Actions de bénévolat",
            icon_name="gift",
            permission="associations.manage_benevalos",
        ),
        PermissionRequiredMenuItem(
            url=lambda request, obj: reverse(
                "association_benevalo_categories:index",
                kwargs={"association": obj.pk},
            ),
            label="Catégories de bénévolat",
            icon_name="tags",
            permission="associations.manage_benevalo_categories",
        ),
        PermissionRequiredMenuItem(
            url=lambda request, obj: reverse(
                "association_benevalo_levels:index",
                kwargs={"association": obj.pk},
            ),
            label="Niveaux de bénévolat",
            icon_name="gauge",
            permission="associations.manage_benevalo_levels",
        ),
        PermissionRequiredMenuItem(
            url=lambda request, obj: reverse(
                "association_projects:index",
                kwargs={"association": obj.pk},
            ),
            label="Projets",
            icon_name="folder",
            permission="associations.manage_projects",
        ),
        PermissionRequiredMenuItem(
            url=lambda request, obj: reverse(
                "association_roles:index",
                kwargs={"association": obj.pk},
            ),
            label="Rôles",
            icon_name="key",
            permission="associations.manage_roles",
        ),
        PermissionRequiredMenuItem(
            url=lambda request, obj: reverse(
                "association_statistics",
                kwargs={"association": obj.pk},
            ),
            label="Statistiques",
            icon_name="chart",
            permission="associations.view_statistics",
        ),
    ],
)
