<!-- omit in toc -->
# Neo4j migration to v4 guidelines

If you are planning to migrate your Neo4j database from an older version to v4,
this document will provide you extra details of what you need to take care of in your Linkurious Enterprise project.

<!-- omit in toc -->
# Table of contents
- [Issues with cypher queries](#issues-with-cypher-queries)
- [Issues with Datasources in Linkurious Enterprise](#issues-with-datasources-in-linkurious-enterprise)
  - [Pre-requisites](#pre-requisites)
  - [Procedure](#procedure)

# Issues with cypher queries

Neo4j v4 has introduced some breaking changes on some cypher syntax of functions (see more details on [Neo4j documentation](https://neo4j.com/docs/cypher-manual/current/deprecations-additions-removals-compatibility/#cypher-deprecations-additions-removals-4.0)).

As a consequence, you may have to rework your all your cypher queries such as:
- Data import scripts
- [Queries and Query Templates](https://doc.linkurio.us/user-manual/latest/query-templates/) defined in Linkurious Enterprise (some users may have created their own queries, consider to warn them)
- [Alerts](https://doc.linkurio.us/user-manual/latest/alert-dashboard/) defined in Linkurious Enterprise


# Issues with Datasources in Linkurious Enterprise

Neo4j v4 has introduced new communication protocols and other changes that will break your datasource configuration in Linkurious Enterprise.

In some cases you can get a communication issue after the upgrade, in other cases you could have the feeling to have lost of your data in Linkurious Enterprise. Follow the below procedure for a safe migration.

## Pre-requisites

- Linkurious Enterprise supports Neo4j v4 starting from the version v2.9.12, if you are working with an older version of Linkurious Enterprise update it before updating Neo4j (Linkurious Enterprise [update procedure](https://doc.linkurio.us/admin-manual/latest/update-procedure/))
- Connect to Linkurious Enterprise and take note of the `Key` associated to Datasource that will be impacted by the migration. You can do it from the `Admin` / `Data-sources Management` page (more details on [our documentation](https://doc.linkurio.us/admin-manual/latest/merging-data-sources/#1-open-the-data-source-management-page))

## Procedure

1. Stop Linkurious Enterprise (more details on [our documentation](https://doc.linkurio.us/admin-manual/latest/stop/))
1. Update Neo4j through the standard procedure (minimum supported version in Linkurious Enterprise is v4.0.2, check our [compatibility matrix](https://github.com/Linkurious/documentation-resources/blob/master/compatibility-matrix/compatibility-matrix.md))
1. From the `production.json` file change the [datasource configurations]((https://doc.linkurio.us/admin-manual/latest/configure-neo4j/#configuration)) to use the suggested protocols for Neo4j v4 in the `url` parameter
   - In case of a Neo4j Standalone server or Cluster configuration use `neo4j://`
   - In case of a Neo4j Standalone server or Cluster configuration using the encrypted layer use `neo4j+s://`
1. Start Linkurious Enterprise, if the system ask to re-index don’t do it at this stage
1. Check again the source `Key` (as done in the [pre-requisites](#pre-requisites)). Depending on the system configuration, most likely you will get a new `Key` with state needReindex and the old `Key` with state offline. If this is the scenario:
   - Use the [merge feature](https://doc.linkurio.us/admin-manual/latest/merging-data-sources/) on the offline datasource into the new generated one and use the *Overwrite merge* option
   - After the merge is done, you will not see any more the old Key and all the old data is now saved within the new Key
1. Complete any pending task to get the datasource ready (e.g. re-index)

***Only in a Neo4j Cluster configuration***:
1. If the datasource setting contains the `writeURL` or `httpUrl` options, you can remove both of them. They are not needed anymore to communicate with the cluster.
1. Now it is possible to configure the additional nodes of the Neo4j Cluster through the [alternativeURLs](https://doc.linkurio.us/admin-manual/latest/configure-neo4j/#configuration) parameter (e.g.  "alternativeURLs": ["neo4j+s://core2:7687", "neo4j+s://core3:7687"]) without the need for an external load balancer / proxy.
1. If you were previously using a Load Balancer between Linkurious Enterprise and Neo4j, you should have configured it with sticky sessions or similar configuration to let Linkurious Enterprise work properly. If that was the only application needing this configuration, you can now revert it to a more suitable load balancing policy.
