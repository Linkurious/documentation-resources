<!-- omit in toc -->
# Neo4j migration to v5 guidelines

If you are planning to migrate your Neo4j database from an older version to v5,
this document will provide you extra details of what you need to take care of in your Linkurious Enterprise project.

<!-- omit in toc -->
# Table of contents
- [Pre-requisites and limitations](#pre-requisites-and-limitations)
- [Issues with cypher queries](#issues-with-cypher-queries)
- [Migrating databases](#migrating-databases)
- [New block storage format](#new-block-storage-format)

# Pre-requisites and limitations

- Linkurious Enterprise supports Neo4j v5 starting from the version v4.0.1 (a beta release estimated to be available in January 2023).
If you are working with an older version of Linkurious Enterprise, update it before updating Neo4j (Linkurious Enterprise [update procedure](https://doc.linkurio.us/admin-manual/latest/update-procedure/))

- We recommend you do not use Neo4j v5.0.0 nor Neo4j v5.1.0. The former is a limited availability release and the latter contains a critical
vulnerability to CVE-2022-42889, also known as Text4Shell. Use Neo4j v5.2.0 or newer.

- Incremental indexing is supported on a Neo4j v5 clusters starting from Linkurious Enterprise v4.0.4

# Issues with cypher queries

Neo4j v5 has introduced some breaking changes on some cypher syntax of functions (see more details on [Neo4j documentation](https://neo4j.com/docs/cypher-manual/current/deprecations-additions-removals-compatibility/#cypher-deprecations-additions-removals-5.0)).

As a consequence, you may have to rework your all your cypher queries such as:
- Data import scripts
- [Queries and Query Templates](https://doc.linkurio.us/user-manual/latest/query-templates/) defined in Linkurious Enterprise (some users may have created their own queries, consider to warn them)
- [Alerts](https://doc.linkurio.us/user-manual/latest/alert-dashboard/) defined in Linkurious Enterprise

# Migrating databases

You must first upgrade to Neo4j v4.4 before being able to migrate your database to Neo4j v5.

In Neo4j v5, BTREE indexes are replaced by RANGE, POINT, and TEXT indexes. Before migrating a database, in Neo4j v4.4,
you should create a matching RANGE, POINT, or TEXT index for each BTREE index (or index-backed constraint).

If you are using incremental indexing on your data-source, Linkurious Enterprise creates BTREE indexes in Neo4j v4.4.
They are named `Linkurious.incremental.<node|edge> :<LABEL>`. We recommend you either:
- drop these indexes before migrating your database to Neo4j v5. Linkurious Enterprise is going to automatically
recreate them as RANGE indexes after the migration, without any inconvenience.
- migrate your own BTREE indexes and then use the `--force-btree-indexes-to-range` option of the `neo4j-admin database migrate`
command to migrate the Linkurious Enterprise indexes.

When Linkurious reconnect to the data-source after the migration has completed, it is going to detect that the database
has changed and display a warning about that. You can safely dismiss this warning. Please note that you will then have
to fully reindex your data-source.

See complete procedure on [Neo4j documentation](https://neo4j.com/docs/upgrade-migration-guide/current/version-5).

# New block storage format

To improve database performances, Neo4j has implemented a new storage format (so called `block`)
in v5.14 and made it the default setting for the new databases created in the Enterprise Edition since v5.17.

> ![NOTE]
> The storage format for existing databases is not automatically migrated to the new `block` format,
> it requires a manual intervention.

> ![CAUTION]
> The `block` format is not available on the Neo4j Community Edition (CE).
> You can be impacted at any time in the feature if you plan an upgrade of an existing database
> from the Neo4j Community Edition (CE) to the Neo4j Enterprise Edition (EE).

Despite the new format doesn't imply any side effect to Linkurious Enterprise (when used on a new db),
the actual migration from an old format to the `block` format (on an existing db) will cause a change to the Neo4j internal IDs of the nodes and relationships ([source](https://neo4j.com/docs/operations-manual/current/database-internals/store-formats/#change-store-format)).

> ![CAUTION]
> If the references (Neo4j internal IDs) used by Linkurious Enterprise to access data change,
> the coherence of the visualizations and cases stored in Linkurious Enterprise is compromised
> with a very high risk of seeing different information than what was originally saved.

If you are already using [Alternative IDs](https://doc.linkurious.com/admin-manual/latest/alternative-ids/) in Linkurious Enterprise,
you are not relying anymore on the Neo4j internal IDs and hence not impacted by this section.
In this configuration you can safely perform the migration.

If you are **NOT** using [Alternative IDs](https://doc.linkurious.com/admin-manual/latest/alternative-ids/) in Linkurious Enterprise
**AND** you are planning to migrate to the `block` format
**AND** you don't want to lose consistency of your data (e.g. it might not be a requirement for DEV environments),
please [get in touch](https://doc.linkurious.com/admin-manual/latest/support/) to receive the appropriate support.
