<!-- omit in toc -->
# Linkurious Enterprise migration to v4.1 guidelines

If you are planning to migrate your Linkurious Enterprise instance from an older version to v4.1,
this document will provide you extra details of what you need to take care or do for a successful upgrade.

<!-- omit in toc -->
# Table of contents
- [General major changes](#general-major-changes)
  - [Requirements](#requirements)
  - [Resources ownership](#resources-ownership)
  - [Simplified log configuration](#simplified-log-configuration)
  - [Worker pool](#worker-pool)
  - [Security updates](#security-updates)
- [Dropped Support section](#dropped-support-section)

# Requirements

Updating from Linkurious Enterprise v2.0 or older to v4.1 is not supported.
If you are updating from Linkurious Enterprise v2.0 or older, please first update to v3.1 or v4.0 before updating to v4.1.

We strongly recommend backing-up your SQL database and your installation folder before updating Linkurious Enterprise.

# General major changes

## Resources ownership

In Linkurious 4.1, we aim to standardize and improve user rights to facilitate onboarding and offboarding of new employees,
as well as giving Linkurious administrators greater freedom to manage access restrictions to the application's functionalities.

A new administrator right has been added for queries, custom actions and alerts.
This right allows the user to edit and delete any asset created by other Linkurious users.
We have also added node group rule creation rights, to harmonize rights.
A node group rule can therefore be modified and deleted by the creator
or a user with the `Manage, edit read/write queries & run` right level.

***Impacted clients:***

All Linkurious clients using queries, custom actions, alerts or node grouping.

***Benefits:***

Rights management has been harmonized between queries, custom actions, alerts and node grouping.
A user with sufficient rights can edit and delete any element created by other users.
Migration of assets created between different instances (using the Configuration Migration Plugin) has also been facilitated.

***Impacts:***
* The `Can create and apply node grouping rules` right is applied to every previously created custom groups.
* The `Manage, edit read/write queries & run` option for the `Queries`, `custom actions`, `alerts` and `node group rule`
access-rights is enabled for the following builtin groups: `Admin` and `Source Manager`.

## Simplified log configuration

In Linkurious v4.0, the logs configuration file had two differents settings for the default log level,
named `logLevel` and `externalLibLogLevel`.

In Linkurious v4.1, we simplify that by merging these two settings into a new one named `defaultLevel`,
which defaults to `info`.

***Impacted clients:***

All Linkurious clients actively using logs.

***Benefits:***

This change simplify the logs configuration.

***Impacts:***

The default log level in the `data/config/logger.json` file is changed to `info`.
If needed, it can be changed to another value once Linkurious enterprise is updated to v4.1.

# Worker pool
The worker pool has been introduced to handle heavy computation tasks by offloading it from the main Linkurious enterprise process.
Currently, the worker pool is used for running alerts, custom queries and visualization layouts.

***Impacted clients:***

- Every customer

***Benefits:***

- Enhanced the responsiveness of the application by offloading heavy computation tasks to separate threads.

***Impacts:***

- The configuration `advanced.layoutWorkers` has been removed from the configuration file as the layout computation is now handled by the worker pool.

See how to enable and configure the worker pool in [the Linkurious Enterprise documentation](https://doc.linkurious.com/admin-manual/latest/advanced-settings/#worker-pool-settings).

## Security updates

We have updated our internal dependencies to new major releases to offer up to date securities fixes.

***Benefits:***

- Enhanced Security

***Impacts:***

- None

# Dropped Support section

- Dropped support for legacy database vendors, check out the [new list][1]
  - Impacted clients: everyone using old database vendors
  - Remediation: verify the new support list and upgrade legacy database vendors accordingly

[1]: https://github.com/Linkurious/documentation-resources/blob/master/compatibility-matrix/compatibility-matrix.md
