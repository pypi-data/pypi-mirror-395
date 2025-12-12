from django.contrib.auth.mixins import UserPassesTestMixin


class AdminViewMixin(UserPassesTestMixin):
    base_template_name = "admin/base.html"

    def test_func(self):
        return self.request.user.is_superuser
