from typing import Any

from django.core.management.base import BaseCommand
from django.db import connection

from django_rewind.models import MigrationCode


class Command(BaseCommand):
    help = "Show which migrations have code stored in the database"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("app_label", nargs="?", help="App label to filter by")

    def handle(self, *args: Any, **options: Any) -> None:
        app_label = options.get("app_label")

        # Get all stored migrations
        stored = MigrationCode.objects.all()
        if app_label:
            stored = stored.filter(app_label=app_label)

        # Get all applied migrations from django_migrations
        from django.db.migrations.recorder import MigrationRecorder

        recorder = MigrationRecorder(connection)
        applied = {(m.app, m.name) for m in recorder.migration_qs}

        self.stdout.write(self.style.SUCCESS("Stored Migrations:"))
        self.stdout.write("")

        for store in stored.order_by("app_label", "migration_name"):
            status = "✓" if (store.app_label, store.migration_name) in applied else "✗"
            code_size = len(store.source_code)
            self.stdout.write(
                f"{status} {store.app_label}.{store.migration_name} "
                f"({code_size} bytes, stored {store.stored_at:%Y-%m-%d})"
            )

        # Show migrations without stored code
        self.stdout.write("")
        self.stdout.write(self.style.WARNING("Applied but not stored:"))

        for app, name in sorted(applied):
            if not stored.filter(app_label=app, migration_name=name).exists():
                self.stdout.write(f"  ! {app}.{name}")
