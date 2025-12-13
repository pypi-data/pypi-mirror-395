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


class BallastCapacitySeries(KplerClient):

    """
    The ``BallastCapacitySeries`` endpoint returns daily/ weekly/ monthly aggregated data values for a given zone/ vessel type/ time period /last product carried.
    """

    RESOURCE_NAME = "ballast-capacity/series"

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
        vessel_types: Optional[List[Enum]] = None,
        gte: Optional[int] = None,
        lte: Optional[int] = None,
        with_freight_view: bool = False,
    ):

        """
        Args:
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            zones: Optional[List[str]] Names of countries/geographical zones
            metric: Optional[Enum] ``BallastCapacitySeriesMetric``
            period: Optional[Enum] ``BallastCapacitySeriesPeriod``
            split: Optional[Enum] ``BallastCapacitySeriesSplit``
            products: Optional[List[str]] Names of products
            unit: Optional[Enum] ``BallastCapacitySeriesUnit``
            vessel_types_cpp: Optional[List[Enum]] ``VesselTypesCPP``
            vessel_types_oil: Optional[List[Enum]] ``VesselTypesOil``
            vessel_types: Optional[List[Enum]] ``VesselTypesDry`` ``VesselTypesLNG`` ``VesselTypesLPG``
            gte: Optional[int] Get vessels with deadweight/capacity greater or equals to this value by default 0
            lte: Optional[int] Get vessels with deadweight/capacity lower or equals to this value by default 606550
            with_freight_view: bool By default: with_freight_view=False. Provides access to the entire fleet's trades, irrespective of your current cargo subscription. Only available via Freight subscription.

        Examples:
            >>> from kpler.sdk.resources.ballast_capacity_series import BallastCapacitySeries
            ... from kpler.sdk import BallastCapacitySeriesMetric, BallastCapacitySeriesPeriod, BallastCapacitySeriesSplit
            ... ballast_capacity_series_client = BallastCapacitySeries(config)
            ... ballast_capacity_series_client.get(
            ...     metric=BallastCapacitySeriesMetric.Capacity,
            ...     period=BallastCapacitySeriesPeriod.Daily,
            ...     split=BallastCapacitySeriesSplit.VesselType,
            ... )

            .. csv-table::
                :header:  "Date","MR","GP","LR3","LR2","VLCC","LR1"

                "2020-11-22","10724.0","NaN","NaN","NaN","NaN","NaN"
                "2020-11-23","616555.0","2080981.0","1194773.0","1004319.0","163657.0","679003.0"
                "2020-11-24","1287340.0","2944327.0","4162769.0","2826019.0","1340769.0","2647163.0"
                "2020-11-25","854538.0","2975890.0","3930704.0","3186276.0","1226344.0","5675351.0"
                "2020-11-26","803699.0","2393202.0","2431821.0","2325491.0","571266.0","2991957.0"
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
            "vesselTypes": process_enum_parameters(vessel_types, False),
            "gte": gte,
            "lte": lte,
            "withFreightView": process_bool_parameter(with_freight_view),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
