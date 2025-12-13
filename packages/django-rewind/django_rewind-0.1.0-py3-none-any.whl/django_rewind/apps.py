from django.apps import AppConfig


class DjangoRewindConfig(AppConfig):
    """
    Configuration for django-rewind app.

    This app provides persistent storage of migration source code,
    enabling rollback operations even when migration files are missing.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_rewind"
    verbose_name = "Django Rewind"

    def ready(self) -> None:
        """
        Replace Django's MigrationExecutor with our enhanced version.

        This ensures that all migrations automatically use PersistentMigrationExecutor,
        which stores migration code when migrations are applied.

        This is done at app startup, so the standard Django migrate command
        will automatically use our enhanced executor.

        Can be disabled by setting DJANGO_REWIND_ENABLED = False in settings.
        """
        # Check if feature is enabled (default to True if not set)
        from django.conf import settings

        enabled = getattr(settings, "DJANGO_REWIND_ENABLED", True)

        if not enabled:
            return

        # Import here to avoid circular imports and ensure Django is fully loaded
        from django.db.migrations import executor as migrations_executor_module

        from django_rewind.executor import PersistentMigrationExecutor

        # Replace Django's MigrationExecutor with our enhanced version
        migrations_executor_module.MigrationExecutor = PersistentMigrationExecutor
