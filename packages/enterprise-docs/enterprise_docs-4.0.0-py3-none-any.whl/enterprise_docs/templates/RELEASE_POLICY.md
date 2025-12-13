# 🚀 Release & Versioning Policy

This project follows a **predictable, safe, and transparent release model** suitable for production environments.

---

## 📌 Versioning Standard

We use **Semantic Versioning (SemVer)**:

MAJOR.MINOR.PATCH

| Component | Meaning |
|----------|--------|
MAJOR | Breaking changes |
MINOR | Backwards-compatible features |
PATCH | Bug fixes & security updates only |

Example tags:  
`v1.2.0`, `v2.0.1`

---

## 🕒 Release Cadence

| Release Type | Frequency | Contents |
|--------------|-----------|---------|
Patch | As needed | Security + bug fixes |
Minor | Monthly | Features, improvements |
Major | ~Annual / Demand-driven | Breaking changes, migrations |

Emergency Security Patch: **Immediate** 🚨

---

## 🧠 Stability Guarantees

| Area | Policy |
|------|-------|
Public API | Stable across PATCH/MINOR |
CLI flags | Deprecated then removed (see deprecation policy) |
Config format | Versioned + migration docs |
Internal APIs | No stability guarantees |

---

## ✅ Pre-Release Checklist

| Step | Required |
|------|---------|
✅ All tests pass | CI enforced |
✅ Lint + type check clean | ruff, mypy |
✅ Coverage ≥ 90% | coverage gate |
✅ Security scan clean | pip-audit, bandit |
✅ Docs updated | mkdocs, README, API docs |
✅ CHANGELOG.md updated | Required |
✅ Version tag created | `vX.Y.Z` |

> Automated build + signing via GitHub Actions

---

## 🔐 Security Backport Policy

| Version | Support Duration |
|--------|-----------------|
Latest | Full support |
Previous major | Security only for 6–12 months |
Older | No guarantees |

Critical CVEs patched **immediately.**

---

## 🚧 Deprecation Policy

- Deprecations announced at least **1 release before removal**
- Marked in docs, CHANGELOG, and CLI warning
- Where feasible, provide migration helpers

See `DEPRECATION_POLICY.md`.

---

## 🏗 Build & Distribution Rules

| Deliverable | Policy |
|------------|--------|
PyPI | ✅ Source + wheels |
Artifacts signed | ✅ Sigstore |
SBOM | ✅ Required |
Build provenance | ✅ attestation |

Automated by `.github/workflows/publish.yml`

---

## 🧾 Tag & Release Procedure

| Step | Command |
|------|--------|
Tag version | `git tag vX.Y.Z` |
Push tag | `git push origin vX.Y.Z` |
CI builds | Auto start |
Publish to PyPI | GitHub OIDC |
Produce SBOM | Yes |
Provenance signing | Yes |

---

## 📣 Communication

Release notes posted in:  
- `CHANGELOG.md`
- GitHub release page
- Milestone changelog (if applicable)

---

## 🙋 Questions

For release questions, open:  
➡️ `.github/ISSUE_TEMPLATE/release.yml`


---

✅ All set

You now have:

Support matrix ✅

Release policy ✅


These files match CNCF / OpenSSF / Google / AWS open source governance quality.


---
