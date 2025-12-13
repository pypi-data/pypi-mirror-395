import logging
from typing import Any, Callable, Optional

from django.db.migrations.executor import MigrationExecutor

from django_rewind.loader import StoredMigrationLoader
from django_rewind.recorder import PersistentMigrationRecorder

logger = logging.getLogger(__name__)


class PersistentMigrationExecutor(MigrationExecutor):
    """
    Extends Django's MigrationExecutor to use stored code when files are missing.
    """

    def __init__(
        self,
        connection: Any,
        progress_callback: Optional[Callable[..., None]] = None,
    ) -> None:
        """
        Initialize the executor with enhanced recorder.

        Args:
            connection: Django database connection object
            progress_callback: Optional callback function for migration progress
        """
        super().__init__(connection, progress_callback)
        # Replace the recorder with our enhanced version
        self.recorder = PersistentMigrationRecorder(connection)

    def _load_migration_or_stored(self, app_label: str, migration_name: str) -> Any:
        """
        Try to load migration from file, fall back to stored code.

        Args:
            app_label: The Django app label (e.g., 'myapp')
            migration_name: The migration name (e.g., '0001_initial')

        Returns:
            A migration instance loaded from file or stored code.

        Raises:
            KeyError: If migration cannot be found in file or stored code.
            ImportError: If migration cannot be imported from file or stored code.
        """
        # First try normal Django loading
        try:
            return self.loader.get_migration(app_label, migration_name)
        except (KeyError, ImportError):
            # File doesn't exist, try stored code
            stored_migration = StoredMigrationLoader.get_stored_migration(
                app_label, migration_name
            )
            if stored_migration:
                logger.info("Loading %s.%s from stored code", app_label, migration_name)
                return stored_migration
            raise

    def unapply_migration(self, state: Any, migration: Any, fake: bool = False) -> Any:
        """
        Override to use stored code if migration file is missing.

        Args:
            state: Django migration state object
            migration: Migration instance to unapply
            fake: If True, mark as unapplied without running operations

        Returns:
            Result from parent's unapply_migration method.
        """
        # Try to load from stored code if needed
        if not hasattr(migration, "operations"):
            migration = self._load_migration_or_stored(
                migration.app_label, migration.name
            )

        # Call parent with potentially replaced migration
        return super().unapply_migration(state, migration, fake=fake)
