# ✅ Support Matrix

This document defines the officially supported environments for this project.

> **Policy**
- Only environments listed below are guaranteed support.
- Non-listed environments may work but are **best-effort** only.
- Breaking support changes are announced in `CHANGELOG.md` and follow the project's `RELEASE_POLICY.md`.

---

## 🐍 Python Version Support

| Python Version | Status | End of Support | Notes |
|----------------|--------|----------------|-------|
| 3.13 | ✅ Supported | TBD | Latest stable |
| 3.12 | ✅ Supported | Oct 2028 | Primary CI target |
| 3.11 | ✅ Supported | Oct 2027 | |
| 3.10 | ⚠️ Maintenance | Oct 2026 | Bug-fixes only |
| < 3.10 | ❌ Unsupported | — | No fixes or builds |

---

## 🖥️ Operating System Compatibility

| OS | Status | Notes |
|----|--------|------|
| Ubuntu 22.04+ | ✅ Fully supported |
| Ubuntu 20.04 | ⚠️ Limited support |
| macOS 13+ (ARM & Intel) | ✅ Supported |
| macOS 12 | ⚠️ Limited | Only critical fixes |
| Windows 11 (WSL recommended) | ✅ Supported |
| Windows native | ⚠️ Partial | No guarantee for low-level tooling |

> Schedule:  
Support aligned with **Python EOL** + minimum 18 months security tail.

---

## 📦 Dependency Compatibility

| Category | Policy |
|---------|--------|
Major dependency upgrades | Allowed only in **minor** or **major** release |
Pinned dev deps | ✅ Required |
Runtime deps | **Minimum supported version policy** (see pyproject) |
Removed/Breaking deps | Must follow `DEPRECATION_POLICY.md` |

---

## 🧪 CI Test Matrix

| Category | Matrix |
|---------|--------|
Python | 3.10, 3.11, 3.12, 3.13 |
OS | Ubuntu, macOS, Windows (WSL preferred) |
Architectures | amd64, arm64 |

---

## 📅 Review Cycle

| Item | Cadence |
|------|--------|
Matrix update | Every 6 months |
EOL software removal | With notice per `DEPRECATION_POLICY.md` |
Security dependency scan | Continuous + weekly scheduled job |

---

## ❓ Questions

For environment-specific concerns, open a **Support Request**:  
➡️ `.github/ISSUE_TEMPLATE/support.yml`