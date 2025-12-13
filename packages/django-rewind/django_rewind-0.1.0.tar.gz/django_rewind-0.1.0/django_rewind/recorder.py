import logging
import os
from typing import Optional

from django.db.migrations.recorder import MigrationRecorder

from django_rewind.models import MigrationCode

logger = logging.getLogger(__name__)


class PersistentMigrationRecorder(MigrationRecorder):
    """
    Extends Django's MigrationRecorder to capture and store migration code.
    """

    def record_applied(self, app: str, name: str) -> None:
        """
        Override to capture migration source code when recording application.

        Args:
            app: The Django app label (e.g., 'myapp')
            name: The migration name (e.g., '0001_initial')
        """
        # Call parent to record in django_migrations
        super().record_applied(app, name)

        # Capture and store the migration code
        migration_code = self._get_migration_source(app, name)
        if migration_code:
            self._store_migration_code(app, name, migration_code)

    def _get_migration_source(self, app: str, name: str) -> Optional[str]:
        """
        Read the migration file from disk.

        Args:
            app: The Django app label (e.g., 'myapp')
            name: The migration name (e.g., '0001_initial')

        Returns:
            The migration source code as a string, or None if the file cannot be read.
        """
        try:
            # Read the source file
            # Find in installed apps
            from django.apps import apps

            app_config = apps.get_app_config(app)
            full_path = os.path.join(app_config.path, "migrations", f"{name}.py")

            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    return f.read()

        except Exception as e:
            logger.warning(
                "Could not capture migration code for %s.%s: %s",
                app,
                name,
                e,
                exc_info=True,
            )

        return None

    def _store_migration_code(self, app: str, name: str, code: str) -> None:
        """
        Store the migration code in the database.

        Args:
            app: The Django app label (e.g., 'myapp')
            name: The migration name (e.g., '0001_initial')
            code: The migration source code to store
        """
        try:
            MigrationCode.objects.update_or_create(
                app_label=app,
                migration_name=name,
                defaults={"source_code": code},
            )
        except Exception as e:
            # Handle case where django_migrations_code table doesn't exist yet
            # This can happen when migrations run before django-rewind's own migration
            # is applied (e.g., Django's built-in app migrations)
            # Log a warning but don't fail - these migrations can be backfilled later
            # Check if it's a "table doesn't exist" error
            error_msg = str(e).lower()
            if "does not exist" in error_msg or "no such table" in error_msg:
                logger.debug(
                    "Skipping migration code storage for %s.%s: "
                    "django_migrations_code table not yet created. "
                    "This is normal during initial migration setup. "
                    "Use backfill_migration_code to store these later if needed.",
                    app,
                    name,
                )
            else:
                # For other errors, log a warning
                logger.warning(
                    "Could not store migration code for %s.%s: %s",
                    app,
                    name,
                    e,
                    exc_info=True,
                )
