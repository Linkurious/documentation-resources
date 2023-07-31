<!-- omit in toc -->
# Linkurious Enterprise migration to v4.0 guidelines

If you are planning to migrate your Linkurious Enterprise instance from an older version to v4.0,
this document will provide you extra details of what you need to take care or do for a successful upgrade.

<!-- omit in toc -->
# Table of contents
- [General major changes](#general-major-changes)
  - [New multi model alerts](#new-multi-model-alerts)
  - [Shared Spaces](#shared-spaces)

# General major changes

## New multi model alerts

The `Alerts` feature has evolved and an alert can now contain multiple cypher queries to improve deduplication across cases.

***Impacted clients:***

- Everyone using `Alerts`

***Benefits:***

- Enhanced deduplication across cases with multiple cypher queries per alert
- Better business indicators with a dedicated query to process alerts columns
- Up to 40 custom columns per alert
- Alerts can be run manually directly through the interface

***Impacts:***

When migrating to alerts 4.0 there are a few changes that will be applied to alerts’ already existing matches, queries and case attributes.
**Queries:** Each alert will still have its pre-existing query, however since alert queries now have their own properties as discussed earlier, the default name for the query will be 
`query#{queryId}` and the `description` property will be empty.

**Case attributes:** all the existing case columns computed values will remain the same after the migration unless the user defines the alert’s case attributes query for the alert. In that case all the case columns will be re-computed in the next alert run overriding the pre-existing column values. 
> If the user defines a wrong case attributes query, all the existing column values will be cleared in the next alert run and will remain empty until the problem has been fixed.

**Alert’s general info:** The alert’s properties: name, description, target, frequency, enablement, sharing options remain the same.

## Shared Spaces

We are releasing a new way to share content across teams. Spaces are specific areas where all visualizations and folders are shared with groups of users.

***Impacted clients:***

- Every customer

***Benefits:***

- Enhanced access control over visualizations and folders.
- Better user management for onboarding and offboarding users.
- Better collaboration on visualization with no risks of data loss.

***Impacts:***

- The dashboard search bar has been removed. To start an investigation, users will have first to open a visualization.
- There's a new admin right to manage resources.
  
