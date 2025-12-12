from django.contrib.auth.mixins import AccessMixin
from django.db.models import Count, Max, Q
from django.shortcuts import redirect
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import TemplateView

from benevalibre.views.mixins import PageContextMixin


class BasePanel:
    template_name: str

    def get_context_data(self):
        return {}

    def render(self):
        context_data = self.get_context_data()
        template = get_template(self.template_name)
        return template.render(context_data)

    __str__ = render
    __html__ = render


class AssociationMembershipPanel(BasePanel):
    template_name = "shared/association_membership_panel.html"

    def __init__(self, user, association, membership=None):
        self.user = user
        self.association = association
        self.membership = membership

    def get_user_benevalos_context(self):
        context = (
            self.user.benevalos
            .filter(association=self.association)
            .aggregate(
                count_validated=Count("id", filter=Q(is_active=True)),
                count_pending=Count("id", filter=Q(is_active=False)),
                last_date=Max("date"),
            )
        )  # fmt: skip
        context["index_url"] = "%s?association=%d" % (
            reverse("user_benevalos:index"),
            self.association.pk,
        )
        if self.user.has_perm("benevalibre.add_benevalo", self.association):
            context["add_url"] = "%s?association=%d" % (
                reverse("user_benevalos:create"),
                self.association.pk,
            )
        return context

    def get_benevalos_context(self):
        context = self.association.benevalos.aggregate(
            count_validated=Count("id", filter=Q(is_active=True)),
            count_pending=Count("id", filter=Q(is_active=False)),
            last_date=Max("date"),
        )
        context["manage_url"] = reverse(
            "association_benevalos:index",
            kwargs={"association": self.association.pk},
        )
        return context

    def get_members_context(self):
        context = self.association.memberships.aggregate(
            count_validated=Count("id", filter=Q(is_active=True)),
            count_pending=Count("id", filter=Q(is_active=False)),
        )
        context["manage_url"] = reverse(
            "association_members:index",
            kwargs={"association": self.association.pk},
        )
        return context

    def get_context_data(self):
        context = {
            "association": self.association,
            "membership": self.membership,
            "role": self.membership.role if self.membership else None,
        }

        if self.association.is_active and (
            self.membership is None or self.membership.is_active
        ):
            context["user_benevalos"] = self.get_user_benevalos_context()

            if self.user.has_perm(
                "associations.manage_benevalos",
                self.association,
            ):
                context["benevalos"] = self.get_benevalos_context()

            if self.user.has_perm(
                "associations.manage_members",
                self.association,
            ):
                context["members"] = self.get_members_context()

        return context


class DashboardView(PageContextMixin, AccessMixin, TemplateView):
    page_title = "Tableau de bord"
    template_name = "dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_active:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_associations(self):
        if self.request.user.is_anonymous_member:
            return [
                AssociationMembershipPanel(
                    self.request.user,
                    self.request.user.association,
                ),
            ]

        return [
            AssociationMembershipPanel(
                self.request.user,
                membership.association,
                membership=membership,
            )
            for membership in (
                self.request.user.memberships.select_related(
                    "association", "role"
                ).order_by("association__name")
            )
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["associations"] = self.get_associations()
        return context


class WelcomeView(PageContextMixin, TemplateView):
    page_title = "Accueil"
    template_name = "welcome.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("dashboard")
        return super().get(*args, **kwargs)
