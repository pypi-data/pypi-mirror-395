from datetime import date
from enum import Enum
from typing import List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import (
    process_bool_parameter,
    process_date_parameter,
    process_enum_parameter,
    process_enum_parameters,
)


class FleetDevelopmentSeries(KplerClient):

    """
    The ``FleetDevelopmentSeries`` returns In-Service fleet, new vessel deliveries and old vessels sold for scrap as well as vessels with Scrubbers installed and planned.
    """

    RESOURCE_NAME = "fleet-development/series"
    RESOURCE_GET_COLUMN_NAME = "fleet-development"

    AVAILABLE_PLATFORMS = [Platform.Liquids, Platform.LPG, Platform.LNG, Platform.Dry]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the fleet_development endpoints

        Examples:
            >>> from kpler.sdk.resources.fleet_development_series import FleetDevelopmentSeries
            ... fleet_development_series_client = FleetDevelopmentSeries(config)
            ... fleet_development_series_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "day","Day","None","False","date yyyy-MM-dd"
                "vessel_name","Name","Name of the vessel","False","string"
                "vessel_imo","IMO","Vessel IMO","False","string"
                "vessel_mmsi","MMSI","The Maritime Mobile Service Identity of the vessel (9 digits)","False","string"
                "vessel_status","Status","Status of the vessel","False","string"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_GET_COLUMN_NAME)

    def get(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        metric: Optional[Enum] = None,
        aggregation_metric: Optional[Enum] = None,
        period: Optional[Enum] = None,
        split: Optional[Enum] = None,
        unit: Optional[Enum] = None,
        vessel_types_cpp: Optional[List[Enum]] = None,
        vessel_types_oil: Optional[List[Enum]] = None,
        vessel_types: Optional[List[Enum]] = None,
        gte: Optional[int] = None,
        lte: Optional[int] = None,
        with_orderbook: bool = False,
    ):

        """
        Args:
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            metric: Optional[Enum] ``FleetDevelopmentSeriesMetric``
            aggregation_metric: Optional[Enum] ``FleetDevelopmentSeriesAggregationMetric``
            period: Optional[Enum] ``FleetDevelopmentSeriesPeriod``
            split: Optional[Enum] ``FleetDevelopmentSeriesSplit``
            unit: Optional[Enum] ``FleetDevelopmentSeriesUnit``
            vessel_types_cpp: Optional[List[Enum]] ``VesselTypesCpp``
            vessel_types_oil: Optional[List[Enum]] ``VesselTypesOil``
            vessel_types: Optional[List[Enum]] ``VesselTypesDry`` ``VesselTypesLNG`` ``VesselTypesLPG``
            gte: Optional[int] Get vessels with deadweight/capacity greater or equals to this value by default 0
            lte: Optional[int] Get vessels with deadweight/capacity lower or equals to this value by default 606550
            with_orderbook: bool = False Access vessels in fleet orderbook, scheduled for future delivery

        Examples:

            >>> from datetime import date
            ... from kpler.sdk.resources.fleet_development_series import FleetDevelopmentSeries
            ... from kpler.sdk import FleetDevelopmentSeriesMetric, FleetDevelopmentSeriesAggregationMetric, FleetDevelopmentSeriesPeriod, FleetDevelopmentSeriesSplit
            ... fleet_development_series_client = FleetDevelopmentSeries(config)
            ... fleet_development_series_client.get(
            ...         start_date=date(2020,1,1),
            ...         end_date=date(2020,5,1),
            ...         metric=FleetDevelopmentSeriesMetric.Available,
            ...         aggregation_metric=FleetDevelopmentSeriesAggregationMetric.Count,
            ...         period=FleetDevelopmentSeriesPeriod.Monthly,
            ...         split=FleetDevelopmentSeriesSplit.VesselType
            ... )

            .. csv-table::
                :header:  "Date","GP","MR","LR2","VLCC","LR3","LR1"

                "2020-01","3727","2325","1107","905","636","506"
                "2020-02","3725","2330","1106","906","639","506"
                "2020-03","3728","2340","1108","909","641","506"
                "2020-04","3737","2347","1109","911","642","507"
                "2020-05","3740","2347","1109","911","642","507"
        """

        query_parameters = {
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "metric": process_enum_parameter(metric),
            "aggregationMetric": process_enum_parameter(aggregation_metric),
            "period": process_enum_parameter(period),
            "split": process_enum_parameter(split),
            "unit": process_enum_parameter(unit),
            "vesselTypesCpp": process_enum_parameters(vessel_types_cpp, False),
            "vesselTypesOil": process_enum_parameters(vessel_types_oil, False),
            "vesselTypes": process_enum_parameters(vessel_types, False),
            "gte": gte,
            "lte": lte,
            "withOrderbook": process_bool_parameter(with_orderbook),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
