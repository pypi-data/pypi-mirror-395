# 📦 Dependency Management Policy

This document defines the official policy for managing dependencies to ensure
security, stability, reproducibility, and long-term maintainability.

Maintainer: Dhruv13x  
Applies to: All tools & libraries under this organization

---

## 🎯 Goals

- Ensure secure and trusted supply chain
- Guarantee reproducible builds
- Minimize dependency footprint & attack surface
- Prevent dependency drift & ecosystem risk
- Ensure timely updates and CVE patches

---

## 📐 Principles

| Policy | Standard |
|---|---|
🚫 Avoid unnecessary dependencies | Prefer stdlib first  
✅ Use version ranges | `>=x,<y` not `*`  
📌 Lock reproducible environments | `uv` / `pip-tools` / hashes  
🛑 Block unmaintained or deprecated packages | Verified before adoption  
🔐 Enforce security scanning | SCA + SBOM + signing  
♻️ Regular upgrade cadence | monthly + quarterly reviews  

---

## 📦 Dependency Classification

| Type | Description | Policy |
|---|---|---|
**Runtime deps** | Required in production | Keep minimal, vetted |
**Optional extras** | CLI / docs / plugins | Must remain optional |
**Dev deps** | Test, lint, build | Pin and review monthly |
**Transitive deps** | Pulled indirectly | Must be inspected quarterly |

---

## ✅ Allowed Sources

- PyPI (trusted publishing only, OIDC preferred)
- GitHub releases (tagged & signed only)
- Internal private registry (if configured)

❌ No direct `git+http` or unknown mirrors  
❌ No vendored binaries without signature verification

---

## 🔐 Security Requirements

All dependencies MUST pass:

| Check | Tool |
|---|---|
SBOM generation | `cyclonedx-bom`  
CVE scanning | `pip-audit --strict`  
Signing (where possible) | Sigstore / OIDC  
Reputation check | Community adoption, maintenance status  

High-risk packages are **prohibited** (crypto libs, shell runtimes, unmaintained libs, abandonware).

---

## ⛔ Disallowed Practices

- Wildcard versions (`*`, no upper bound)
- Direct installs from arbitrary URLs
- Running dependency code during install (avoid unsafe setup hooks)
- Vendoring w/o license + security checks
- Adding heavy dependencies without architectural need

---

## 🔄 Upgrade & Review Cadence

| Frequency | Task |
|---|---|
Monthly | Dev dependencies & tooling bump  
Quarterly | Runtime deps review, transitive audit  
Every release | SBOM regen, pip-audit, hash update  
Annual | Supply-chain audit & dependency pruning  

---

## 📁 Tools

| Function | Tool |
|---|---|
Locking | `pip-tools` OR `uv` lock  
Vulnerabilities | `pip-audit`  
SBOM | `cyclonedx`  
Integrity | `sigstore`  
Formatting | `pyproject-fmt`  

---

## 🧪 Testing Requirements

Before merging dependency changes:

- ✅ CI passes
- ✅ Static typing & lint pass
- ✅ CVE scan clean
- ✅ No regression in code size / performance

---

## ✅ Enforcement

All merges modifying dependencies MUST be reviewed by a maintainer.

CI will block merges if:

- CVEs found
- signatures missing
- SBOM not updated (for tagged release)
- lockfile not updated (if used)

---

## 📎 Notes

This repo follows **minimal dependency philosophy** — simplicity, security, and performance first.