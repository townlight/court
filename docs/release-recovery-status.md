# CivicCourt Release-Recovery Status

Date: 2026-05-07

## Status

CivicCourt `0.1.2` is a published foundation label under suite-wide release-recovery review. It is not product-ready and must not be promoted as production municipal court software.

## Current Runtime Boundary

The current package provides cited procedure-answer drafts, review-required court form drafts, restricted-record-aware sample search, hearing-prep checklists, optional local court workpaper persistence, bearer-role protection for persisted retrieval, and a public sample UI at `/civiccourt`.

It does not replace court case management, issue warrants, file documents, decide cases, provide legal advice, call live LLMs, or integrate with live court CMS systems.

## Recovery Evidence

- WSL-native release verification passed through `scripts/verify-release.sh`: `19 passed`, docs gate passed, placeholder import check passed, Ruff passed, and build artifacts/checksums were created.
- Fresh install proof resolved CivicCore from the published v0.4.0 release wheel without a hidden CI preinstall: `CivicCore: 0.4.0`, `CivicCourt: 0.1.2`, `WSL platform: linux`.
- Browser QA covered `docs/index.html` at desktop 1440 x 1000 and mobile 390 x 844 with console, overflow, and keyboard-focus checks.
- Documentation gates reject stale product-ready language, the old shipping badge, and browser mojibake.

## Promotion Rule

Do not call CivicCourt finished, shippable, production-ready, or product-ready until a later active-module sprint implements the full CivicCourt v1.0.0 definition of done and passes the release gate.
