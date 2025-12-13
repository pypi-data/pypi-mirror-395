from django.db import models


class MigrationCode(models.Model):
    """
    Stores the source code of applied migrations.

    This model acts as a companion to Django's built-in `django_migrations` table,
    storing the complete Python source code for each migration. This enables
    rollback operations even when migration files are missing from the codebase.

    The model uses `app_label` and `migration_name` to match Django's migration
    identification pattern, which corresponds to the `app` and `name` fields
    in Django's `django_migrations` table.

    Note: The `stored_at` field represents when the code was stored in this table,
    which may differ from when the migration was actually applied (tracked in
    `django_migrations.applied`).
    """

    app_label = models.CharField(
        max_length=100,
        help_text="Django app label (matches django_migrations.app field)",
        db_index=True,
    )
    migration_name = models.CharField(
        max_length=255,
        help_text=(
            "Migration name (e.g., '0001_initial', matches django_migrations.name). "
            "Typically follows pattern: NNNN_name where NNNN is a 4-digit number."
        ),
        db_index=True,
    )
    source_code = models.TextField(
        help_text="Complete Python source code of the migration file"
    )
    stored_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the migration source code was stored in this table",
        db_index=True,
    )

    class Meta:
        db_table = "django_migrations_code"
        verbose_name = "Migration Source Code"
        verbose_name_plural = "Migration Source Code"
        unique_together = [["app_label", "migration_name"]]
        indexes = [
            models.Index(fields=["app_label", "migration_name"]),
            models.Index(fields=["stored_at"]),
        ]
        ordering = ["app_label", "migration_name"]

    def __str__(self) -> str:
        """
        Return string representation: app_label.migration_name.

        Returns:
            String in format 'app_label.migration_name'.
        """
        return f"{self.app_label}.{self.migration_name}"

    def __repr__(self) -> str:
        """
        Return detailed representation for debugging.

        Returns:
            Detailed string representation including app_label, migration_name,
            source code length, and stored_at timestamp.
        """
        return (
            f"<MigrationCode: {self.app_label}.{self.migration_name} "
            f"({len(self.source_code)} bytes, stored_at={self.stored_at})>"
        )
