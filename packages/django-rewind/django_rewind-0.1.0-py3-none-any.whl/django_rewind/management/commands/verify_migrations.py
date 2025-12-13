import os
from collections import namedtuple
from typing import Any, List, Optional

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models.query import QuerySet

from django_rewind.models import MigrationCode

# Result container for migration verification
VerificationResult = namedtuple(
    "VerificationResult",
    ["migration", "status", "file_code"],
)


class Command(BaseCommand):
    """Verify that stored migration code matches files on disk."""

    help = "Verify that stored migration code matches files on disk"

    # Status constants
    STATUS_VERIFIED = "verified"
    STATUS_MISSING = "missing"
    STATUS_MISMATCH = "mismatch"

    def add_arguments(self, parser: Any) -> None:
        """Add command-line arguments."""
        parser.add_argument(
            "app_label",
            nargs="?",
            help="App label to verify (optional, verifies all if not specified)",
        )

    @staticmethod
    def _normalize_code(code: Optional[str]) -> Optional[str]:
        """
        Normalize code for comparison.

        Normalizes by:
        - Converting line endings to LF
        - Removing trailing whitespace from lines
        - Stripping leading/trailing whitespace

        Args:
            code: Source code string to normalize

        Returns:
            Normalized code string, or None if input is None
        """
        if code is None:
            return None

        # Normalize line endings to LF
        normalized = code.replace("\r\n", "\n").replace("\r", "\n")

        # Remove trailing whitespace from each line and strip overall
        lines = [line.rstrip() for line in normalized.split("\n")]
        return "\n".join(lines).strip()

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

    def _read_file_code(
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

    def _get_file_code(self, app_label: str, migration_name: str) -> Optional[str]:
        """
        Get migration file code from disk.

        Args:
            app_label: Django app label
            migration_name: Migration name

        Returns:
            File contents as string, or None if file doesn't exist
        """
        file_path = self._get_migration_file_path(app_label, migration_name)
        if file_path is None:
            return None

        return self._read_file_code(file_path, app_label, migration_name)

    def _compare_migration(self, stored_migration: MigrationCode) -> VerificationResult:
        """
        Compare a stored migration with its file on disk.

        Args:
            stored_migration: MigrationCode instance

        Returns:
            VerificationResult namedtuple with status and file_code
        """
        file_code = self._get_file_code(
            stored_migration.app_label, stored_migration.migration_name
        )

        if file_code is None:
            return VerificationResult(
                migration=stored_migration,
                status=self.STATUS_MISSING,
                file_code=None,
            )

        # Normalize both codes for comparison
        normalized_file = self._normalize_code(file_code)
        normalized_stored = self._normalize_code(stored_migration.source_code)

        if normalized_file != normalized_stored:
            return VerificationResult(
                migration=stored_migration,
                status=self.STATUS_MISMATCH,
                file_code=file_code,
            )

        return VerificationResult(
            migration=stored_migration,
            status=self.STATUS_VERIFIED,
            file_code=file_code,
        )

    def _get_stored_migrations(
        self, app_label: Optional[str] = None
    ) -> QuerySet[MigrationCode]:
        """
        Get stored migrations to verify.

        Args:
            app_label: Optional app label to filter by

        Returns:
            QuerySet of MigrationCode objects
        """
        queryset = MigrationCode.objects.all().order_by("app_label", "migration_name")
        if app_label:
            queryset = queryset.filter(app_label=app_label)
        return queryset

    def _report_verified(self, verified_results: List[VerificationResult]) -> None:
        """Report successfully verified migrations."""
        if verified_results and self.verbosity >= 1:
            count = len(verified_results)
            self.stdout.write(self.style.SUCCESS(f"✓ {count} migrations verified"))

    def _report_missing(self, missing_results: List[VerificationResult]) -> None:
        """Report missing migration files."""
        if not missing_results:
            return

        if self.verbosity >= 1:
            self.stdout.write("")
            count = len(missing_results)
            self.stdout.write(
                self.style.WARNING(f"⚠ {count} files missing (code in DB only):")
            )

        for result in missing_results:
            migration = result.migration
            self.stdout.write(f"  • {migration.app_label}.{migration.migration_name}")

    def _report_mismatches(self, mismatch_results: List[VerificationResult]) -> None:
        """Report code mismatches."""
        if not mismatch_results:
            return

        if self.verbosity >= 1:
            self.stdout.write("")
            count = len(mismatch_results)
            self.stdout.write(self.style.ERROR(f"✗ {count} code mismatches found:"))

        for result in mismatch_results:
            migration = result.migration
            self.stdout.write(f"  • {migration.app_label}.{migration.migration_name}")

            if self.verbosity >= 2 and result.file_code:
                # Show line count comparison in verbose mode
                file_lines = len(result.file_code.split("\n"))
                stored_lines = len(migration.source_code.split("\n"))
                self.stdout.write(
                    self.style.WARNING(
                        f"    File: {file_lines} lines, "
                        f"Stored: {stored_lines} lines"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING("    (File content differs from stored code)")
                )

    def _report_summary(self, has_mismatches: bool, has_missing: bool) -> None:
        """Report final summary message."""
        if not has_mismatches and not has_missing:
            if self.verbosity >= 1:
                self.stdout.write("")
                self.stdout.write(
                    self.style.SUCCESS("✓ All migrations verified successfully!")
                )
        elif self.verbosity >= 1:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "Note: Missing files are expected if migrations were deleted."
                )
            )

    def _report_results(self, results: List[VerificationResult]) -> int:
        """
        Report all verification results.

        Args:
            results: List of VerificationResult objects

        Returns:
            Exit code: 1 if mismatches found, 0 otherwise
        """
        # Group results by status
        verified = [r for r in results if r.status == self.STATUS_VERIFIED]
        missing = [r for r in results if r.status == self.STATUS_MISSING]
        mismatches = [r for r in results if r.status == self.STATUS_MISMATCH]

        # Report each category
        self._report_verified(verified)
        self._report_missing(missing)
        self._report_mismatches(mismatches)
        self._report_summary(bool(mismatches), bool(missing))

        # Return exit code: 1 if mismatches found, 0 otherwise
        return 1 if mismatches else 0

    def handle(self, *args: Any, **options: Any) -> int:
        """
        Main command handler.

        Returns:
            Exit code: 0 for success, 1 if mismatches found
        """
        app_label = options.get("app_label")
        self.verbosity = options.get("verbosity", 1)

        # Get stored migrations
        stored_migrations = list(self._get_stored_migrations(app_label))

        if not stored_migrations:
            self.stdout.write(
                self.style.WARNING("No stored migrations found to verify.")
            )
            return 0

        # Show progress message
        if self.verbosity >= 1:
            self.stdout.write("Verifying stored migrations...")
            self.stdout.write("")

        # Verify each migration
        results = [
            self._compare_migration(migration) for migration in stored_migrations
        ]

        # Report results and return exit code
        return self._report_results(results)
