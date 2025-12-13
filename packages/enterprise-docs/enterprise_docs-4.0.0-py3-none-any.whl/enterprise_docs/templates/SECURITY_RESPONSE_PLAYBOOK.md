# 🛡️ Security Incident Response Playbook

This document guides coordinated security incident handling.

## 🚨 Incident Severity Levels

| Level | Definition | Response Target |
|---|---|---|
High | CVE / exploit / package compromise | 24 hours |
Medium | Scoped vulnerability / disclosure | 72 hours |
Low | Minor issue, no exposure | 7 days |

---

## 📣 Reporting Channels

- 📨 Email: security@<domain>
- 🔏 Sensitive issue: GitHub → **Security Advisories**
- 🛠️ <PRIVATE> team only

---

## 👥 Roles & Responsibilities

| Role | Responsibility |
|---|---|
Incident Commander | Maintains timeline, decisions |
Security Lead | Technical response, patching |
Comms Lead | Stakeholder messaging |
Ops | Logs, infrastructure, SBOM updates |

(For solo-maintainer mode: Dhruv13x plays all roles)

---

## 🧾 Response Workflow (SIRT Model)

| Phase | Actions |
|---|---|
Identification | Validate report, classify severity |
Containment | Revoke tokens, disable affected services |
Eradication | Patch vulnerability, remove malicious code |
Recovery | Release fixed version, restore confidence |
Post-mortem | Publish advisory & lessons learned |

---

## 🧩 Tools & Controls

- 📦 Pip-audit + Dependabot
- 🔐 OIDC trusted publishing
- ✅ Sigstore signing
- 🧬 CycloneDX SBOM
- 🛡️ detect-secrets

---

## 📜 Communication Templates

**Security Advisory Draft**

> Title: SECURITY PATCH — <Issue Summary>  
> Patched in: vX.Y.Z  
> Severity: <Low/Med/High>  
> Description:  
> Fix Summary:  
> Action for Users: `pip install --upgrade <package>`  

---

## 🧠 Lessons Learned Template

| What happened | Why | Fix | Prevention |
|---|---|---|---|

---

## 🏁 Closure Criteria

- Patch released  
- Advisory published  
- SBOM updated  
- Risk Register entry updated