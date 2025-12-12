import os
from pathlib import Path

from django.conf import settings
from django.db import migrations

# Avant le remplacement de django-stdimage par sorl-thumbnail, les miniatures
# étaient stockées dans le même dossier que les fichiers originaux. Le dossier
# 'logos' est nettoyé de tous les fichiers non associés à Association.logo.


def delete_old_thumbnails(apps, schema_editor):
    path = Path(settings.MEDIA_ROOT) / "logos"
    if not path.is_dir():
        return

    Association = apps.get_model("association", "Association")

    all_image_files = {
        str(child)
        for child in path.iterdir()
        if child.is_file()
    }

    used_image_files = {
        obj.logo.path
        for obj in Association.objects.all()
        if obj.logo
    }

    unused_image_files = all_image_files - used_image_files
    for image in unused_image_files:
        os.remove(image)


class Migration(migrations.Migration):

    dependencies = [
        ("association", "0018_alter_association_logo"),
    ]

    operations = [
        migrations.RunPython(delete_old_thumbnails),
    ]
