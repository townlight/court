# Changelog

## [Unreleased]

### Added

- Suite-wide release-recovery status, audit-full packet, browser QA evidence, and regression checks that keep the published v0.1.2 label provisional.

### Changed

- Replaced the unresolved `civiccore==0.4.0` package dependency with the published CivicCore v0.4.0 release wheel so fresh installs do not rely on a hidden CI preinstall step.
- Updated release verification to prefer `python3` before `python` and removed the WindowsApps fallback from the WSL/Ubuntu release path.

## [0.1.2] - 2026-04-29

### Added

- Bearer-token auth and role checks for persisted court form and hearing prep retrieval via `CIVICCOURT_AUTH_TOKEN_ROLES` and `civiccore.auth`.

### Changed

- Moved CivicCourt to `civiccore==0.4.0` so persisted retrieval protection consumes the published shared auth helper instead of a module-local bridge.
- Updated CI, release verification, docs, runtime tests, and public UI copy for the v0.1.2 dependency and auth boundary.

## [0.1.1] - 2026-04-28

### Added

- Optional SQLAlchemy-backed court form and hearing-prep workpaper records via `CIVICCOURT_WORKPAPER_DB_URL`.
- Court form and hearing-prep retrieval endpoints for persisted records.

### Changed

- Dependency-alignment release: moved CivicCourt to `civiccore==0.3.0` while preserving the existing v0.1.0 runtime foundation behavior.
- Updated CI, verification gates, package metadata, docs, runtime tests, landing page, and public UI labels for the v0.1.1 release.

## [0.1.0] - 2026-04-27

### Added

- CivicCourt runtime foundation with FastAPI health, root, public UI, and deterministic API endpoints.
- Procedure Q&A, court form drafts, restricted-record-aware search, and hearing preparation checklist helpers.
- Professional docs, browser QA artifacts, GitHub community templates, placeholder-import gate, release gate, and package build.
