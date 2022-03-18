# LK-SEC-2022-1

## Timeline
- 2022-03-16 The vulnerability is disclosed and patched by OpenSSL with the release of OpenSSL 1.1.1n
- 2022-03-17 The vulnerability is patched by Node.js with the release of Node.js 14.19.1
- 2022-03-18 Linkurious discloses this document

## Description
Denial of Service vulnerability of OpenSSL in Node.js: [CVE-2022-0778](https://nvd.nist.gov/vuln/detail/CVE-2022-0778)

## Impact
If an administrator configures Linkurious Enterprise to connect to an external component (e.g. Neo4j, Elasticsearch) over SSL, 
and if the external component has been configured to use a malicious SSL certificate, then Linkurious Enterprise will crash.

## Severity: low
- CVSS v3.1 score: `3.5` (see [score details][score]).
- No patch is necessary.

## Who is affected?
Linkurious Enterprise version: v2.10.* and v3.0.0 to v3.0.10.

## How can it be patched?
- Not patch is necessary.
- A fix will be provided as part of the next patch version of Linkurious Enterprise v3.0

[score]: https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator?vector=AV:L/AC:H/PR:H/UI:R/S:U/C:N/I:N/A:H/E:U/RL:O/RC:C/CR:H/IR:M/AR:M/MAV:L/MAC:H/MPR:H/MUI:R/MS:U/MC:N/MI:N/MA:H&version=3.1
