Changelog
*********

- 1.0.63 - 2025-12-08
    - Update numpy version and allow up to 2.3.5

- 1.0.62 - 2025-11-07
    - Add Tonnage Supply Series endpoint
    - Add Tonnage Supply Vessels endpoint
    - Add `TonnageSupplyVesselTypes`, `TonnageSupplyVesselsState`, `TonnageSupplySeriesMetric`, and `TonnageSupplySeriesSplit` enums

- 1.0.61 - 2025-11-07
    - Fix FutureWarning for deprecated `errors='ignore'` parameter in pandas `to_datetime()` and `to_numeric()` calls

- 1.0.60 - 2025-10-06
    - Make `FreightMetricsSeriesStatus` enum available

- 1.0.59 - 2025-10-06
    - Add support for python 3.13
    - Update pandas version and allow from 1.5.3 up to 2.3.2
    - Drop support for python 3.7 and 3.8

- 1.0.58 - 2025-09-09
    - Add timeout parameter to `Configuration` Object

- 1.0.57 - 2025-09-03
    - Update classifiers metadata tags with python 3.12

- 1.0.56 - 2025-05-28
    - Add `with_empty_volume` parameter to `port_calls` endpoint

- 1.0.53 - 2025-04-01
    - Fix `trade_snapshot` endpoint's `snapshot_date` parameter issue
    - Remove support for python 3.7
    - Add support for python 3.12

- 1.0.52 - 2024-10-31
   - Add destination_start_date and destination_end_date parameters to trades endpoint

- 1.0.51 - 2024-07-22
    - Bug fix for v2 freight metrics

- 1.0.50 - 2024-07-17
    - Update vessel states enum in Fleet Utilization endpoints with 'Maintenance' value

- 1.0.49 - 2024-07-15
    - Update freight metrics to use v2 API instead of obsolete v1 API
    - Enforce numpy version < 2 to prevent version conflicts with some pandas versions

- 1.0.48 - 2024-05-28
    - Fix typos in Refineries Documentation

- 1.0.47 - 2024-05-27
    - Add the 7 refineries endpoints in Aggregation:
    - Refineries Overview
    - Refineries Crude Runs
    - Refineries Crude Imports
    - Refineries Utilization Rates
    - Refineries Refined Products Supply
    - Refineries Secondary Unit Feed Input
    - Refineries Margins

- 1.0.46 - 2024-05-21
    - Allow Requests version until 2.31.0

- 1.0.45 - 2024-05-02
    - fix snapshot date usage in `TradesSnapshot`

- 1.0.44 - 2024-04-09
    - add `us-balances` endpoint to `supply-demand`

- 1.0.43 - 2023-12-20
    - parameter `metric` now required in `fleet_development_vessels` and `fleet_metrics_vessels`

- 1.0.42 - 2023-11-10
    - update `check_new_version` in `Configuration` object

- 1.0.41 - 2023-11-02
    - add netImport and netExport to Flows

- 1.0.40 - 2023-10-27
    - fix typos in some documentation

- 1.0.39 - 2023-10-20
    - Documentation layout update

- 1.0.38 - 2023-09-27
    - Fix uninferred numeric types for some endpoints

- 1.0.37 - 2023-09-18
    - Remove deprecated prices endpoint
    - Add `LongHaulVesselTypes` splits to flows
    - Add `intraRegion parameter` to trades and flows

- 1.0.36 - 2023-08-30
    - Limit requests to 2.2.29
    - Limit urllib3 to 1.27
    - Update twine to 4.0.2

- 1.0.35 - 2023-08-30
    - Allow Pandas version until 1.5.3
    - Add support for python 3.10 and 3.11

- 1.0.34 - 2023-07-25
    - Add `return_columns_ids` parameter in `TradesUpdates` to return columns ids instead of column names in the jsonUpdates column

- 1.0.33 - 2023-06-22
    - Allow Pandas version until 1.4.3
    - fixed bug with VesselTypeDry on Fleet_Utilization
    - Add snapshot_date to flows on all platforms

- 1.0.29 - 2023-02-16
    - fix typo in `Flows` doc

- 1.0.28 - 2023-02-14
    - Add `withProductEstimation` parameter in `Flows`

- 1.0.27 - 2022-11-07
    - Add `Fixtures` feature on Liquids

- 1.0.26 - 2022-10-28
    - Allow Pandas version until 1.4.2
    - Add `get_columns` on inventories, congestion_vessels, fleet_utilization_vessels, freight_metrics, ballast_capacity_port_calls
    - Add `zones`, `products` on all platform
    - Add `installations` on LNG

- 1.0.25 - 2022-10-20
    - Add `TradesUpdates` feature on all platform

- 1.0.24 - 2022-10-10
    - add new client `SupplyDemand`

- 1.0.23 - 2022-09-27
    - Add `TradesSnapshot` feature on all platform

- 1.0.22 - 2022-08-31
    - Bugfix for `FlowsSplit.Sources` value in `Flows`

- 1.0.21 - 2022-08-25
    - Documentation updates

- 1.0.20 - 2022-04-12
    - Documentation updates
    - Bugfix for `vessel_states` values in `Diversions`

- 1.0.19 - 2022-04-06
    - Add `crude quality` split for `Flows` and `Fleet Metrics`
    - Add `Diversions` feature on LNG platform

- 1.0.17 - 2021-11-22
    - Add `vessel_types` and `vessel_types_alt` (oil liquids platform only) filters for `Flows` and `Fleet Metrics`

- 1.0.16 - 2021-11-17
    - Add `without_eia_adjustment` param for `Inventories`

- 1.0.15 - 2021-10-12
    - Add `vessels` param for vessels endpoint for `Fleet Utilization`, `Congestion` and `Fleet Development`

- 1.0.14 - 2021-09-15
    - Add `period` param for vessels endpoint for `Fleet Utilization` and `Congestion`
    - Add new params for `Fleet Utilization` according to the documentation

- 1.0.13 - 2021-09-08
    - fix change log

- 1.0.12 - 2021-08-20
    - fix typo in `Trades` doc

- 1.0.11 - 2021-08-20
    - add new splits for `Flows` & `Fleet Metrics`
    - add new client `InventoriesCushingDrone`

- 1.0.8 - 2021-06-18
    - review dependencies
    - licensing source code

- 1.0.7 - 2021-06-01
    - add `with_product_estimation` parameter for trades
    - documentation updates
    - availability to update the endpoints url for dev purpose

- 1.0.5 - 2021-02-24
    - add `withFreightView` param according to the documentation
    - add `withOrderbook` param according to the documentation
    - add Contracting metric for fleet-development series/vessels
    - add product and grade split for congestion series
    - add `Fleet Metrics` feature on LNG platform

- 1.0.4 - 2021-01-29
    - fix boolean fields always reflecting as `True` in pandas
    - continuous integration improvements

- 1.0.3 - 2021-01-13
    - change version requirement for a lib : `numpy>=1.19.0`
    - new versions notification through a log message on `Configuration` object creation
    - better error handling on authentication failure

- 1.0.2 - 2020-12-17
    - allow proxy configuration in `Configuration` object
    - allow usage of local ssl certificate in `Configuration` object
    - allow disabling of ssl verification (default set to False) in `Configuration` object

- 1.0.1 - 2020-12-09
    - module and classes names uniformization
    - fix usage of doc string

- 1.0.0 - 2020-12-09
    - first version
