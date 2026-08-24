import os

from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate


def create_render_admin(sender, using, **kwargs):
    username = os.environ.get("ADMIN_USERNAME")
    password = os.environ.get("ADMIN_PASSWORD")
    if not username or not password:
        return

    User = get_user_model()
    user, created = User._default_manager.db_manager(using).get_or_create(
        username=username,
        defaults={"is_staff": True, "is_superuser": True},
    )
    if created:
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=using)


class StreamConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stream"

    def ready(self):
        post_migrate.connect(create_render_admin, sender=self, dispatch_uid="stream.create_render_admin")
