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


class CongestionSeries(KplerClient):

    """
    The ``CongestionSeries`` endpoint returns current and historical waiting time for vessels spent in waiting areas before going to berth.
    """

    RESOURCE_NAME = "congestion/series"

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
        congestion_only: bool = None,
        vessel_operation: Optional[Enum] = None,
        waiting_duration_min: Optional[int] = None,
        waiting_duration_max: Optional[int] = None,
        with_freight_view: bool = False,
    ):

        """
        Args:
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            zones: Optional[List[str]] Names of countries/geographical zones
            metric: Optional[Enum] ``CongestionSeriesMetric``
            period: Optional[Enum] ``CongestionSeriesPeriod``
            split: Optional[Enum] ``CongestionSeriesSplit``
            products: Optional[List[str]] Names of products
            unit: Optional[Enum] ``CongestionSeriesUnit``
            vessel_types_cpp: Optional[List[Enum]] ``VesselTypesCPP``
            vessel_types_oil: Optional[List[Enum]] ``VesselTypesOil``
            vessel_types: Optional[List[Enum]] ``VesselTypesDry`` ``VesselTypesLNG`` ``VesselTypesLPG``
            gte: Optional[int] Get vessels with deadweight/capacity greater or equals to this value by default 0
            lte: Optional[int] Get vessels with deadweight/capacity lower or equals to this value by default 606550
            congestion_only: bool Exclude vessels in the waiting zone not tagged as congestion (lays ups,open vessels,floating storage,distressed cargoes etc).Use ["true", "false"]
            vessel_operation: Optional[Enum] ``CongestionSeriesOperation``
            waiting_duration_min: Optional[int] Minimum waiting duration of vessel. Default to 0 days if not specified.
            waiting_duration_max: Optional[int] Maximum waiting duration of vessel. Default to 1000000 days if not specified.
            with_freight_view: bool By default: with_freight_view=False. Provides access to the entire fleet's trades, irrespective of your current cargo subscription. Only available via Freight subscription.

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.congestion_series import CongestionSeries
            ... from kpler.sdk import CongestionSeriesMetric, CongestionSeriesPeriod, CongestionSeriesSplit
            ... congestion_series_client = CongestionSeries(config)
            ... congestion_series_client.get(
            ...     start_date=date(2020, 1, 1),
            ...     end_date=date(2020, 6, 1),
            ...     metric=CongestionSeriesMetric.Count,
            ...     period=CongestionSeriesPeriod.Monthly,
            ...     split=CongestionSeriesSplit.VesselType
            ... )

            .. csv-table::
                :header:  "Date","MR","GP","LR3","LR2","VLCC","LR1"

                "2020-01","6097","5636","742","2241","866","1022"
                "2020-02","5683","5232","685","2094","831","944"
                "2020-03","6145","5659","747","2223","905","1033"
                "2020-04","5467","8006","676","2073","906","887"
                "2020-05","5414","9446","650","2045","855","838"
                "2020-06","170","268","21","72","22","22"
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
            "congestionOnly": process_bool_parameter(congestion_only),
            "vesselOperation": process_enum_parameter(vessel_operation, False),
            "waitingDurationMin": waiting_duration_min,
            "waitingDurationMax": waiting_duration_max,
            "withFreightView": process_bool_parameter(with_freight_view),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
