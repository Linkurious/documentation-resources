<!-- omit in toc -->

# Linkurious Enterprise migration to v4.4 guidelines

If you are planning to migrate your Linkurious Enterprise instance from an older version to v4.4,
this document will provide you extra details of what you need to take care or do for a successful upgrade.

<!-- omit in toc -->

# Table of contents

- [Requirements](#requirements)
- [General major changes](#general-major-changes)
  - [Node.js v26](#nodejs-v26)
  - [Prometheus metrics replaced by OpenTelemetry](#prometheus-metrics-replaced-by-opentelemetry)

# Requirements

If you are updating from Linkurious Enterprise v4.1 or older, please also read the
[v4.2 migration guidelines](LKE-v4.2-migration.md) before updating.

Linkurious Enterprise v4.4 runs on Node.js v26. Before updating, check that your operating system
is still supported (see [Node.js v26](#nodejs-v26)).

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
