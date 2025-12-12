# Changelog

## [2.0.0] - 2025-12-06

### Changed
- Modernize Django support (3.2+)
- Update Python support (3.8+)
- Replace deprecated `unique_together` with `UniqueConstraint`
- Update `Signal` API (remove deprecated `providing_args`)
- Fix app configuration name
- Add `default_auto_field` to AppConfig
- Update dependencies: Django >=3.2, channels >=4.0

### Migration
- New migration file for constraint updates
