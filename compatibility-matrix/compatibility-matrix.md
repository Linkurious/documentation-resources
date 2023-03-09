# Linkurious Enterprise

## Version compatibility matrix

| Vendor \ Linkurious version|    2.10.x     | 3.0.0 - 3.0.6 | 3.0.7 - 3.0.x |     3.1.x     |     4.0.x     |
|:---------------------------|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| [Neo4j][a]                 | 3.2 - 4.2[^1] | 3.2 - 4.2[^1] |   3.2 - 4.4   |  4.0.2 - 4.4  | 4.0.2 - 5.x   |
| [Neo4 Aura][b]             |      Yes      |      Yes      |      Yes      |      Yes      |      Yes      |
| [Elasticsearch][c]         | 1.4 - 6.8[^2] | 6.0 - 7.x[^2] | 6.0 - 7.x[^2] | 6.0 - 7.x     | 6.0 - 7.x     |
| [JanusGraph][d]            | 0.1.x - 0.2.x |      No       |      No       |      No       |      No       |
| [Azure Cosmos DB][e]       |      Yes      |      Yes      |      Yes      |      Yes      |      Yes      |
| [Memgraph][f]              |      No       |      No       |      No       |      No       | 2.4 - 2.5[^3] |
| [Amazon Neptune][g]        |      No       |      No       |      No       |      No       |   1.2.0[^3]   |
| [MySQL][h]                 |   5.6 - 8.0   |   5.6 - 8.0   |   5.6 - 8.0   |   5.6 - 8.0   |   5.6 - 8.0   |
| [MariaDB][i]               |  10.1 - 10.5  |  10.1 - 10.5  |  10.1 - 10.5  |  10.1 - 10.5  |  10.1 - 10.5  |
| [Microsoft SQL Server][j]  |  2014 - 2019  |  2014 - 2019  |  2014 - 2019  |  2014 - 2019  |  2014 - 2019  |

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
[^2]: Elasticsearch 6.x is not supported with the neo4j-to-elasticsearch plugin
[^3]: No support for [incremental indexing](https://doc.linkurious.com/admin-manual/4.0/incremental-indexing/) with Elasticsearch
