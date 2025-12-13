from typing import Any, Dict

from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

from django_rewind.models import MigrationCode


@admin.register(MigrationCode)
class MigrationCodeAdmin(admin.ModelAdmin):
    """
    Admin interface for MigrationCode model.

    Provides a read-only interface for inspecting stored migration code.
    Migrations are automatically stored when applied via the migrate command.
    """

    list_display = [
        "app_label",
        "migration_name_link",
        "code_size",
        "stored_at",
        "file_status",
        "is_applied",
    ]
    list_filter = ["app_label", "stored_at"]
    search_fields = ["app_label", "migration_name"]
    date_hierarchy = "stored_at"
    readonly_fields = [
        "app_label",
        "migration_name",
        "stored_at",
        "warning_banner",
        "file_status_detail",
        "source_code",
    ]
    fieldsets = (
        (
            "Migration Information",
            {
                "fields": ("app_label", "migration_name", "stored_at"),
            },
        ),
        (
            "Status & Warnings",
            {
                "fields": ("warning_banner", "file_status_detail"),
                "description": "Current status and any warnings about this migration",
            },
        ),
        (
            "Source Code",
            {
                "fields": ("source_code",),
                "description": "Complete Python source code of the migration file",
            },
        ),
    )

    def code_size(self, obj: MigrationCode) -> str:
        """
        Display the size of stored code in a human-readable format.

        Args:
            obj: The MigrationCode instance

        Returns:
            Human-readable size string (bytes, KB, or MB)
        """
        size = len(obj.source_code)
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"

    code_size.short_description = "Code Size"

    def migration_name_link(self, obj: MigrationCode) -> str:
        """
        Display migration name as a link to the detail view.

        Args:
            obj: The MigrationCode instance

        Returns:
            HTML-formatted link to the detail view
        """
        url = reverse("admin:django_rewind_migrationcode_change", args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, escape(obj.migration_name))

    migration_name_link.short_description = "Migration Name"
    migration_name_link.admin_order_field = "migration_name"

    def warning_banner(self, obj: MigrationCode) -> str:
        """
        Display warning banner if file is missing or differs.

        Args:
            obj: The MigrationCode instance

        Returns:
            HTML-formatted warning banner or empty string
        """
        status = self._get_file_status(obj)

        # Only show warning if file is missing or differs
        if "Missing" in status["icon"]:
            return format_html(
                '<div style="padding: 16px; background: {}; border-radius: 4px; border: 2px solid {}; color: {}; margin-bottom: 16px;">'
                '<strong style="font-size: 14px;">⚠ WARNING: Migration file not found in current codebase</strong><br>'
                '<p style="margin: 8px 0 0 0; font-size: 13px;">{}<br>'
                "This migration was applied from a different branch or the file was deleted. "
                "The code is stored in the database for rollback purposes.</p>"
                "</div>",
                status["bg_color"],
                status["border_color"],
                status["text_color"],
                status["message"],
            )
        elif "Differs" in status["icon"]:
            return format_html(
                '<div style="padding: 16px; background: {}; border-radius: 4px; border: 2px solid {}; color: {}; margin-bottom: 16px;">'
                '<strong style="font-size: 14px;">✗ WARNING: Code mismatch detected</strong><br>'
                '<p style="margin: 8px 0 0 0; font-size: 13px;">{}<br>'
                "The migration file exists but its content differs from the stored code. "
                "This may indicate the file was modified after it was applied to the database.</p>"
                "</div>",
                status["bg_color"],
                status["border_color"],
                status["text_color"],
                status["message"],
            )
        return ""

    warning_banner.short_description = ""

    def source_code(self, obj: MigrationCode) -> str:
        """
        Display complete source code with line numbers.

        Args:
            obj: The MigrationCode instance

        Returns:
            HTML-formatted full source code
        """
        if not obj.source_code:
            return "No code stored"

        # Split into lines and add line numbers
        lines = obj.source_code.split("\n")
        numbered_lines = [f"{i+1:4d} | {line}" for i, line in enumerate(lines)]
        numbered_code = "\n".join(numbered_lines)

        # Escape HTML and format as code
        escaped_code = escape(numbered_code)

        return format_html(
            '<pre style="max-height: 400px; overflow: auto; background: #f5f5f5; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px; line-height: 1.4;"><code>{}</code></pre>',
            mark_safe(escaped_code),
        )

    source_code.short_description = "Source Code"

    def file_status_detail(self, obj: MigrationCode) -> str:
        """
        Show detailed file status comparison.

        Args:
            obj: The MigrationCode instance

        Returns:
            HTML-formatted status detail
        """
        status = self._get_file_status(obj)
        return format_html(
            '<div style="padding: 12px; background: {}; border-radius: 4px; border: 1px solid {}; color: {};">'
            "<strong>Status:</strong> {}<br>"
            "<strong>Message:</strong> {}"
            "</div>",
            status["bg_color"],
            status["border_color"],
            status["text_color"],
            status["icon"],
            status["message"],
        )

    file_status_detail.short_description = "File Status"

    def file_status(self, obj: MigrationCode) -> str:
        """
        Display file status in list view.

        Args:
            obj: The MigrationCode instance

        Returns:
            HTML-formatted status icon
        """
        status = self._get_file_status(obj)
        return format_html(
            '<span style="color: {};" title="{}">{}</span>',
            status["text_color"],
            status["message"],
            status["icon"],
        )

    file_status.short_description = "File"

    def _get_file_status(self, obj: MigrationCode) -> Dict[str, str]:
        """
        Check file status: exists, missing, or differs.

        Args:
            obj: The MigrationCode instance

        Returns:
            Dictionary with status information containing:
            - icon: Status icon text
            - message: Status message
            - bg_color: Background color for detail view
            - border_color: Border color for detail view
            - text_color: Text color for both views
        """
        try:
            import os

            from django.apps import apps

            app_config = apps.get_app_config(obj.app_label)
            file_path = os.path.join(
                app_config.path, "migrations", f"{obj.migration_name}.py"
            )

            if not os.path.exists(file_path):
                return {
                    "icon": "⚠ Missing",
                    "message": "Migration file does not exist on disk (code only in database)",
                    "bg_color": "#fff8e1",
                    "border_color": "#ffc107",
                    "text_color": "#856404",
                }

            # Read and compare file content
            with open(file_path, "r", encoding="utf-8") as f:
                file_code = f.read()

            # Normalize for comparison (strip whitespace)
            if file_code.strip() == obj.source_code.strip():
                return {
                    "icon": "✓ Verified",
                    "message": "File exists and matches stored code",
                    "bg_color": "#e8f5e9",
                    "border_color": "#4caf50",
                    "text_color": "#1b5e20",
                }
            else:
                return {
                    "icon": "✗ Differs",
                    "message": "File exists but content differs from stored code",
                    "bg_color": "#ffebee",
                    "border_color": "#f44336",
                    "text_color": "#b71c1c",
                }
        except (LookupError, OSError, IOError):
            return {
                "icon": "? Unknown",
                "message": "Could not check file status",
                "bg_color": "#f5f5f5",
                "border_color": "#9e9e9e",
                "text_color": "#424242",
            }

    def is_applied(self, obj: MigrationCode) -> str:
        """
        Check if this migration is currently applied in django_migrations.

        Args:
            obj: The MigrationCode instance

        Returns:
            HTML-formatted status indicating if migration is applied
        """
        from django.db import connection
        from django.db.migrations.recorder import MigrationRecorder

        try:
            recorder = MigrationRecorder(connection)
            applied = recorder.migration_qs.filter(
                app=obj.app_label, name=obj.migration_name
            ).exists()

            if applied:
                return format_html(
                    '<span style="color: #28a745;" title="Migration is applied">✓ Applied</span>'
                )
            else:
                return format_html(
                    '<span style="color: #ffc107;" title="Migration is not applied">⚠ Not Applied</span>'
                )
        except Exception:
            return format_html('<span style="color: #6c757d;">? Unknown</span>')

    is_applied.short_description = "Applied"
    is_applied.boolean = False

    def has_add_permission(self, request: Any) -> bool:
        """
        Disable manual addition - migrations should only be stored automatically.

        Args:
            request: Django HTTP request object

        Returns:
            Always False to prevent manual addition
        """
        return False

    def has_change_permission(self, request: Any, obj: Any = None) -> bool:
        """
        Disable editing - stored migration code should not be modified.

        Args:
            request: Django HTTP request object
            obj: Optional MigrationCode instance

        Returns:
            Always False to prevent editing
        """
        return False

    def has_delete_permission(self, request: Any, obj: Any = None) -> bool:
        """
        Allow deletion - users may want to clean up old stored migrations.

        Args:
            request: Django HTTP request object
            obj: Optional MigrationCode instance

        Returns:
            Always True to allow deletion
        """
        return True

    def changelist_view(self, request: Any, extra_context: Any = None) -> Any:
        """
        Override changelist view to add summary statistics.

        Args:
            request: Django HTTP request object
            extra_context: Additional context for template

        Returns:
            TemplateResponse with summary statistics
        """
        response = super().changelist_view(request, extra_context=extra_context)

        # Calculate summary statistics
        try:
            queryset = self.get_queryset(request)
            total = queryset.count()

            # Count by status
            verified = 0
            missing = 0
            differs = 0
            unknown = 0

            for migration in queryset:
                status = self._get_file_status(migration)
                if "Verified" in status["icon"]:
                    verified += 1
                elif "Missing" in status["icon"]:
                    missing += 1
                elif "Differs" in status["icon"]:
                    differs += 1
                else:
                    unknown += 1

            # Add summary to context
            if hasattr(response, "context_data"):
                response.context_data["summary_stats"] = {
                    "total": total,
                    "verified": verified,
                    "missing": missing,
                    "differs": differs,
                    "unknown": unknown,
                }

        except Exception:
            # If anything goes wrong, just don't show stats
            pass

        return response
