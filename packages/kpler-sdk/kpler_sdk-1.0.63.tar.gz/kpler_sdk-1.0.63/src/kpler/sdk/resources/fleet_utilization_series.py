from datetime import date
from enum import Enum
from typing import List, Optional

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import (
    process_bool_parameter,
    process_date_parameter,
    process_enum_parameter,
    process_enum_parameters,
    process_list_parameter,
)


class FleetUtilizationSeries(KplerClient):

    """
    The ``FleetUtilizationSeries`` endpoint returns current and historical supply & demand capacity balance, total,loaded & ballast capacity evolution and capacity available by products.
    """

    RESOURCE_NAME = "fleet-utilization/series"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        zones: Optional[List[str]] = None,
        metric: Optional[Enum] = None,
        period: Optional[Enum] = None,
        split: Optional[Enum] = None,
        products: Optional[List[str]] = None,
        unit: Optional[Enum] = None,
        vessel_types_cpp: Optional[List[Enum]] = None,
        vessel_types_oil: Optional[List[Enum]] = None,
        vessel_states: Optional[List[Enum]] = None,
        percent: Optional[bool] = None,
        gte: Optional[int] = None,
        lte: Optional[int] = None,
        vessel_types: Optional[List[Enum]] = None,
        previous_zones: Optional[List[str]] = None,
        next_zones: Optional[List[str]] = None,
        vessel_directions: Optional[List[str]] = None,
        distinct_aggregation: bool = False,
    ):

        """
        Args:
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            zones: Optional[List[str]] Names of countries/geographical zones
            metric: Optional[Enum] ``FleetUtilizationSeriesMetric``
            period: Optional[Enum] ``FleetUtilizationSeriesPeriod``
            split: Optional[Enum] ``FleetUtilizationSeriesSplit``
            products: Optional[List[str]] Names of products
            unit: Optional[Enum] ``FleetUtilizationSeriesUnit``
            vessel_types_cpp: Optional[List[Enum]] ``VesselTypesCPP``
            vessel_types_oil: Optional[List[Enum]] ``VesselTypesOil``
            vessel_states: Optional[List[Enum]] ``FleetUtilizationSeriesVesselsState``
            percent: Optional[bool] Access percentage of loaded vessels over ballast vessels
            gte: Optional[int] Get vessels with deadweight/capacity greater or equals to this value by default 0
            lte: Optional[int] Get vessels with deadweight/capacity lower or equals to this value by default 606550
            vessel_types: Optional[List[Enum]] ``VesselTypesDry`` ``VesselTypesLNG`` ``VesselTypesLPG``
            previous_zones: Optional[List[str]] Names of zones (port/region/country/continent) the vessel is coming from
            next_zones: Optional[List[str]] Names of zones (port/region/country/continent) the vessel is going to
            vessel_directions: Optional[List[str]] Names of the vessel’s course of direction on the given day
            distinct_aggregation: Option[bool] Show or hide distinct vessels by default false

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.fleet_utilization_series import FleetUtilizationSeries
            ... from kpler.sdk import FleetUtilizationSeriesMetric, FleetUtilizationSeriesPeriod,FleetUtilizationSeriesSplit, FleetUtilizationSeriesUnit
            ... fleet_utilization_series_client = FleetUtilizationSeries(config)
            ... fleet_utilization_series_client.get(
            ...     start_date=date(2020,10,1),
            ...     end_date=date(2020,11,1),
            ...     zones=["Japan"],
            ...     metric=FleetUtilizationSeriesMetric.Count,
            ...     period=FleetUtilizationSeriesPeriod.Daily,
            ...     split=FleetUtilizationSeriesSplit.Product,
            ...     unit=FleetUtilizationSeriesUnit.MT
            ... )

            .. csv-table::
                :header:  "Date","Clean Products","crude/co","DPP","NPC","Other"

                "2020-10-01","114","62","31","37","13"
                "2020-10-02","114","60","36","40","14"
                "2020-10-03","104","59","38","43","12"
                "2020-10-04","105","55","38","42","13"
                "2020-10-05","109","60","40","42","13"
                "2020-10-06","100","61","37","36","14"
                "2020-10-07","103","52","31","30","14"
                "2020-10-08","105","38","33","24","13"
                "2020-10-09","109","46","31","17","11"
                "2020-10-10","115","48","35","21","10"
                "...","...","...","...","...","...",
        """

        query_parameters = {
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "zones": process_list_parameter(zones),
            "metric": process_enum_parameter(metric),
            "period": process_enum_parameter(period),
            "split": process_enum_parameter(split),
            "products": process_list_parameter(products),
            "unit": process_enum_parameter(unit),
            "vesselTypesCpp": process_enum_parameters(vessel_types_cpp, False),
            "vesselTypesOil": process_enum_parameters(vessel_types_oil, False),
            "vesselStates": process_enum_parameters(vessel_states, False),
            "percent": process_bool_parameter(percent),
            "gte": gte,
            "lte": lte,
            "vesselTypes": process_enum_parameters(vessel_types, False),
            "previousZones": process_list_parameter(previous_zones),
            "nextZones": process_list_parameter(next_zones),
            "vesselDirections": process_list_parameter(vessel_directions),
            "distinctAggregation": process_bool_parameter(distinct_aggregation),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
