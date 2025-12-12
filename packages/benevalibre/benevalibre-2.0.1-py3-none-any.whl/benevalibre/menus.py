from dataclasses import dataclass, field

from django.urls import reverse_lazy
from django.utils.functional import Promise

from django_cotton.templatetags import Attrs

from benevalibre.models import InstanceSettings


@dataclass
class BoundMenuItem:
    url: str
    label: str
    icon_name: str | None = None
    is_active: bool = False
    attrs: dict = field(default_factory=dict)

    def __post_init__(self):
        self.attrs = Attrs(self.attrs)


class MenuItem:
    def __init__(self, url, label, icon_name=None):
        self.url = url
        self.label = label
        self.icon_name = icon_name

    def get_url(self, request, obj=None):
        if isinstance(self.url, Promise):
            return str(self.url)
        if callable(self.url):
            return self.url(request, obj)
        return self.url

    def is_shown(self, request, obj=None):
        return True

    def get_bound_menu_item(self, request, obj=None):
        attrs = {}

        url = self.get_url(request, obj)
        is_external = url.startswith("http")
        is_active = not is_external and request.path.startswith(url)

        if is_external:
            attrs["rel"] = "noopener"

        return BoundMenuItem(
            url=url,
            label=self.label,
            icon_name=self.icon_name,
            is_active=is_active,
            attrs=attrs,
        )


class AdminOnlyMenuItem(MenuItem):
    def is_shown(self, request, obj=None):
        return request.user.is_superuser


class UserOnlyMenuItem(MenuItem):
    def is_shown(self, request, obj=None):
        return request.user.is_authenticated


class ActiveOnlyMenuItem(MenuItem):
    def is_shown(self, request, obj=None):
        return request.user.is_active


class PermissionRequiredMenuItem(MenuItem):
    def __init__(self, *args, permission, **kwargs):
        self.permission = permission
        super().__init__(*args, **kwargs)

    def is_shown(self, request, obj=None):
        return request.user.has_perm(self.permission, obj)


class Menu:
    def __init__(self, items):
        self.items = items

    def get_items_for_request(self, request, obj=None):
        for item in self.items:
            if item.is_shown(request, obj):
                yield item.get_bound_menu_item(request, obj)


# MENUS
# ------------------------------------------------------------------------------


main_menu = Menu(
    items=[
        ActiveOnlyMenuItem(
            url=reverse_lazy("dashboard"),
            label="Tableau de bord",
            icon_name="home",
        ),
        MenuItem(
            url=reverse_lazy("associations:index"),
            label="Associations",
            icon_name="institution",
        ),
        AdminOnlyMenuItem(
            url=reverse_lazy("instance_admin"),
            label="Administration",
            icon_name="gear",
        ),
    ],
)

user_menu = Menu(
    items=[
        ActiveOnlyMenuItem(
            url=reverse_lazy("user_benevalos:index"),
            label="Mes bénévolats",
            icon_name="gift",
        ),
        UserOnlyMenuItem(
            url=reverse_lazy("account:update"),
            label="Mon compte",
            icon_name="user",
        ),
    ],
)

admin_menu = Menu(
    items=[
        AdminOnlyMenuItem(
            url=reverse_lazy("instance_settings"),
            label="Paramètres",
            icon_name="gear",
        ),
        AdminOnlyMenuItem(
            url=reverse_lazy("announcements:index"),
            label="Annonces",
            icon_name="bullhorn",
        ),
        AdminOnlyMenuItem(
            url=reverse_lazy("default_benevalo_categories:index"),
            label="Catégories de bénévolat",
            icon_name="tags",
        ),
        AdminOnlyMenuItem(
            url=reverse_lazy("default_benevalo_levels:index"),
            label="Niveaux de bénévolat",
            icon_name="gauge",
        ),
        AdminOnlyMenuItem(
            url=reverse_lazy("default_roles:index"),
            label="Rôles",
            icon_name="key",
        ),
        AdminOnlyMenuItem(
            url=reverse_lazy("instance_statistics"),
            label="Statistiques",
            icon_name="chart",
        ),
    ],
)


class TermsMenuItem(MenuItem):
    def __init__(self, label, icon_name=None):
        super().__init__(url=None, label=label, icon_name=icon_name)

    def get_url(self, request, obj=None):
        instance_settings = InstanceSettings.for_request(request)
        return instance_settings.terms_of_use_file.url

    def is_shown(self, request, obj=None):
        instance_settings = InstanceSettings.for_request(request)
        return bool(instance_settings.terms_of_use_file)


footer_menu = Menu(
    items=[
        TermsMenuItem(label="Charte d'utilisation"),
        MenuItem(
            url="https://docs.benevalibre.org",
            label="Documentation",
        ),
        MenuItem(
            url="https://forum.benevalibre.org",
            label="Forum d'entraide",
        ),
        MenuItem(
            url="https://benevalibre.org",
            label="Le projet Bénévalibre",
        ),
    ],
)
