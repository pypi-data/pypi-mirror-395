import os
from typing import Any, Optional, Set, Tuple

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

from django_rewind.models import MigrationCode


class Command(BaseCommand):
    """Backfill migration code for migrations applied before django-rewind was installed."""

    help = "Store source code for migrations that were applied before django-rewind was installed"

    def add_arguments(self, parser: Any) -> None:
        """Add command-line arguments."""
        parser.add_argument(
            "app_label",
            nargs="?",
            help="App label to backfill (optional, backfills all apps if not specified)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be backfilled without actually storing the code",
        )

    def _get_applied_migrations(
        self, app_label: Optional[str] = None
    ) -> Set[Tuple[str, str]]:
        """
        Get all applied migrations from django_migrations table.

        Args:
            app_label: Optional app label to filter by

        Returns:
            Set of (app_label, migration_name) tuples
        """
        recorder = MigrationRecorder(connection)
        applied = {(m.app, m.name) for m in recorder.migration_qs}
        if app_label:
            applied = {(app, name) for app, name in applied if app == app_label}
        return applied

    def _get_stored_migrations(self) -> Set[Tuple[str, str]]:
        """
        Get all migrations that already have code stored.

        Returns:
            Set of (app_label, migration_name) tuples
        """
        return {
            (m.app_label, m.migration_name)
            for m in MigrationCode.objects.all().only("app_label", "migration_name")
        }

    def _get_migration_file_path(
        self, app_label: str, migration_name: str
    ) -> Optional[str]:
        """
        Get the file path for a migration.

        Args:
            app_label: Django app label
            migration_name: Migration name (e.g., '0001_initial')

        Returns:
            Full file path, or None if app not found
        """
        try:
            app_config = apps.get_app_config(app_label)
            return os.path.join(app_config.path, "migrations", f"{migration_name}.py")
        except LookupError:
            return None

    def _read_migration_file(
        self, file_path: Optional[str], app_label: str, migration_name: str
    ) -> Optional[str]:
        """
        Read migration file code from disk.

        Args:
            file_path: Full path to migration file
            app_label: App label (for error messages)
            migration_name: Migration name (for error messages)

        Returns:
            File contents as string, or None if file doesn't exist or can't be read
        """
        if not file_path or not os.path.exists(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except (OSError, IOError, UnicodeDecodeError) as e:
            if self.verbosity >= 2:
                self.stdout.write(
                    self.style.WARNING(
                        f"  Warning: Could not read {app_label}.{migration_name}: {e}"
                    )
                )
            return None

    def _store_migration_code(
        self, app_label: str, migration_name: str, code: str
    ) -> None:
        """
        Store the migration code in the database.

        Args:
            app_label: Django app label
            migration_name: Migration name
            code: The migration source code to store
        """
        MigrationCode.objects.update_or_create(
            app_label=app_label,
            migration_name=migration_name,
            defaults={"source_code": code},
        )

    def _backfill_migration(
        self, app_label: str, migration_name: str, dry_run: bool = False
    ) -> Tuple[bool, Optional[str]]:
        """
        Backfill a single migration.

        Args:
            app_label: Django app label
            migration_name: Migration name
            dry_run: If True, don't actually store the code

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        file_path = self._get_migration_file_path(app_label, migration_name)
        if file_path is None:
            return False, f"App '{app_label}' not found"

        code = self._read_migration_file(file_path, app_label, migration_name)
        if code is None:
            return False, "Migration file not found or could not be read"

        if not dry_run:
            self._store_migration_code(app_label, migration_name, code)

        return True, None

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Main command handler.

        Returns:
            None
        """
        app_label = options.get("app_label")
        self.verbosity = options.get("verbosity", 1)
        dry_run = options.get("dry_run", False)

        if dry_run and self.verbosity >= 1:
            self.stdout.write(
                self.style.WARNING("DRY RUN MODE - No changes will be made")
            )
            self.stdout.write("")

        # Get applied migrations
        applied = self._get_applied_migrations(app_label)
        if not applied:
            self.stdout.write(
                self.style.WARNING("No applied migrations found to backfill.")
            )
            return

        # Get already stored migrations
        stored = self._get_stored_migrations()

        # Find migrations that need backfilling
        to_backfill = sorted(applied - stored)

        if not to_backfill:
            if self.verbosity >= 1:
                self.stdout.write(
                    self.style.SUCCESS(
                        "All applied migrations already have code stored."
                    )
                )
            return

        if self.verbosity >= 1:
            count = len(to_backfill)
            self.stdout.write(
                f"Found {count} migration(s) to backfill:"
                if not dry_run
                else f"Would backfill {count} migration(s):"
            )
            self.stdout.write("")

        # Backfill each migration
        successful = []
        failed = []

        for app, name in to_backfill:
            if self.verbosity >= 2:
                self.stdout.write(f"Processing {app}.{name}...")

            success, error = self._backfill_migration(app, name, dry_run=dry_run)

            if success:
                successful.append((app, name))
                if self.verbosity >= 1:
                    action = "Would store" if dry_run else "Stored"
                    self.stdout.write(self.style.SUCCESS(f"  ✓ {action} {app}.{name}"))
            else:
                failed.append((app, name, error))
                if self.verbosity >= 1:
                    self.stdout.write(
                        self.style.ERROR(f"  ✗ Failed {app}.{name}: {error}")
                    )

        # Summary
        if self.verbosity >= 1:
            self.stdout.write("")
            if successful:
                action = "Would be stored" if dry_run else "Stored"
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ {len(successful)} migration(s) {action.lower()}"
                    )
                )
            if failed:
                self.stdout.write(
                    self.style.ERROR(f"✗ {len(failed)} migration(s) failed")
                )
                if self.verbosity >= 2:
                    for app, name, error in failed:
                        self.stdout.write(f"  • {app}.{name}: {error}")
