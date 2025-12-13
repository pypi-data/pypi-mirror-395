import sys
import types
from typing import Any, Optional

from django_rewind.models import MigrationCode


class StoredMigrationLoader:
    """
    Loads migrations from stored code when files are missing.
    """

    @staticmethod
    def load_from_code(app_label: str, migration_name: str, source_code: str) -> Any:
        """
        Dynamically load a migration from stored source code.

        Args:
            app_label: The Django app label (e.g., 'myapp')
            migration_name: The migration name (e.g., '0001_initial')
            source_code: The Python source code of the migration

        Returns:
            A migration instance that can be used by Django's executor.

        Raises:
            ValueError: If no Migration class is found in the source code.
        """
        # Create a unique module name
        module_name = f"_stored_migrations.{app_label}.{migration_name}"

        # Create a new module
        module = types.ModuleType(module_name)
        module.__file__ = f"<stored:{app_label}.{migration_name}>"

        # Add required imports to the module's namespace
        module.__dict__.update(
            {
                "migrations": __import__(
                    "django.db.migrations", fromlist=["migrations"]
                ),
                "models": __import__("django.db.models", fromlist=["models"]),
            }
        )

        # Execute the code in the module's namespace
        exec(source_code, module.__dict__)

        # Add to sys.modules so imports work
        sys.modules[module_name] = module

        # Get the Migration class
        if hasattr(module, "Migration"):
            migration_class = module.Migration
            return migration_class(migration_name, app_label)

        raise ValueError(
            f"No Migration class found in stored code for {app_label}.{migration_name}"
        )

    @staticmethod
    def get_stored_migration(app_label: str, migration_name: str) -> Optional[Any]:
        """
        Retrieve and load a migration from stored code.

        Args:
            app_label: The Django app label (e.g., 'myapp')
            migration_name: The migration name (e.g., '0001_initial')

        Returns:
            A migration instance if found in the database, None otherwise.
        """
        try:
            stored = MigrationCode.objects.get(
                app_label=app_label, migration_name=migration_name
            )
            return StoredMigrationLoader.load_from_code(
                app_label, migration_name, stored.source_code
            )
        except MigrationCode.DoesNotExist:
            return None
