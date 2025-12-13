# ⏪ django-rewind

**Roll back Django migrations even when the migration file is deleted.**

Your database stores the migration source code. Switch branches freely. Rewind anytime.

> **Never lose the ability to roll back.** django-rewind automatically saves every migration's code to your database, so you can always undo changes — even if the migration file is gone.

**Built on a fundamental principle:** The database is persistent and long-running, while source code is ephemeral and ever-changing. The database itself is the authoritative record of what migrations have been applied - django-rewind ensures your database can always reverse its own history, independent of your source code.

---

## The Problem

You deploy a feature branch with a new migration. The migration runs successfully. Then you switch back to `main` (which doesn't have that migration file). Now your database schema doesn't match your code, and Django can't roll back because the migration file is gone.

**The result?** Redeploying old branches, manual SQL fixes, or that sinking feeling in your stomach. 😰

---

## The Solution

**django-rewind** solves this by automatically storing every migration's code in your database when it's applied. Even if the file disappears from your codebase, you can still roll back using the stored code. It's like having a safety net for your migrations! 🎯

```bash
# Branch A: Apply migration
python manage.py migrate
# ✓ Migration 0005 applied and code stored

# Branch B: File is gone, but rollback still works!
python manage.py migrate myapp 0004
# ✓ Loading myapp.0005 from stored code
# ✓ Successfully rolled back
```

---

## Features

- ⏪ **Rollback without files** - Migrations stored in database
- 🔄 **Branch switching** - Deploy any branch without migration conflicts
- 🛡️ **Safety net** - Never lose the ability to roll back
- 📊 **Django Admin** - Visual interface for inspection
- ⚡ **Zero config** - Works automatically once installed
- 🔍 **Verification** - Compare stored code vs. current files
- 🚀 **Production ready** - Non-invasive, backwards compatible

---

## Quick Start

Get up and running in under 2 minutes! 🚀

### Installation

Install django-rewind using pip:

```bash
pip install django-rewind
```

### Configuration

Add `django_rewind` to your `INSTALLED_APPS` in `settings.py`. Make sure to add it **before** your other apps:

```python
# settings.py
INSTALLED_APPS = [
    'django_rewind',  # Add this first
    'django.contrib.admin',
    'django.contrib.auth',
    # ... your other apps
]
```

Then run migrations to create the storage table:

```bash
python manage.py migrate
```

### Usage

That's it! Now migrations are automatically stored whenever you run `migrate`:

```bash
# Migrations work exactly as before - no changes needed!
python manage.py makemigrations
python manage.py migrate
# ✓ Migration code automatically stored in database

# Now you can roll back even if files are deleted
python manage.py migrate myapp 0003
# ✓ Works even if 0004.py and 0005.py are gone!

# Inspect stored migrations
python manage.py show_stored_migrations

# Verify stored code matches current files
python manage.py verify_migrations

# Backfill source code for migrations executed before django-rewind was installed
python manage.py backfill_migration_code

# View in Django Admin (optional)
# Visit /admin/django_rewind/migrationcode/
```

---

## Real-World Scenario

Here's a common situation that django-rewind solves:

**Before django-rewind ❌**

```bash
# Feature branch deploys to staging
git checkout feature/add-preferences
python manage.py migrate
# ✓ Migration users.0005_add_preferences applied

# Switch back to main branch
git checkout main
python manage.py migrate users 0004
# ❌ Error: Can't find users/migrations/0005_add_preferences.py
# 😱 Database is stuck in wrong state
# 💔 You're now redeploying branches multiple times or manually writing SQL to fix things
```

**After django-rewind ✅**

```bash
# Feature branch deploys to staging
git checkout feature/add-preferences
python manage.py migrate
# ✓ Migration users.0005_add_preferences applied
# ✓ Code automatically stored in database

# Switch back to main branch
git checkout main
python manage.py migrate users 0004
# ✓ Loading users.0005_add_preferences from stored code
# ✓ Successfully rolled back
# 😎 Back to clean state - no manual SQL needed!
```

With django-rewind, you can switch branches freely without worrying about migration file mismatches! 🎉

### Other Common Scenarios

django-rewind also helps in these situations:

**1. Hotfix Deployment / Urgent Fix Based on Old Commit**

When you need to deploy an urgent fix from an older commit that doesn't have recent migrations:

```bash
# Production has migrations 0001-0010 applied
# You need to deploy commit from before migration 0008 was created
git checkout <old-commit-hash>
python manage.py migrate myapp 0007
# ✓ django-rewind loads 0008, 0009, 0010 from stored code
# ✓ Successfully rolls back to match old codebase
```

**2. Blue/Green Deployment**

In blue/green deployments, you may need to roll back the green environment to match the blue environment's state, even if the codebases differ:

```bash
# Green environment has newer migrations than blue
# Need to sync green back to blue's migration state
python manage.py migrate myapp <blue-migration-number>
# ✓ Missing migrations automatically loaded from stored code
# ✓ Environments stay in sync regardless of codebase differences
```

**3. Production Debugging - Query Stored Code for Exact Truth**

When debugging production issues, you need to know exactly what migration code was executed. Use management commands to inspect stored migrations:

```bash
# List all stored migrations to see what's in the database
python manage.py show_stored_migrations

# Check a specific app
python manage.py show_stored_migrations myapp

# Verify stored code matches current files (or identify mismatches)
python manage.py verify_migrations
```

Or access programmatically for deeper inspection:

```python
from django_rewind.models import MigrationCode

# Get the exact code that was run in production
migration = MigrationCode.objects.get(
    app_label='myapp',
    migration_name='0005_add_index'
)
print(migration.source_code)  # Exact code that modified production DB
print(f"Stored: {migration.stored_at}")  # When it was stored
```

This gives you the definitive source of truth about what actually ran in production, independent of what's in your current codebase.

---

## How It Works

django-rewind works seamlessly behind the scenes:

1. **Storage**: When you run `migrate`, django-rewind automatically captures the migration file's source code
2. **Database**: Stores it in a new table called `django_migrations_code` (separate from Django's own migration tracking)
3. **Rollback**: If a migration file is missing during rollback, django-rewind automatically loads it from the stored code
4. **Execution**: Runs the reverse operations exactly like normal Django migrations—no magic, just stored code

The best part? You don't need to change how you work with migrations. Everything happens automatically! ✨

### Philosophy: Database as the Source of Truth

django-rewind is built on a fundamental principle: **the database is persistent and long-running, while source code is ephemeral and ever-changing.**

In production systems, your database lives for years, accumulating schema changes across countless deployments, feature branches, and rollbacks. Your source code, however, is constantly in flux—branches are merged and deleted, migrations are squashed, files are refactored, and repositories are rewritten. This creates a fundamental mismatch: the database remembers what was applied, but the migration files that created that state may no longer exist.

**The database itself is the authoritative record of what migrations have been applied**. The migration files in your repository are merely the instructions that _were_ executed—they're historical artifacts that may or may not still exist.

django-rewind bridges this gap by storing the migration source code alongside the migration record in the database. This ensures that:

- **The database is self-contained**: It carries both the record of what was applied (`django_migrations`) and the code that was executed (`django_migrations_code`)
- **Rollbacks are always possible**: Even if migration files are deleted, squashed, or lost, the database retains the exact code that was run
- **Branch switching is safe**: You can freely switch between branches without worrying about missing migration files
- **Production resilience**: Your production database can roll back migrations even if the codebase has changed significantly

This approach aligns with the principle that **the database state is the source of truth**, not the migration files in your repository. By storing migration code in the database, django-rewind ensures that your database can always reverse its own history, independent of your source code.

### Architecture

```
┌─────────────────────────────────────┐
│  python manage.py migrate           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  django-rewind intercepts           │
│  1. Captures migration source code  │
│  2. Stores in database              │
│  3. Runs migration normally         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Database now contains:             │
│  • django_migrations (Django)       │
│  • django_migrations_code (rewind)  │
│    - app_label                      │
│    - migration_name                 │
│    - source_code ← THE MAGIC!       │
│    - stored_at                      │
└─────────────────────────────────────┘
```

---

## Django Admin Interface

View and manage stored migrations through Django's familiar admin interface. Navigate to `/admin/django_rewind/migrationcode/` to see all your stored migrations.

**Admin Features:**

- ✓ List all stored migrations with status indicators
- ⚠ See which files are missing from your codebase
- ✗ Detect code mismatches between stored and current files
- 📋 View complete source code
- 📊 Check if migrations are currently applied
- 🔍 Code display with formatting (monospace, scrollable)

> **Note:** The admin interface is read-only by default to prevent accidental modifications to stored migration code.

---

## Tips & Best Practices

- **Install early**: Add django-rewind to your project as soon as possible to start storing migration code
- **Regular verification**: Run `python manage.py verify_migrations` periodically to ensure stored code matches your files
- **Admin inspection**: Use the Django admin to browse stored migrations and see what's been applied
- **Branch safety**: Switch branches with confidence—django-rewind has your back!

---

## Advanced Usage

### Custom Settings

```python
# settings.py
# Disable django-rewind (default: True, enabled by default)
DJANGO_REWIND_ENABLED = False
```

### Management Commands

```bash
# Show all stored migrations
python manage.py show_stored_migrations

# Show for specific app
python manage.py show_stored_migrations myapp

# Verify stored code matches files
python manage.py verify_migrations
```

### Programmatic Access

```python
from django_rewind.models import MigrationCode

# Get stored migration
migration = MigrationCode.objects.get(
    app_label='myapp',
    migration_name='0005_add_field'
)

print(migration.source_code)
print(f"Stored: {migration.stored_at}")
```

---

## Safety & Security

**Non-Invasive:**

- Doesn't modify Django's `django_migrations` table
- Uses separate `django_migrations_code` table
- Can be uninstalled cleanly without affecting Django

**Read-Only Admin:**

- Migration code cannot be edited via admin
- Prevents accidental modifications
- Audit trail of all changes

**Execution Safety:**

- Code is only loaded from database, never user input
- Executes in controlled namespace
- Same security model as Django migrations

---

## Requirements

- Python 3.9+
- Django 3.2+

**Tested with:**

- Django 3.2, 4.2, 5.0, 5.1
- PostgreSQL, MySQL, SQLite
- Python 3.9, 3.10, 3.11, 3.12

**Note:** Django 5.0 and 5.1 require Python 3.10+. For Django 3.2 and 4.2, Python 3.9+ is sufficient.

---

## Documentation

For more information, see:

- **[Contributing Guide](./CONTRIBUTING.md)** - How to contribute and develop
- **[Changelog](./CHANGELOG.md)** - Version history and changes

---

## Contributing

We'd love your help! Contributions are welcome and appreciated. Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

### Development Setup

We recommend using [uv](https://github.com/astral-sh/uv) for fast dependency management, but pip works too:

**Using uv (recommended):**

```bash
# Clone the repository
git clone https://github.com/HartBrook/django-rewind.git
cd django-rewind

# Install dependencies
uv sync --extra dev

# Run tests
uv run pytest
```

**Using pip:**

```bash
# Clone the repository
git clone https://github.com/HartBrook/django-rewind.git
cd django-rewind

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

For more details, see [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## FAQ

**Q: Does this work with squashed migrations?**  
A: Yes! Squashed migrations are stored just like regular migrations. No special handling needed.

**Q: What happens to old stored migrations?**  
A: They stay in the database indefinitely. You can clean them up manually if needed, but there's no harm in leaving them.

**Q: Can I use this in production?**  
A: Absolutely! It's designed for production use. It's non-invasive, backwards compatible, and adds minimal overhead.

**Q: Does this slow down migrations?**  
A: The performance impact is negligible — it just reads the migration file and inserts one database row. You won't notice any difference.

**Q: What if I manually edit the database?**  
A: django-rewind can't help with manual database changes. Always use Django migrations for schema changes!

**Q: Can I disable storing for certain apps?**  
A: Not yet, but it's on the roadmap. For now, it's all-or-nothing. If you need this feature, please open an issue!

**Q: What databases are supported?**  
A: All databases that Django supports! We've tested with PostgreSQL, MySQL, and SQLite.

**Q: Is this safe to use?**  
A: Yes! It uses the same security model as Django migrations. Code is only loaded from the database, never from user input.

---

## Roadmap

- [ ] v0.1.0 - MVP release (storage + rollback)
- [ ] v0.2.0 - Migration conflict resolution

---

## Credits

Created by Cody Hart

Inspired by the collective pain of Django developers everywhere who've had to clean up migrations at the worst possible moment.

Special thanks to:

- Django core team for the excellent migrations framework
- Everyone who's ever manually fixed a broken migration state

---

## License

MIT License - see [LICENSE](./LICENSE) for details

---

## Support

Need help? We're here for you!

- **🐛 Found a bug?** [Open an issue](https://github.com/HartBrook/django-rewind/issues)
- **💡 Have a question?** [Start a discussion](https://github.com/HartBrook/django-rewind/discussions)
- **📧 Email:** mrcodyhart@gmail.com

We welcome feedback, suggestions, and contributions!

---

⏪ **django-rewind** - Because migrations should work forwards _and_ backwards, always.

```bash
pip install django-rewind
```

## ⚠️ Important Warning

**django-rewind modifies Django's migration execution flow.** While designed to be safe and non-invasive:

- ✅ **Always backup your database** before using in production
- ✅ **Test thoroughly** in staging environments first
- ✅ **Review stored migration code** before rollbacks
- ⚠️ **This software is provided "as-is"** without warranty of any kind

The author is not responsible for data loss. See [LICENSE](./LICENSE) for details.
