import json
import logging
from itertools import groupby

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.forms.models import ModelChoiceIterator

from benevalibre.associations.models import (
    Association,
    AssociationAnonymousMember,
    AssociationBenevaloCategory,
    AssociationBenevaloLevel,
    AssociationMembership,
    AssociationMigration,
    AssociationProject,
    AssociationRole,
)
from benevalibre.forms import NativeDateTimeInput
from benevalibre.forms.benevalos import BenevaloForm

logger = logging.getLogger("benevalibre.associations")


class ActivityFieldGroupChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset.select_related(
            "activity_field_group"
        ).order_by("activity_field_group__name", "name")
        # Regroupe les choix par groupe de champs d'activité
        for group, activity_fields in groupby(
            queryset,
            lambda obj: obj.activity_field_group,
        ):
            yield (
                str(group),
                [
                    self.choice(activity_field)
                    for activity_field in activity_fields
                ],
            )


class ActivityFieldChoiceField(forms.ModelChoiceField):
    iterator = ActivityFieldGroupChoiceIterator


class AssociationForm(forms.ModelForm):
    class Meta:
        model = Association
        fields = [
            "name",
            "description",
            "website_url",
            "logo",
            "activity_field",
            "is_hidden",
            "moderate_membership",
            "moderate_benevalo",
            "country",
            "postal_code",
            "has_employees",
            "income",
        ]
        field_classes = {
            "activity_field": ActivityFieldChoiceField,
        }

    template_name = "forms/layouts/association.html"


class AssociationImportForm(forms.Form):
    file = forms.FileField(
        label="Fichier de données",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["json"],
                message="Veuillez choisir un fichier JSON valide.",
            ),
        ],
        widget=forms.FileInput(attrs={"accept": ".json,application/json"}),
    )

    def clean(self):
        cleaned_data = super().clean()

        if not self.has_error("file"):
            try:
                cleaned_data["data"] = json.load(cleaned_data["file"])
            except ValueError:
                logger.exception("Failed to deserialize JSON file to import")
                self.add_error("file", "Le fichier est corrompu ou incorrect.")

        return cleaned_data


class AssociationMigrateForm(forms.ModelForm):
    class Meta:
        model = AssociationMigration
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 3}),
        }


class AssociationMembershipForm(forms.ModelForm):
    class Meta:
        model = AssociationMembership
        fields = ["role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["role"].queryset = (
            self.instance.association.roles.all().order_by("name")
        )  # fmt: skip


class AssociationAnonymousMemberForm(forms.ModelForm):
    class Meta:
        model = AssociationAnonymousMember
        fields = ["name", "expiration_date", "is_active"]
        widgets = {
            "expiration_date": NativeDateTimeInput(),
        }


class BenevaloAuthorType(models.TextChoices):
    USER = "user", "Utilisateur⋅rice"
    ANONYMOUS = "anonymous_member", "Membre anonyme"

    __empty__ = "Aucun"


class AssociationBenevaloForm(BenevaloForm):
    author_type = forms.ChoiceField(
        choices=BenevaloAuthorType.choices,
        required=False,
        label="Membre",
        widget=forms.Select(attrs={"x-model": "author_type"}),
    )

    class Meta(BenevaloForm.Meta):
        fields = ["user", "anonymous_member"] + BenevaloForm.Meta.fields

    template_name = "forms/layouts/association_benevalo.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.user:
            self.initial["author_type"] = BenevaloAuthorType.USER
        elif self.instance.anonymous_member:
            self.initial["author_type"] = BenevaloAuthorType.ANONYMOUS

        self.fields["user"].queryset = (
            self.instance.association.members.all().order_by_full_name()
        )  # fmt: skip
        self.fields["anonymous_member"].queryset = (
            self.instance.association.anonymous_members.all()
        )  # fmt: skip

    def clean(self):
        cleaned_data = super().clean()

        if not self.has_error("author_type"):
            if author_type := cleaned_data.get("author_type"):
                if not self.has_error(author_type):
                    if not cleaned_data.get(author_type):
                        self.add_error(
                            author_type,
                            ValidationError(
                                "Veuillez choisir un membre parmi la liste.",
                                code="required",
                            ),
                        )
                    elif author_type == BenevaloAuthorType.USER:
                        cleaned_data["anonymous_member"] = None
                    else:
                        cleaned_data["user"] = None
            else:
                cleaned_data["user"] = None
                cleaned_data["anonymous_member"] = None

        return cleaned_data


class AssociationBenevaloCategoryForm(forms.ModelForm):
    class Meta:
        model = AssociationBenevaloCategory
        fields = ["name", "description", "default_category"]

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        # Inclus l'association pour valider la contrainte sur le nom
        exclude.remove("association")
        return exclude


class AssociationBenevaloLevelForm(forms.ModelForm):
    class Meta:
        model = AssociationBenevaloLevel
        fields = ["name", "description"]

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        # Inclus l'association pour valider la contrainte sur le nom
        exclude.remove("association")
        return exclude


class AssociationProjectForm(forms.ModelForm):
    class Meta:
        model = AssociationProject
        fields = ["name", "description"]

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        # Inclus l'association pour valider la contrainte sur le nom
        exclude.remove("association")
        return exclude


class BaseRoleForm(forms.ModelForm):
    class Meta:
        fields = [
            "name",
            "description",
            "is_default",
            "list_members",
            "manage_members",
            "manage_benevalos",
            "manage_benevalo_categories",
            "manage_benevalo_levels",
            "manage_projects",
            "manage_roles",
            "manage_association",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    template_name = "forms/layouts/role.html"


class AssociationRoleForm(BaseRoleForm):
    class Meta(BaseRoleForm.Meta):
        model = AssociationRole

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        # Inclus l'association pour valider la contrainte sur le nom
        exclude.remove("association")
        # Exclus la validation d'un unique rôle par défaut, l'actuel sera
        # modifié avant l'appel de save() pour qu'il n'y en ait qu'un
        exclude.add("is_default")
        return exclude

    def save(self, commit=True):
        if not self.errors and self.instance.is_default:
            queryset = AssociationRole.objects.default().filter(
                association=self.instance.association
            )
            if self.instance.pk is not None:
                queryset = queryset.exclude(pk=self.instance.pk)
            queryset.update(is_default=False)
        return super().save(commit=commit)
