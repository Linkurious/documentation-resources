# Linkurious Enterprise

## Version compatibility matrix

| Vendor \ Linkurious version|  4.0.0 - 4.0.6  | 4.0.7 - 4.0.15  | 4.0.16 - 4.0.x  |      4.1.x      |        4.2.x       |        4.3.x       |
|:---------------------------|:---------------:|:---------------:|:---------------:|:---------------:|:------------------:|:------------------:|
| [Neo4j][a]                 | 4.1.0 - 5.x[^1] | 4.1.0 - 5.x[^1] | 4.1.0 - 5.x[^1] | 4.4.0 - 5.x[^1] | 4.4.0 - 2025.x[^1] | 4.4.0 - 2026.x[^1] |
| [Neo4 Aura][b]             |      Yes        |       Yes       |       Yes       |       Yes       |         Yes        |         Yes        |
| [Elasticsearch][c]         |      7.x        |    7.0 - 8.x    |    7.0 - 8.x    |    7.0 - 8.x    |      7.0 - 8.x     |      8.0 - 9.x     |
| [Azure Cosmos DB][d]       |      Yes        |      Yes        |       Yes       |       Yes       |         Yes        |         Yes        |
| [Memgraph][e]              | 2.4 - 2.7[^2]   | 2.4 - 2.7[^2]   |  2.4 - 2.7[^2]  | 2.4 - 2.16[^2]  |    2.4 - 3.1[^2]   |    2.4 - 3.6[^2]   |
| [Amazon Neptune][f]        |   1.2.0[^2]     |   1.2.0[^2]     |    1.2.0[^2]    |    1.3.0[^2]    |      1.3.0[^2]     |      1.3.4[^2]     |
| [Google Spanner][g]        |       No        |       No        |       No        |     No[^3]      |         Yes        |         Yes        |
| [Google BigQuery][h]       |       No        |       No        |       No        |       No        |         No         |        Yes[^4]     |
| [MySQL][i]                 |   5.6 - 8.0     |   5.6 - 8.0     |    5.6 - 8.0    |       8.0       |      8.0 - 8.4     |      8.0 - 8.4     |
| [MariaDB][j]               |  10.1 - 10.5    |  10.1 - 10.5    |   10.1 - 10.5   |  10.6 - 10.11   |     10.6 - 11.4    |     10.6 - 11.8    |
| [Microsoft SQL Server][k]  |  2014 - 2019    |  2014 - 2019    |   2014 - 2022   |   2014 - 2022   |     2014 - 2022    |     2014 - 2022    |

[a]: https://neo4j.com/
[b]: https://neo4j.com/aura/
[c]: https://www.elastic.co/enterprise-search
[d]: https://azure.microsoft.com/en-us/products/cosmos-db
[e]: https://memgraph.com/
[f]: https://aws.amazon.com/neptune/
[g]: https://cloud.google.com/spanner
[h]: https://cloud.google.com/bigquery
[i]: https://www.mysql.com/
[j]: https://mariadb.org/
[k]: https://www.microsoft.com/en-us/sql-server/

[^1]: [Incremental indexing](https://doc.linkurious.com/admin-manual/4.0/incremental-indexing/) on Neo4j 5.x clusters is supported only if Linkurious Enterprise is 4.0.4 or higher and Neo4j is 5.4.0 or higher
[^2]: No support for [incremental indexing](https://doc.linkurious.com/admin-manual/4.0/incremental-indexing/) with Elasticsearch
[^3]: Google Spanner is supported in beta on Linkurious Enterprise 4.1.13 and higher
[^4]: Google BigQuery is fully supported only on Linkurious Enterprise 4.3.3 and higher

