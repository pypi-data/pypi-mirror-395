import os
from pathlib import Path

from django.conf import settings
from django.db import migrations

# Avant le remplacement de django-stdimage par sorl-thumbnail, les miniatures
# étaient stockées dans le même dossier que les fichiers originaux. Le dossier
# 'avatars' est nettoyé de tous les fichiers non associés à User.avatar.


def delete_old_thumbnails(apps, schema_editor):
    path = Path(settings.MEDIA_ROOT) / "avatars"
    if not path.is_dir():
        return

    User = apps.get_model("accounts", "User")

    all_image_files = {
        str(child)
        for child in path.iterdir()
        if child.is_file()
    }

    used_image_files = {
        obj.avatar.path
        for obj in User.objects.all()
        if obj.avatar
    }

    unused_image_files = all_image_files - used_image_files
    for image in unused_image_files:
        os.remove(image)


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_rename_user_anonymized"),
    ]

    operations = [
        migrations.RunPython(delete_old_thumbnails),
    ]
