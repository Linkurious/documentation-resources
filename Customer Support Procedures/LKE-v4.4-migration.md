<!-- omit in toc -->

# Linkurious Enterprise migration to v4.4 guidelines

If you are planning to migrate your Linkurious Enterprise instance from an older version to v4.4,
this document will provide you extra details of what you need to take care or do for a successful upgrade.

<!-- omit in toc -->

# Table of contents

- [Requirements](#requirements)
- [General major changes](#general-major-changes)
  - [Node.js v26](#nodejs-v26)
  - [Express 5 for plugins](#express-5-for-plugins)
  - [Prometheus metrics replaced by OpenTelemetry](#prometheus-metrics-replaced-by-opentelemetry)
  - [Plugin Manager and CSV Importer plugins removed](#plugin-manager-and-csv-importer-plugins-removed)
  - [Neo4j 4.4 no longer supported](#neo4j-44-no-longer-supported)
  - [Memgraph 2.x no longer supported](#memgraph-2x-no-longer-supported)
  - [Embedded Elasticsearch removed](#embedded-elasticsearch-removed)

# Requirements

If you are updating from Linkurious Enterprise v4.1 or older, please also read the
[v4.2 migration guidelines](LKE-v4.2-migration.md) before updating.

Linkurious Enterprise v4.4 runs on Node.js v26. Before updating, check that your operating system
is still supported (see [Node.js v26](#nodejs-v26)).

Linkurious Enterprise v4.4 supports Neo4j 5 or newer versions that are not end-of-life.
If you use Neo4j 4.4 or older, plan to upgrade it (see [Neo4j 4.4 no longer supported](#neo4j-44-no-longer-supported)).

Linkurious Enterprise v4.4 supports Memgraph 3.0 or newer. If you use Memgraph 2.x, plan to upgrade it
(see [Memgraph 2.x no longer supported](#memgraph-2x-no-longer-supported)).

We strongly recommend backing-up your SQL database and your installation folder before updating Linkurious Enterprise.

# General major changes

## Node.js v26

In Linkurious Enterprise v4.4, the embedded Node.js runtime has been updated to v26.

**_Impacted clients:_**

- Clients running Linkurious Enterprise on macOS older than 13.5.
- Clients using custom plugins.

**_Benefits:_**

Up-to-date security fixes and performance improvements from the latest Node.js release.

**_Impacts:_**

Node.js v26 has the following [platform requirements](https://github.com/nodejs/node/blob/v26.x/BUILDING.md#platform-list):

| Operating system | Minimum version                              |
| ---------------- | -------------------------------------------- |
| Linux            | kernel >= 4.18 and glibc >= 2.28 (unchanged) |
| Windows          | Windows 10 / Windows Server 2016 (unchanged) |
| macOS            | 13.5 (Ventura)                               |

If your server runs macOS older than 13.5, upgrade the operating system before updating Linkurious Enterprise.

Plugins run on the Node.js runtime embedded in Linkurious Enterprise. If you use custom plugins,
check that they and their dependencies are compatible with Node.js v26 before updating
(see the [Node.js changelog](https://github.com/nodejs/node/blob/main/doc/changelogs/CHANGELOG_V26.md)
for breaking changes).

The Docker image is not affected: it already ships with the right Node.js version.

## Express 5 for plugins

In Linkurious Enterprise v4.4, the web framework used by the server and by the plugin host has been updated
from Express 4 to [Express 5](https://expressjs.com/en/guide/migrating-5.html).

**_Impacted clients:_**

- Clients using custom plugins that declare backend APIs (`backendFiles` in the plugin manifest).

**_Benefits:_**

- Up-to-date security fixes: Express 5 is the actively maintained release line, and Express 4 is reaching its end of life.

**_Impacts:_**

The router given to plugin backend files is created by Linkurious Enterprise. From v4.4 on, plugin routes run
on Express 5, even if the plugin ships its own copy of Express 4. Code written for Express 4 may fail to start
or behave differently. The main changes are:

| Area                         | Express 4                                             | Express 5                                                    |
| ---------------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| Wildcard routes              | `/files/*`                                            | `/files/*splat` (the plugin fails to start otherwise)        |
| Optional route parameters    | `/items/:id?`                                         | `/items{/:id}` (the plugin fails to start otherwise)         |
| Regular expressions in paths | `/user/:id(\d+)`                                      | Not supported (the plugin fails to start)                    |
| Removed methods              | `req.param()`, `res.send(404)`, `res.json(obj, 500)`… | Error or wrong response when the route is called             |
| Query strings                | `?ids[]=1&ids[]=2` parsed as an array                 | Not parsed as an array anymore: the plugin may misbehave     |
| Request body                 | Empty object when there is no body                    | `undefined` with recent body parsers: the plugin may misbehave |

Check your custom plugins for these changes. For more details, see the [Express 5 migration guide](https://expressjs.com/en/guide/migrating-5.html).

A plugin with a legacy route syntax will build but fails to start. You will find a `PathError` in the
logs. For example`PathError: Missing parameter name at index 8: /files/*`.

## Prometheus metrics replaced by OpenTelemetry

In Linkurious Enterprise v4.4, the legacy Prometheus metrics exporter has been removed and replaced by
[OpenTelemetry](https://opentelemetry.io), the open standard for observability.

**_Impacted clients:_**

Clients who enabled metrics with the `metrics` key of the configuration file (`metrics.enabled: true`).

**_Benefits:_**

- Vendor-neutral telemetry: metrics can be scraped by Prometheus or pushed to any OpenTelemetry-compatible backend.
- New Linkurious Enterprise-specific metrics, such as graph query duration and data-source state.
- Distributed tracing, with trace identifiers added to Linkurious Enterprise logs.

**_Impacts:_**

The `metrics` configuration key is now removed: with no further action, metrics are no longer exposed after the update.

To restore them:

1. Set the `LKE_OTEL_ENABLED=true` environment variable. OpenTelemetry is configured through environment
   variables only, not through the configuration file.
2. If you are not using Docker, also set `OTEL_METRICS_EXPORTER=prometheus` and `OTEL_EXPORTER_PROMETHEUS_PORT=9400`
   to keep exposing metrics on the same `/metrics` endpoint and port as before.
   The Docker image already uses these defaults.
3. If you do not run an OpenTelemetry (OTLP) collector, set `OTEL_TRACES_EXPORTER=none` to disable trace export.

Most metric names have changed (for example, `nodejs_eventloop_lag_seconds` and `http_request_duration_seconds`
no longer exist). Update your Prometheus alerts and Grafana dashboards accordingly.

See the [Observability documentation](https://doc.linkurious.com/admin-manual/latest/observability/)
for the full configuration and the list of available metrics.

## Plugin Manager and CSV Importer plugins removed

In Linkurious Enterprise v4.4, the deprecated `plugin-manager` and `csv-importer` plugins are no longer
distributed. Both are replaced by built-in features:

| Removed plugin   | Built-in replacement                                                                           |
| ---------------- | ---------------------------------------------------------------------------------------------- |
| `plugin-manager` | The `Admin -> Plugins manager` page                                                            |
| `csv-importer`   | [CSV import](https://doc.linkurious.com/admin-manual/latest/import-csv/) with import templates |

**_Impacted clients:_**

- Clients using the Plugin Manager plugin. It was installed by default.
- Clients using the CSV Importer plugin.
- Clients listing `plugin-manager` or `csv-importer` in the `LKE_PLUGINS` environment variable.

**_Benefits:_**

The built-in features are maintained and released with Linkurious Enterprise, with no separate plugin to install or update.

**_Impacts:_**

`plugin-manager` is no longer part of the default `LKE_PLUGINS` value, and neither plugin can be installed
through `LKE_PLUGINS` anymore.

Plugins already installed are not removed by the update: their files stay in `<linkurious>/data/plugins`
and they keep running. To remove them:

1. Delete the `lke-plugin-plugin-manager-*.lke` and `lke-plugin-csv-importer-*.lke` files from
   `<linkurious>/data/plugins`.
2. Optionally, remove the `plugin-manager` and `csv-importer` entries from the `Plugins settings` field
   in `Admin -> Global configuration`. Settings of a removed plugin are ignored.
3. Remove `plugin-manager` and `csv-importer` from the `LKE_PLUGINS` environment variable, if set.

Users of the CSV Importer plugin should create [CSV import templates](https://doc.linkurious.com/admin-manual/latest/import-csv/)
to import their files.

## Neo4j 4.4 no longer supported

In Linkurious Enterprise v4.4, support for Neo4j 4.4 and older has ended. The lowest supported Neo4j version is now v5.

**_Impacted clients:_**

- Clients with a Neo4j 4.4 (or older) data source.

**_Benefits:_**

- Supported Neo4j versions are maintained and receive security fixes from Neo4j.

**_Impacts:_**

Neo4j 4.4 and older are end-of-life and are no longer supported:
deployments running Neo4j 4 must update to Neo4j 5 or newer versions that are not end-of-life.
In general, end-of-life Neo4j versions are not supported.

Since 2025, Neo4j has used calendar versioning, with a new release every month (`2025.01`, `2025.02`, …).
Each calendar release reaches end-of-life soon after the next one is out, while Neo4j 5.26, the last 5.x release,
is a long-term support (LTS) release. In practice, a supported deployment runs either Neo4j 5.26 LTS
or a recent calendar release (see the [Neo4j end-of-life dates](https://endoflife.date/neo4j)).

See the [Neo4j upgrade and migration guide](https://neo4j.com/docs/upgrade-migration-guide/current/).

## Memgraph 2.x no longer supported

In Linkurious Enterprise v4.4, support for Memgraph 2.x has ended. The lowest supported Memgraph version is now v3.0.0.

**_Impacted clients:_**

- Clients with a Memgraph 2.x data source.

**_Benefits:_**

- Supported Memgraph versions are maintained and receive security fixes from Memgraph.

**_Impacts:_**

Memgraph 2.x is no longer supported: deployments running Memgraph 2.x must update to Memgraph 3.0.0 or newer.

See the [Memgraph upgrade guide](https://memgraph.com/docs/database-management/upgrades).

## Embedded Elasticsearch removed
In Linkurious Enterprise v4.4, the embedded Elasticsearch runtime has been removed.

**_Impacted clients:_**

- Clients running any Linkurious Enterprise version except the Docker image without the `-es` suffix
- Clients using the embedded Elasticsearch runtime

**_Benefits:_**

- Reduced size of the Linkurious Enterprise installation and Docker image.
- Cleaner and independant update cycles for Linkurious Enterprise and Elasticsearch.

**_Impacts:_**

Embedded Elasticsearch is no longer an available search vendor option. Datasources configured with Embedded Elasticsearch now appear as regular Elasticsearch configuration with `host` `127.0.0.1` and `port` `9201`.

To restore the datasource configuration, you can either:

- Setup an external Elasticsearch server, see [how to configure it](https://doc.linkurious.com/admin-manual/latest/es-config/);
- Use another search engine provided for your graph vendor, see [the search option comparison](https://doc.linkurious.com/admin-manual/latest/search-options/);
- Disable search using the [No Search](https://doc.linkurious.com/admin-manual/latest/no-search/) option.

Notes:
- The data of the old embedded Elasticsearch at `<linkurious>/system/elasticsearch` is backed up during the update process. It can be safely removed to free up space as it is no longer used.
- If you use Docker, replace the `linkurious-enterprise-es` image with `linkurious-enterprise`. The `/elasticsearch` volume is obsolete: only the `/data` volume is needed.
