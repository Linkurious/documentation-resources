# Linkurious Enterprise

## Version compatibility matrix

| Vendor \ Linkurious version|    2.10.x     | 3.0.0 - 3.0.6 | 3.0.7 - 3.0.x |     3.1.x     |  4.0.0 - 4.0.6  |  4.0.7 - 4.0.x  | 4.0.16 - 4.0.x  |
|:---------------------------|:-------------:|:-------------:|:-------------:|:-------------:|:---------------:|:---------------:|:---------------:|
| [Neo4j][a]                 | 3.2 - 4.2[^1] | 3.2 - 4.2[^1] |   3.2 - 4.4   |  4.0.2 - 4.4  | 4.1.0 - 5.x[^2] | 4.1.0 - 5.x[^2] | 4.1.0 - 5.x[^2] |
| [Neo4 Aura][b]             |      Yes      |      Yes      |      Yes      |      Yes      |      Yes        |       Yes       |       Yes       |
| [Elasticsearch][c]         | 1.4 - 6.8[^3] | 6.0 - 7.x[^3] | 6.0 - 7.x[^3] | 6.0 - 7.x     |      7.x        |    7.0 - 8.x    |    7.0 - 8.x    |
| [JanusGraph][d]            | 0.1.x - 0.2.x |      No       |      No       |      No       |      No         |      No         |       No        |
| [Azure Cosmos DB][e]       |      Yes      |      Yes      |      Yes      |      Yes      |      Yes        |      Yes        |       Yes       |
| [Memgraph][f]              |      No       |      No       |      No       |      No       | 2.4 - 2.7[^4]   | 2.4 - 2.7[^4]   |  2.4 - 2.7[^4]  |
| [Amazon Neptune][g]        |      No       |      No       |      No       |      No       |   1.2.0[^4]     |   1.2.0[^4]     |    1.2.0[^4]    |
| [MySQL][h]                 |   5.6 - 8.0   |   5.6 - 8.0   |   5.6 - 8.0   |   5.6 - 8.0   |   5.6 - 8.0     |   5.6 - 8.0     |    5.6 - 8.0    |
| [MariaDB][i]               |  10.1 - 10.5  |  10.1 - 10.5  |  10.1 - 10.5  |  10.1 - 10.5  |  10.1 - 10.5    |  10.1 - 10.5    |   10.1 - 10.5   |
| [Microsoft SQL Server][j]  |  2014 - 2019  |  2014 - 2019  |  2014 - 2019  |  2014 - 2019  |  2014 - 2019    |  2014 - 2019    |   2014 - 2022   |

[a]: https://neo4j.com/
[b]: https://neo4j.com/aura/
[c]: https://www.elastic.co/enterprise-search
[d]: https://janusgraph.org/
[e]: https://azure.microsoft.com/en-us/products/cosmos-db
[f]: https://memgraph.com/
[g]: https://aws.amazon.com/neptune/
[h]: https://www.mysql.com/
[i]: https://mariadb.org/
[j]: https://www.microsoft.com/en-us/sql-server/

[^1]: Support for Neo4j 4.3 without [incremental indexing](https://doc.linkurious.com/admin-manual/2.10.15/incremental-indexing/) feature.
[^2]: [Incremental indexing](https://doc.linkurious.com/admin-manual/4.0/incremental-indexing/) on Neo4j 5.x clusters is supported only if Linkurious is 4.0.4 or higher and Neo4j is 5.4.0 or higher
[^3]: Elasticsearch 6.x is not supported with the neo4j-to-elasticsearch plugin
[^4]: No support for [incremental indexing](https://doc.linkurious.com/admin-manual/4.0/incremental-indexing/) with Elasticsearch
