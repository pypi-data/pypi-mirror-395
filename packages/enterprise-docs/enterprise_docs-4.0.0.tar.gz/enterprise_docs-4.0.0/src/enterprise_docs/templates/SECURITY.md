# 🔐 Security Policy

## 📣 Reporting Security Issues

We take security vulnerabilities seriously.  
If you believe you have found a security issue, please **do not open a public issue**.

Instead, contact us privately at:

- Security Contact: <security@yourdomain.com>  
- Maintainer: <dhruv13x@gmail.com>

We will acknowledge receipt within **48 hours** and provide a status update within **5 business days**.

Please include:

- Description of the vulnerability
- Steps to reproduce / proof-of-concept (if available)
- Affected versions & environment details
- Suggested remediation (optional)

### ✅ Responsible Disclosure

We follow coordinated disclosure best practices:

- Do **not** publicly disclose until we release a fix or provide guidance
- Avoid testing in production environments without consent
- No exploitation, destruction, or tampering of real data

We do not support bounty programs yet, but contributors are credited in advisories.

---

## 🛠️ Supported Versions

We provide security fixes only for supported versions:

| Version | Status |
|--------|--------|
| Latest release | ✅ Supported |
| Previous minor release | ✅ Critical fixes only |
| Older releases | ❌ Security updates not guaranteed |

For long-term enterprise use, lock versions and track SBOMs.

---

## 🧰 Security Practices

Our projects follow modern software-supply-chain security guidelines:

| Practice | Status |
|---------|--------|
| PyPI Trusted Publishing (OIDC) | ✅ |
| SBOM (CycloneDX) | ✅ Provided in releases |
| Build Provenance (Sigstore) | ✅ |
| Dependency Audits (`pip-audit`) | ✅ |
| Secret Scanning (`detect-secrets`) | ✅ |
| Code Quality (Ruff, MyPy, Black) | ✅ |
| Continuous Testing | ✅ |
| Commit Signing Recommended | ✅ |
| Reproducible Builds | ✅ |
| No vendor lock-in | ✅ |

---

## 🔐 Cryptographic Verification

All release artifacts may be verified using:

- **Sigstore** signatures  
- **Build Attestation** metadata  
- `sbom.json` (CycloneDX) included in release assets

Instructions will be provided per-project in README.

---

## 📦 Dependency & SBOM Policy

We generate and publish SBOMs for transparency.  
Users are encouraged to:

- Review SBOMs before deployment
- Use pinned dependencies or lockfiles
- Run independent `pip-audit` scans
- Use container isolation or venvs

Enterprise deployments should also monitor CVE feeds.

---

## 🧾 Security Advisory Process

If a vulnerability is confirmed, we will:

1. Assign CVE (if appropriate)
2. Prepare patch and validation
3. Coordinate release timeline with the reporter
4. Publish advisory in GitHub Security Advisories
5. Update docs, changelog, and release notes

---

## 🤝 Third-Party Dependencies

We review third-party packages for:

- License compatibility  
- Security posture  
- Maintenance activity  

Projects will include a NOTICE file if required.

---

## 📄 Legal

- Submitting a report does **not** create any contractual obligations
- Security testing must comply with applicable laws
- We reserve the right to refuse reports that are malicious, spam, or vague

---

## ❤️ Thank You

We appreciate responsible security research — ethical disclosure protects users and the ecosystem.

Thank you for helping keep our software safe and secure!