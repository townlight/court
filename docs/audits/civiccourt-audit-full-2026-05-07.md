# CivicCourt Audit-Full Packet

Date: 2026-05-07
Repo: `CivicSuite/civiccourt`
Mode: release-recovery gate
Local commit audited before fixes: `bc8f0e4ca804b72c2f31117c97a666a4428d80da`

## 1. Executive Audit

Static audit confidence: High for release-script, docs, dependency, auth boundary, and tests inspected locally.
Runtime sign-off confidence: High for this release-recovery scope after WSL release verification and browser QA passed.

CivicCourt does not claim v1.0.0, but its release evidence had trust gaps: `pyproject.toml` depended on unresolved `civiccore==0.4.0` while CI preinstalled the wheel, WSL verification could choose `python` before `python3`, and docs used a first-viewport "Shipping v0.1.2" badge instead of provisional release-recovery language.

## 2. Audit Coverage Ledger

| Area | Status | Evidence |
|---|---|---|
| Engineering | Checked | `pyproject.toml`, `.github/workflows/verify.yml`, `civiccourt/main.py`, `civiccourt/public_ui.py` |
| Security and authorization | Checked | persisted retrieval auth tests and `CIVICCOURT_AUTH_TOKEN_ROLES` boundary |
| UI/UX | Checked | static docs updated; Playwright desktop/mobile browser QA passed |
| Product/PM | Checked | provisional foundation label added |
| Documentation | Checked | README, text docs, manual, changelog, docs index, recovery status |
| Install/bootstrap/seeding | Checked | dependency changed to published CivicCore v0.4.0 wheel |
| Version/release consistency | Checked | version remains `0.1.2`; no v1 promotion |
| Test engineering | Checked | regression tests added for release verifier, docs gate, dependency, and recovery copy |
| Runtime QA | Checked | WSL release gate passed; browser QA passed |
| Cross-cutting synthesis | Checked | main issue class is release evidence and status truth |

## 3. Claim Verification Matrix

| Claim | Result | Evidence |
|---|---|---|
| CivicCourt is not product-ready | Verified static | README/manual/recovery status |
| Version remains `0.1.2` | Verified static | package, pyproject, release script |
| Fresh install can resolve CivicCore | Verified | WSL temp venv installed `civiccore-0.4.0` and `civiccourt-0.1.2` |
| Persisted retrieval requires bearer-role auth | Verified static/test | existing auth tests cover 401/403/503/404 paths |
| Browser docs are readable | Verified | Playwright desktop/mobile QA passed with no console/page errors |

## 4. What The Dev Team Needs To Do Now

1. Push the recovery branch.
2. Open a PR.
3. Confirm GitHub CI runs the release gate without a hidden CivicCore preinstall.
4. Merge only after CI is green.

## 5. Next-Sprint Watchlist

- Full CivicCourt v1.0.0 scope remains future active-module work.
- Any future production claim must include real user-flow Playwright tests, runtime install proof, consistency gates, docs-source enforcement, and security scans.

## 6. Engineering Deep Dive

Finding ENG-001
Severity: Critical
Confidence: High
Evidence type: Static
Status: Durable defect
Why it matters: A package should install from its declared metadata without CI quietly installing a missing dependency first.
Evidence: `pyproject.toml` used `civiccore==0.4.0`; workflow separately installed the CivicCore wheel.
Blast radius: Fresh installs, CI trust, WSL release proofs.
Fix: Use the published CivicCore v0.4.0 release wheel directly and allow Hatch direct references.

## 7. Security And Authorization Deep Dive

Existing persisted retrieval auth is meaningful for this foundation scope: anonymous requests return 401, missing auth configuration returns actionable 503, unauthorized roles return 403 in the shared CivicCore helper path, and missing records return 404. This recovery patch does not expand auth scope.

## 8. UI/UX Deep Dive

Finding UX-001
Severity: Major
Confidence: High
Evidence type: Static
Status: Durable defect
Why it matters: First-viewport release labels shape public trust.
Evidence: `docs/index.html` displayed "Shipping v0.1.2".
Blast radius: Public docs and status interpretation.
Fix: Replace with "v0.1.2 foundation under recovery review" and add browser QA.

## 9. Product/PM Deep Dive

The current module is useful as a deterministic foundation but is not production court software. It lacks court CMS integration, filing, warrant issuance, judicial workflows, SSO, approval queues, and production court deployment proof.

## 10. Documentation Deep Dive

Docs now state the provisional foundation label and keep unshipped court capabilities out of available/current wording.

## 11. Install / Bootstrap / Seeding Deep Dive

Finding BOOT-001
Severity: Critical
Confidence: High
Evidence type: Static
Status: Durable defect
Why it matters: Hidden install steps make release evidence non-repeatable.
Evidence: CI preinstalled CivicCore before package install.
Blast radius: New users, CI, release gates.
Fix: Remove hidden preinstall and let the package dependency resolve the release wheel.

## 12. Version And Release Consistency Deep Dive

Version remains `0.1.2`. This patch does not promote CivicCourt to v1.0.0.

## 13. Test Engineering Deep Dive

Regression tests cover Python launcher ordering, removal of WindowsApps fallback, direct CivicCore wheel dependency, docs gate markers, docs recovery copy, and public UI dependency/recovery wording.

## 14. Runtime QA Deep Dive

WSL fresh install resolved CivicCore from the published v0.4.0 wheel and imported `civiccourt==0.1.2` on Linux. WSL `scripts/verify-release.sh` passed with `19 passed`, docs gate passed, placeholder import check passed, Ruff passed, and build artifacts/checksums created. Playwright Chromium verified the recovery docs at desktop and mobile widths with no console errors, page errors, mojibake, stale shipping badge, or horizontal overflow; keyboard focus reached the recovery evidence link.

## 15. Cross-Cutting Synthesis

CivicCourt's main recovery issue is evidence trust. The auth and sample court boundaries are clearer than many scaffold modules, but the release/install proof still needed hardening.

## 16. Verification Gaps And Sign-Off Limits

This packet does not certify CivicCourt as product-ready. It certifies only that the current published foundation label is truthfully represented and locally verifiable for the release-recovery scope.
