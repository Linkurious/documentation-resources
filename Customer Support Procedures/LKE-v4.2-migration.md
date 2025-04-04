<!-- omit in toc -->
# Linkurious Enterprise migration to v4.2 guidelines

If you are planning to migrate your Linkurious Enterprise instance from an older version to v4.2,
this document will provide you extra details of what you need to take care or do for a successful upgrade.

<!-- omit in toc -->
# Table of contents
- [Requirements](#requirements)
- [General major changes](#general-major-changes)
  - [Hardened cookie secrets](#hardened-cookie-secrets)
  - [Security updates](#security-updates)

# Requirements

Configuration files with secrets encoded before Linkurious Enterprise v4.0.25 can no longer be decrypted in v4.2.0 and later.
If you are updating from Linkurious Enterprise v4.0 or older and secrets are encrypted in your configuration file,
please update to v4.1 first before updating to v4.2.

We strongly recommend backing-up your SQL database and your installation folder before updating Linkurious Enterprise.

# General major changes

## Hardened cookie secrets

In Linkurious v4.2, cookie secrets must be at least 32 character longs.

***Impacted clients:***

Clients using a cookie secret shorter than 32 characters.

***Benefits:***

Cookie secrets shorter than 32 characters are unsecure, enforcing longer secrets improves the security of the application.

***Impacts:***

If your configuration contains a `server.cookieSecret` value that is shorter than 32 characters,
you must replace it with a longer value.

## Security updates

We have updated our internal dependencies to new major releases to offer up to date securities fixes.

***Benefits:***

Enhanced Security.

***Impacts:***

As part of these security updates, the embedded Elasticsearch has been updated to v8.17.4.

Due to this update, the data-sources that use the "Embedded Elasticsearch" search provider will have
full-text search disabled, upon upgrading Linkurious.

To re-enable full-text search, you will need to re-index the impacted data-sources. This can be done
in one click from the data-source configuration page.
