# Changelog

All notable changes to the HLA-Compass SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Schema discovery API: `self.data.sql.schema()`, `tables()`, `columns()`, `describe()`
- CLI commands: `hla-compass data schema`, `hla-compass data tables`
- `py.typed` marker for PEP 561 type checker support
- Shell completion support via Click

### Changed
- Pydantic-first module development: `Input` model is now the recommended way to define inputs
- Golden example updated to demonstrate Pydantic `Input` pattern
- Improved error messages with links to documentation

### Fixed
- Removed debug print statements from CLI modules

## [2.0.0] - 2024-11-XX

### Added
- `DataClient` with scoped SQL and Storage access
- `ModuleTester.quickstart()` for rapid testing
- Pydantic `Input` model support for typed inputs
- `hla-compass preflight` command for manifest sync
- Storage helpers: `save_json`, `save_csv`, `save_excel`

### Changed
- Module execution now uses `RuntimeContext` with typed properties
- Manifest schema auto-generated from Pydantic models

## [1.0.0] - 2024-XX-XX

- Initial public release
