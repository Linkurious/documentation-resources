# Neo4j Plugin: Linkurious Custom Analyzer

## Description
An optional Custom Lucene Analyzer for Neo4j to be used when Neo4jSearch is chosen as index engine.

## Use case
Its use is recommended when you need to search for subparts of URL, emails, IPv6 addresses, or in general strings that contain alphanumeric components (e.g. `acme2dev`→`server.acme2dev.com`, `smith1990`→`john.smith1990@gmail.com`)

## Key Features:
- strings are tokenized by splitting on non-alphanumerical characters (i.e. anything but a number or a letter);
- strings are lowercased;
- alphanumeric char sequences are considered as a single token;
- No-ASCII characters are filtered and replaced by ASCII characters (e.g. [`é`, `è`, `ê`, `ë`] → `e`).

## Usage:
1. Download the `LinkuriousCustomAnalyzer-1.0.0.jar` file from this repository;
2. Install the plugin in your Neo4j instance;
3. Configure the `linkurious-custom-analyzer` analyzer in Linkurious Enterprise ([documentation](https://doc.linkurious.com/admin-manual/latest/search-neo4j/#configuration));
4. re-index the datasource.
 
> NOTE: please, refer to the official Neo4j documentation for detailed information on how to install the Neo4j plugin