## Linkurious Enterprise

#### Version compatibility matrix

| LKE version   | 2.9.0 - 2.9.4 | 2.9.5 - 2.9.9 | 2.9.10 - 2.9.x | 2.10.x        | 3.0.0 - 3.0.6 | 3.0.7 - 3.0.x |
|:--------------|:-------------:|:-------------:|:--------------:|:-------------:|:-------------:|:-------------:|
| Neo4j         | 2.2 - 3.5     | 3.2 - 4.2[^2] | 3.2 - 4.2[^2]  | 3.2 - 4.2[^2] | 3.2 - 4.2[^2] | 3.2 - 4.4     |
| Neo4 Aura     | No            | No            | [Yes][1]       | Yes           | Yes           | Yes           |
| Elasticsearch | 1.4 - 6.8[^3] | 1.4 - 6.8[^3] | 1.4 - 6.8[^3]  | 1.4 - 6.8[^3] | 6.0 - 7.x[^3] | 6.0 - 7.x[^3] |
| JanusGraph    | 0.1.x - 0.2.x | 0.1.x - 0.2.x | 0.1.x - 0.2.x  | 0.1.x - 0.2.x | No            | No            |
| CosmosDB      | No            | Yes           | Yes            | Yes           | Yes           | Yes           |
| MySQL         | 5.5 - 5.7     | 5.5 - 5.7     | 5.6 - 8.0      | 5.6 - 8.0     | 5.6 - 8.0     | 5.6 - 8.0     |
| MariaDB       | 10.1 - 10.4   | 10.1 - 10.4   | 10.1 - 10.5    | 10.1 - 10.5   | 10.1 - 10.5   | 10.1 - 10.5   |
| SQL Server    | 2000 - 2017   | 2000 - 2017   | 2014 - 2019    | 2014 - 2019   | 2014 - 2019   | 2014 - 2019   |

[1]: https://doc.linkurio.us/admin-manual/2.9.10/release-notes/
[^2]: These versions support Neo4j 4.3 with the exception of the [incremental indexing](https://doc.linkurio.us/admin-manual/2.10.15/incremental-indexing/) feature.
[^3]: Elasticsearch 6.x is not supported with the neo4j-to-elasticsearch plugin
