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
  - [Cluster Mode: Fault Tolerance enhancement](#cluster-mode-fault-tolerance-enhancement)

# Requirements

Configuration files with secrets encoded before Linkurious Enterprise v4.0.25 can no longer be decrypted in v4.2.0 and later.
If you are updating from Linkurious Enterprise v4.0 or older and secrets are encrypted in your configuration file,
please update to v4.1 first before updating to v4.2.

We strongly recommend backing-up your SQL database and your installation folder before updating Linkurious Enterprise.

# General major changes

## Hardened cookie secrets

In Linkurious v4.2, cookie secrets must be at least 64 character longs.

***Impacted clients:***

Clients using a cookie secret shorter than 64 characters.

***Benefits:***

Cookie secrets shorter than 64 characters are unsecure, enforcing longer secrets improves the security of the application.

***Impacts:***

If your configuration contains a `server.cookieSecret` value that is shorter than 64 characters,
you must replace it with a longer value. Otherwise, it is going to be replaced automatically by a
secure value upon the next Linkurious restart.

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

## Cluster Mode: Fault Tolerance enhancement

We have updated the existing Fault Tolerance guidelines and made a new feature to better support the setup of a redundant infrastructure. The new feature is identified as [Cluster mode](https://doc.linkurious.com/admin-manual/latest/cluster-mode/).

***Benefits:***

* Enhanced system integrity via the new server role (`primary` vs `secondary`) to let the system automatically disable tasks that cannot run concurrently
  without the need of manual configurations
* Enhanced architecture that allows having more than just a single extra backup node
  (despite the technical enablement, a dedicated license discussion is still needed for deploying multiple servers)
* The architecture now supports the possibility to distribute users' connections among different servers that can all be active at the same time
  (read the feature documentation for limitations)

***Impacts:***

Despite the lack of direct impacts on existing `Fault Tolerance` setups, we changed our guidelines and introduced new configuration options that requires manual intervention to be enabled.
If you have an old `Fault tolerance` implementation according to our [previous documentation](https://doc.linkurious.com/admin-manual/4.1/faq/#how-can-fault-tolerance-be-achieved-), we suggest you to migrate to the new [Cluster mode](https://doc.linkurious.com/admin-manual/latest/cluster-mode/).

In particular, this would require to:
1. Re-align the configurations between the 2 existing servers of the `Fault tolerance` implementation 
2. Add the new `cluster` configuration by specifying a single server as `primary` and the other as `secondary`
3. Change your load balancer / reverse proxy configuration to improve the load balancing policy:
   the `backup` configuration is not a requirement anymore, the `Sticky Sessions` is a requirement when distributing the requests
4. Reach out to your CSM or SE if you need / plan to add new servers to your redundant environment

## Entity Resolution

In Linkurious Enterprise 4.2.1, several [entity resolution](https://doc.linkurious.com/admin-manual/latest/entity-resolution/) bugs have been fixed.
As a consequence, when updating to v4.2.1:
- the entity resolution server must be updated to a version at least 1.1.0 or after
- entity resolution must be purged
