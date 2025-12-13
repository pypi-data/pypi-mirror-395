# Generated manually for django-rewind

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MigrationCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "app_label",
                    models.CharField(
                        db_index=True,
                        help_text="Django app label (matches django_migrations.app field)",
                        max_length=100,
                    ),
                ),
                (
                    "migration_name",
                    models.CharField(
                        db_index=True,
                        help_text=(
                            "Migration name (e.g., '0001_initial', matches django_migrations.name). "
                            "Typically follows pattern: NNNN_name where NNNN is a 4-digit number."
                        ),
                        max_length=255,
                    ),
                ),
                (
                    "source_code",
                    models.TextField(
                        help_text="Complete Python source code of the migration file"
                    ),
                ),
                (
                    "stored_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text="Timestamp when the migration source code was stored in this table",
                    ),
                ),
            ],
            options={
                "verbose_name": "Migration Source Code",
                "verbose_name_plural": "Migration Source Code",
                "db_table": "django_migrations_code",
                "ordering": ["app_label", "migration_name"],
            },
        ),
        migrations.AlterUniqueTogether(
            name="migrationcode",
            unique_together={("app_label", "migration_name")},
        ),
        migrations.AddIndex(
            model_name="migrationcode",
            index=models.Index(
                fields=["app_label", "migration_name"],
                name="django_migr_app_lab_d98bd3_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="migrationcode",
            index=models.Index(
                fields=["stored_at"],
                name="django_migr_stored__87212c_idx",
            ),
        ),
    ]
