# 📊 Risk Register

A living document to track risks, mitigation strategies, and monitoring actions.

| ID | Category | Description | Impact | Likelihood | Owner | Mitigation | Status |
|---|---|---|---|---|---|---|---|
| R-001 | Security | Dependency vulnerability in critical library | High | Medium | <OWNER> | Scheduled scans, pip-audit CI | Monitoring |
| R-002 | Supply Chain | Tampered package or dependency | High | Low | <OWNER> | Sigstore signing, OIDC deploys, SBOM | Mitigated |
| R-003 | Performance | Slow startup on large projects | Medium | Medium | <OWNER> | Profiling + lazy-load modules | Open |
| R-004 | People | Single-maintainer risk | High | High | Dhruv13x | Contributor onboarding + CODEOWNERS | In Progress |
| R-005 | Licensing | Incoming contributions with incompatible licenses | Medium | Low | <OWNER> | License scan + CLA | Monitoring |
| R-006 | Reliability | CI/CD pipeline failure blocks releases | High | Medium | <OWNER> | Redundancy + GitHub backup mirrors | Monitoring |

### 🔁 Review Cadence

| Frequency | Reviewers |
|---|---|
Quarterly | Maintainers, Security team  

### 📌 Notes

- New risks logged via issue label `type: risk`
- Risks reassessed every release cycle
- Ties to `SECURITY.md` and `RELEASE_POLICY.md`