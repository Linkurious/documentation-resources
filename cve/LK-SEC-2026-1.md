# LK-SEC-2026-1

## Timeline
- 2026-10-21 [CVE-2026-111497](https://www.cve.org/CVERecord?id=CVE-2026-111497) is published (Brotli vulnerability)
- 2026-10-21 Node.js releases a security release fixing [CVE-2026-111497](https://www.cve.org/CVERecord?id=CVE-2026-111497) ([source](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases))
- 2026-10-22 Linkurious releases Linkurious Enterprise v4.3.14 fixing [CVE-2026-111497](https://www.cve.org/CVERecord?id=CVE-2026-111497)
- 2026-10-23 Linkurious notifies all customers about the security fix ([source](https://resources.linkurious.com/linkurious-enterprise-4.3.14-security-improvements-with-node.js))

## Description
Vulnerability in a dependency of Node.js, which is the server framework of Linkurious Enterprise.

## Impact
A remote unauthenticated attacker can corrupt adjacent decoder state memory, disclose sensitive memory contents, 
cause a denial of service, or potentially execute arbitrary code using a crafted Brotli-compressed stream. ([see details](https://www.sysdig.com/blog/node2shell-cve-2026-111497-detecting-the-node-js-brotli-rce))

## Severity: high
- CVSS v3.1 score: `7.3` (see [score details](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator?vector=AV:L%2FAC:H%2FPR:H%2FUI:R%2FS:U%2FC:N%2FI:N%2FA:H%2FE:U%2FRL:O%2FRC:C%2FCR:H%2FIR:M%2FAR:M%2FMAV:L%2FMAC:H%2FMPR:H%2FMUI:R%2FMS:U%2FMC:N%2FMI:N%2FMA:H&version=3.1) and [severity rules](https://doc.linkurious.com/admin-manual/latest/vulnerabilities/#severity-levels)).
- Patch required.

## Who is affected?
All versions of Linkurious Enterprise up to v4.3.13 (included).

## How can it be patched?
- Upgrade to Linkurious Enterprise v4.3.14
