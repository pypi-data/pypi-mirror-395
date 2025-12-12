from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

import filetype


@deconstructible
class FileTypeValidator:
    message = (
        "Le format du fichier (%(type)s) n'est pas autorisé "
        "(types autorisés : %(allowed_types)s)."
    )
    code = "invalid_file_type"

    def __init__(self, allowed_types: list = None, message=None):
        if message is not None:
            self.message = message
        self.allowed_types = allowed_types

    def __call__(self, value):
        if self.allowed_types is not None:
            kind = filetype.guess(value)

            if not kind or kind.mime not in self.allowed_types:
                raise ValidationError(
                    self.message
                    % {
                        "type": kind.mime if kind else "inconnu",
                        "allowed_types": ", ".join(self.allowed_types),
                    },
                    code=self.code,
                )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, FileTypeValidator)
            and self.allowed_types == other.allowed_types
        )
