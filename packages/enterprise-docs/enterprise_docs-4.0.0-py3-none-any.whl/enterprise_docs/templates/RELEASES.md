# 📦 Release & Versioning Policy

This project follows **Semantic Versioning (SemVer)**:

> MAJOR.MINOR.PATCH

| Type | Meaning |
|------|--------|
| MAJOR | Breaking changes, architecture migrations |
| MINOR | New features, improvements, deprecations |
| PATCH | Bug fixes, performance improvements, documentation |

No breaking changes are permitted in MINOR or PATCH releases.

---

## 🔐 Release Security Requirements

All releases **must comply with OpenSSF recommended practices**:

- ✅ Reproducible builds (`pyproject.toml`)
- ✅ PyPI publishing via **OIDC / Trusted Publisher**
- ✅ SBOM generation (CycloneDX)
- ✅ Sigstore signing of artifacts
- ✅ Build provenance attestation
- ✅ CI-verified environment (no local publishing)

No manual uploads or credentials stored in CI.

---

## 🧪 Pre-Release Checklist

Before creating a release tag:

### ✅ Code Quality
- [ ] All tests passing
- [ ] No increase in failing checks
- [ ] Coverage ≥ 90%
- [ ] Lint clean (ruff, mypy, black)
- [ ] Docs updated for API changes
- [ ] Changelog updated

### ✅ Security
- [ ] `pip-audit` passes (no known CVEs)
- [ ] `detect-secrets` passes
- [ ] No high severity Bandit findings
- [ ] Dependencies reviewed

### ✅ Packaging
- [ ] `python -m build` succeeds locally
- [ ] `twine check dist/*` passes

---

## 🚀 Release Process

### 1️⃣ Prepare version

Update `CHANGELOG.md`:

vX.Y.Z — YYYY-MM-DD

Added

Changed

Fixed

Security

### 2️⃣ Commit & Tag

git commit -am "release: vX.Y.Z" git tag vX.Y.Z git push origin main --tags

Tag triggers GitHub Actions.

### 3️⃣ GitHub Actions handles:

- ✅ Clean virtual build environment
- ✅ Build wheel & sdist
- ✅ Metadata validation
- ✅ Security audit
- ✅ Generate SBOM (`sbom.json`)
- ✅ Sigstore sign artifacts
- ✅ Publish to PyPI via OIDC
- ✅ Generate provenance attestation

---

## 🔄 Post-Release Steps

- [ ] Verify release on PyPI
- [ ] Publish release notes (GitHub Releases UI)
- [ ] Publish docs site (if applicable)
- [ ] Announce in project channels (optional)

---

## 🔒 Emergency & Security Fixes

Security hotfixes **may bypass feature freeze**, but must:

- Patch only vulnerable code
- Ship immediately after fix + tests
- Backport if needed to prior supported branch

---

## 📅 Release Cadence

| Release Type | Frequency |
|-------------|-----------|
Patch | As needed (bug/security)
Minor | ~ Monthly or based on feature readiness
Major | Rare, planned, documented migration path

---

## 🧯 Deprecated Features

All removals require:

- Deprecation warning for 1 MINOR release
- Clear documentation in CHANGELOG
- Migration guidance

---

## 🛟 Supported Versions

| Version | Status |
|--------|--------|
Latest Major | ✅ Fully supported
Previous Major | ⚠️ Security fixes only
Older | ❌ Unsupported

Maintainers may accelerate policy for security concerns.

---

## ✨ Provenance & Trust

All artifacts are:

| Integrity Feature | Enabled |
|------------------|--------|
Signed (Sigstore) | ✅
SBOM Attached | ✅
Provenance Attested | ✅
Reproducible Build | ✅
Verified CI Source | ✅

Users can verify releases using instructions in `SECURITY.md`.

---

## 🧩 Example Verification

cosign verify-blob --certificate dist/.sigstore.pem dist/.whl

---

## 🙋 Questions?

Open a GitHub Discussion or Issue.  
Security concerns → email in `SECURITY.md`.

---

_This release process enforces reliability, security, and traceability across all published versions._


---
