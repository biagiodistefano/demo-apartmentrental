import typing as t

import django.db.migrations.operations.special
from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def add_realtor_group(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Group = apps.get_model('auth', 'Group')
    new_group, _ = Group.objects.get_or_create(name='realtor')
    # Additional group setup (like permissions) can be done here


def remove_realtor_group(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='realtor').delete()


class Migration(migrations.Migration):

    dependencies: t.List[t.Tuple[str, str]] = [
        # Specify any dependencies here, usually the last migration of the app
    ]

    operations: t.List[django.db.migrations.operations.special.RunPython] = [
        migrations.RunPython(add_realtor_group, remove_realtor_group),
    ]
