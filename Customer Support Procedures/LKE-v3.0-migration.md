<!-- omit in toc -->
# Linkurious Enterprise migration to v3.0 guidelines

If you are planning to migrate your Linkurious Enterprise instance from an older version to v3.0,
this document will provide you extra details of what you need to take care or do for a successful upgrade.

<!-- omit in toc -->
# Table of contents
- [General major changes](#general-major-changes)
  - [Upgrade of the Embedded Elasticsearch](#upgrade-of-the-embedded-elasticsearch)
  - [Evolution of the concept of `Alerts` to `Cases`](#evolution-of-the-concept-of-alerts-to-cases)
  - [Improving connectivity with Neo4j v4](#improving-connectivity-with-neo4j-v4)
- [Dropped Support section](#dropped-support-section)
- [General reminders](#general-reminders)
  - [Schema management](#schema-management)
- [Known issues](#known-issues)

# General major changes

## Upgrade of the Embedded Elasticsearch

The embedded Elasticsearch has been updated to v7.10 to remediate an outdated and unsupported version.

***Impacted clients:***

- Everyone using the `Embedded Elasticsearch` index strategy

***Benefits:***

- Remediation of security risks due an outdated version
- Remove the need for the customers to install a Java environment (Linkurious Enterprise will now rely on an embedded version of Java avoiding conflicts with other applications)

***Impacts:***

- The previous indexes are dropped during the upgrade process, after the new start, all the datasources using the `Embedded Elasticsearch` index strategy have to be reindex

## Evolution of the concept of `Alerts` to `Cases`

The `Alerts` feature has evolved into something more powerful and is becoming more and more a real `Case Management` tool.

***Impacted clients:***

- Everyone using `Alerts`

***Benefits:***

- Read more about all the new capabilities on our [blog post](https://linkurio.us/blog/linkurious-enterprise-3-0-beta/)

***Impacts:***

- All the existing alerts will be disabled after the upgrade (requiring a manual action on all of them) to allow generating new results
- To re-enable an existing alert, it is needed to configure a new mandatory parameter (the `target`), learn more about it on [https://doc.linkurio.us/admin-manual/3.0.3/alerts/#alert-target](https://doc.linkurio.us/admin-manual/3.0.4/alerts/#alert-target)
- Since the new feature allows to perform investigation directly in a `Case` (the new concept of item to be investigated), the previous functionality to save the results in an external visualization has been replaced by the functionality of saving the ongoing investigation in the `Case` itself
- The APIs around alerts have changed name to reflect the new evolution and some of them also changed the behavior to reflect the new capabilities

## Improving connectivity with Neo4j v4

We are deprecating the usage of the `http://` protocol in favor of the faster and more reliable `neo4j://` and `neo4j+s://` ones.

***Impacted clients:***

- Everyone connecting to Neo4j v4 through the `http://` protocol

***Benefits:***

- Get the best performances and reliability out of the connectivity with Neo4j v4 database both for standalone and cluster configuration

***Impacts:***

- Linkurious Enterprise will try to automatically discover and use the `neo4j://` protocol to connect to the database. In case the database is well configured, the system will be able to connect automatically otherwise will fail.
  
  > 💡 Even if you don't get connectivity issues, we suggest to reconfigure the datasource with below recommendations to avoid impacts in the future.

***Remediation steps:***

1. Verify with your IT department the traffic between Linkurious Enterprise server and Neo4j server is allowed for the `neo4j://` protocol (default port is 7687)
1. Stop Linkurious Enterprise
1. Access the `production.json` file and perform the below checks / changes on every impacted datasource:
   1. Change the `url` parameter from `http://` to `neo4j://` (or from`https://` to `neo4j+s://` for secure connection) and adjust the port accordingly
   1. If present, remove the `writeURL` and `httpUrl` parameters, they are not needed anymore
   1. In case of a Neo4j Cluster configuration, you can add the`alternativeURLs` to add the connection to other nodes of the cluster(more details [here](https://doc.linkurio.us/admin-manual/3.0.4configure-neo4j/#configuration))
   1. Check for the presence of the `manualSourceKey` parameter: if you don't have it you have to follow the [EXTRA] step at the end
1. Start Linkurious Enterprise
1. [EXTRA] Due the change of `url` after a successful connection, Linkurious Enterprise will generate a new empty datasource; use the [merge feature](https://doc.linkurio.us/admin-manual/3.0.4/merging-data-sources/) (with the *Overwrite* flag) to restore all the previous data

# Dropped Support section

- Dropped support for legacy Operating Systems, check out the [new list](https://doc.linkurio.us/admin-manual/3.0.4/requirements/#operating-system)
    - Impacted clients: everyone using old operating systems
    - Remediation: verify the new support list and upgrade legacy systems accordingly
- Dropped support for legacy Elasticsearch: minimum version v6
    - Impacted clients: everyone using the `Elasticsearch` index strategy directly pointing to an external server having version below v6 (clients using `Neo4j to Elasticsearch` are not impacted)
    - Remediation: upgrade the external Elasticsearch server to keep the old index OR perform a new fresh installation of latest Elasticsearch and run again the datasource index process
- Dropped support for legacy browsers
    - Impacted clients: everyone using IE11
    - Remediation: move users to a different supported browser
- Dropped support for JanusGraph
    - Impacted clients: everyone using JanusGraph
    - Remediation: move the project to another graph database vendor or remain on your current version of the product (**IMPORTANT** please consider our support policy to properly understand the impact of not upgrading to a recent version of Linkurious Enterprise)

# General reminders

## Schema management

Since Linkurious Enterprise v2.8 we have added the concept of [schema](https://doc.linkurio.us/admin-manual/3.0.4/data-schema/) to better support new features. Be sure to read about it and configure the schema properly to get the best out of Linkurious Enterprise v3.0.

Clients getting benefits:

- everyone using the data edit capabilities of Linkurious Enterprise: be sure to configure the correct type of your properties for data consistency
- everyone using the `Elasticsearch` index strategy to look for numbers and dates: be sure to configure the correct type of your properties to allow this type of search
- everyone having the need of optimizing the index: be sure to set as `View only` all the Node Categories, Edge Types and/or their properties that are not relevant for the users
- everyone looking for a full control of what users can see: be sure to configure the [Strict mode](https://doc.linkurio.us/admin-manual/3.0.4/schema-strict/) of the schema (you can eventually benefit also of the [Property-key access rights](https://doc.linkurio.us/admin-manual/3.0.4/property-level-access-rights/))

## Link generation

Over the time we have improved the security of our application to protect our clients. As a consequence, more and more features developed in the latest releases are ensuring that the end users are connecting through the correct link.

To avoid any unexpected behavior or issues with some features, please cross check that you have properly configured the [link generation](https://doc.linkurio.us/admin-manual/3.0.4/web-server/#link-generation) section: `domain` and the public ports configurations have to be configured with the correct dns name and ports used by the end users to access the web application (typically `localhost` is not a configuration you should see in the production environment, verify with the IT department in case of doubts).

# Known issues

- After an upgrade from Linkurious Enterprise 2.x, if you are installing on Linux or macOS, and are using the embedded Elasticsearch instance, Elasticsearch will not start. The fix is to make the files in `system/elasticsearch/bin/` executable. If you are not sure how to do that, please [get in touch](https://doc.linkurio.us/admin-manual/latest/support/).
