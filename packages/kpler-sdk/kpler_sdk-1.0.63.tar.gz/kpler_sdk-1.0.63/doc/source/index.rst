.. kpler python sdk documentation master file, created by
   sphinx-quickstart on Fri Oct 16 14:10:16 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Kpler Python SDK
****************

The Kpler Python SDK provides access to Kpler data.

It can be easily integrated into notebooks, scripts, and applications.

It is available to all Kpler API clients.

Example
-------
.. literalinclude:: examples/quick_one.py
    :linenos:
    :language: python

returns :

.. csv-table::
    :header: "vessel_name","closest_ancestor_product","closest_ancestor_grade","start","end","origin_location_name","destination_location_name"

    "Eco Bel Air","crude","Basrah","2020-11-01 14:20:00","2020-12-14 01:02:00","Al Basrah","PADD 5"
    "Stella","crude","NaN","2020-10-30 09:48:00","2020-12-09 21:30:00","Angra dos Reis","PADD 5"
    "Cap Charles","crude","NaN","2020-10-21 05:47:00","2020-11-20 23:15:00","Angra dos Reis","Long Beach"
    "Sebarok Spirit","crude","Maya","2020-10-21 01:00:00","2020-10-24 06:49:00","Yuum Kak Naab FPSO","Houston"
    "Montreal Spirit","crude","NaN","2020-10-20 13:30:00","2020-11-24 01:18:00","Sao Sebastiao","Cherry Point"
    "Washington","crude","ANS","2020-10-19 14:48:00","2020-10-27 00:00:00","Valdez","San Francisco"
    "...","...","...","...","...","...","..."

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Home

   self
   getting_started
   change_log

.. toctree::
   :maxdepth: 2
   :caption: Aggregations

   resources/flows
   resources/ballast_capacity_series
   resources/congestion_series
   resources/fleet_development_series
   resources/fleet_metrics_series
   resources/fleet_utilization_series
   resources/inventories
   resources/inventories_cushing_drone
   resources/freight_metrics_series
   resources/supply_demand
   resources/tonnage_supply_series
   resources/refineries/utilization_rates
   resources/refineries/crude_runs
   resources/refineries/crude_imports
   resources/refineries/overview
   resources/refineries/refined_products_supply
   resources/refineries/secondary_unit_feed_input
   resources/refineries/margins

.. toctree::
   :maxdepth: 2
   :caption: Facts

   resources/trades
   resources/port_calls
   resources/ship_to_ships
   resources/vessels
   resources/contracts
   resources/outages
   resources/diversions
   resources/ballast_capacity_port_calls
   resources/congestion_vessels
   resources/fleet_development_vessels
   resources/fleet_metrics_vessels
   resources/fleet_utilization_vessels
   resources/inventories_tank_levels
   resources/trades_snapshot
   resources/trades_updates
   resources/fixtures
   resources/tonnage_supply_vessels

.. toctree::
   :maxdepth: 2
   :caption: Dimensions

   resources/products
   resources/installations
   resources/zones
   resources/players


Indices and tables
==================

* :ref:`genindex`
