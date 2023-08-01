<!-- omit in toc -->
# Linkurious Enterprise migration to v4.0 guidelines

If you are planning to migrate your Linkurious Enterprise instance from an older version to v4.0,
this document will provide you extra details of what you need to take care or do for a successful upgrade.

<!-- omit in toc -->
# Table of contents
- [General major changes](#general-major-changes)
  - [New multi model alerts](#new-multi-model-alerts)
  - [Shared Spaces](#shared-spaces)
  - [Security updates](#security-updates)
- [Dropped Support section](#dropped-support-section)

# General major changes

## New multi model alerts

The `Alerts` feature has evolved and an alert can now contain multiple cypher queries to improve deduplication across cases.

***Impacted clients:***

- Everyone using `Alerts`

***Benefits:***

- Enhanced deduplication across cases with multiple cypher queries per alert
- Better business indicators with a dedicated query to process alerts columns
- Up to 40 custom columns per alert
- Alerts can be run manually directly through the interface

***Impacts:***

When migrating to alerts 4.0 there are a few changes that will be applied to alerts’ already existing matches, queries and case attributes.
**Queries:** Each alert will still have its pre-existing query, however since alert queries now have their own properties as discussed earlier, the default name for the query will be 
`query#{queryId}` and the `description` property will be empty.

**Case attributes:** all the existing case columns computed values will remain the same after the migration unless the user defines the alert’s case attributes query for the alert. In that case all the case columns will be re-computed in the next alert run overriding the pre-existing column values. 
> If the user defines a wrong case attributes query, all the existing column values will be cleared in the next alert run and will remain empty until the problem has been fixed.

**Alert’s general info:** The alert’s properties: name, description, target, frequency, enablement, sharing options remain the same.

## Shared Spaces

We are releasing a new way to share content across teams. Spaces are specific areas where all visualizations and folders are shared with groups of users.

***Impacted clients:***

- Every customer

***Benefits:***

- Enhanced access control over visualizations and folders.
- Better user management for onboarding and offboarding users.
- Better collaboration on visualization with no risks of data loss.

***Impacts:***

- The dashboard search bar has been removed. To start an investigation, users will have first to open a visualization.
- There's a new admin right to manage resources.

## Security updates

We have updated our internal dependencies to new major releases to offer up to date securities fixes.
The new version is rejecting by default security certificates that use outdated security algorithms. This can cause possible connection issues.

***Impacted clients:***

- Every customer using secure connection with certificates that use outdated securities algorithms

***Benefits:***

- Enhanced Security

***Impacts:***

- If Linkurious Enterprise is configured to bind on the `HTTPS` port and the certificate uses outdated securities algorithms, the system will faild to start (the [system logs][6] contains relevant information about this error).
- If Linkurious Enterprise is connected to external systems (e.g. graph database, external authentication providers, etc.) through a secure channel having a certificate using outdated securities, the system will refuse to enstablish the connection. The error will be a generic connection issues visible from the interface or the [system logs][6] depending on the faulty component.

***Remediation steps:***

We stringly suggest to regenerate the problematic certificates with new one that matches modern security standards (e.g. don't use MD5 for key hashing), see requirement [here][8].

If this is not possible in the short term and you need a **temporary** fix to this problem, you can follow the below steps to allow Linkurious Enterprise accepting old certificates:
- [Stop Linkurious Enterprise][1]
- [Uninstall Linkurious Enterprise from the system services][2] (if it was installed as such)
- Edit the `<linkurious>/data/manager/manager.json` file and add both `--openssl-legacy-provider` and `--tls-cipher-list=DEFAULT@SECLEVEL=0` options to the environment variable for the `Linkurious Server` service.
  
  You should now have something like the below example:
  ```json
  ...
  "services": [
    {
      "name": "Linkurious Server",
      ...
      "env": {
        "NODE_OPTIONS": "--openssl-legacy-provider --tls-cipher-list=DEFAULT@SECLEVEL=0"
      }
    }
   ]
   ...
  ```
  If you alredy have some configuration, concatenate the new one separated by a space to have something similar to the below example:
  ```json
  ...
  "services": [
    {
      "name": "Linkurious Server",
      ...
      "env": {
        "NODE_OPTIONS": "--old-configuration --openssl-legacy-provider --tls-cipher-list=DEFAULT@SECLEVEL=0"
      }
    }
   ]
   ...
  ```
- [Reinstall Linkurious Enterprise as a system services][3] (if needed)
- [Start Linkurious Enterprise][4]
- You are good to go!

After you properly renewed the certificates, revert the above changes.

# Dropped Support section

- Dropped support for legacy Operating Systems, check out the [new list][5]
  - Impacted clients: everyone using old operating systems
  - Remediation: verify the new support list and upgrade legacy systems accordingly
- Dropped support for legacy browsers, check out the [new list][7]
  - Impacted clients: everyone using old browsers
  - Remediation: verify the new support list and upgrade legacy browsers

[1]: https://doc.linkurio.us/admin-manual/4.0/stop/
[2]: https://doc.linkurious.com/admin-manual/4.0/install/#uninstall-from-services
[3]: https://doc.linkurious.com/admin-manual/4.0/install/#install-as-a-service
[4]: https://doc.linkurio.us/admin-manual/4.0/start/
[5]: https://doc.linkurio.us/admin-manual/4.0/requirements/#operating-system
[6]: https://doc.linkurious.com/admin-manual/4.0/logs/
[7]: https://doc.linkurious.com/admin-manual/4.0/client-requirements/#desktop-browsers
[8]: https://www.openssl.org/docs/manmaster/man3/SSL_CTX_set_security_level.html#Level-1
