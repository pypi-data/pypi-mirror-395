# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-12-07

### Added

- Initial release
- Migration code storage in database
- Rollback support for deleted migration files
- Django Admin interface for viewing stored migrations
- Management commands: `show_stored_migrations`, `verify_migrations`, and `backfill_migration_code`
- Support for Django 3.2, 4.2, 5.0, 5.1
- Support for Python 3.9, 3.10, 3.11, 3.12

[Unreleased]: https://github.com/HartBrook/django-rewind/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/HartBrook/django-rewind/releases/tag/v0.1.0
