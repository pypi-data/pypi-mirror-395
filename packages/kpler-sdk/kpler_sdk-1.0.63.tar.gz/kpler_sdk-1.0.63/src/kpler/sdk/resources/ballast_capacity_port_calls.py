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
    process_enum_parameters,
    process_list_parameter,
)


class BallastCapacityPortCalls(KplerClient):

    """
    The ``BallastCapacityPortCalls`` endpoint provides all the list of ballast vessels on the input period with their next load ETA and Destination.
    """

    RESOURCE_NAME = "ballast-capacity/port-calls"
    COLUMNS_RESOURCE_NAME = "ballast-capacity"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint ballast-capacity.


        Examples:
            >>> from kpler.sdk.resources.ballast_capacity_port_calls import BallastCapacityPortCalls
            ... ballast_capacity_port_calls_client = BallastCapacityPortCalls(config)
            ... ballast_capacity_port_calls_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "date","Date (timestamp)","Date (timestamp)","False","date yyyy-MM-dd"
                "vessel_imo","IMO","Vessel IMO","False","long"
                "vessel","Name","Vessel name","False","string"
                "vessel_dwt_tons","Capacity","Dead Weight Tonnage","False","long"
                "cargo_tons","Cargo (t)","Cargo (t)","False","double"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.COLUMNS_RESOURCE_NAME)

    def get(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        zones: Optional[List[str]] = None,
        products: Optional[List[str]] = None,
        vessel_types_cpp: Optional[List[Enum]] = None,
        vessel_types_oil: Optional[List[Enum]] = None,
        sources: Optional[List[Enum]] = None,
        vessel_state: Optional[List[Enum]] = None,
        size: Optional[int] = None,
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
            products: Optional[List[str]] Names of products
            vessel_types_cpp: Optional[List[Enum]] ``VesselTypesCPP``
            vessel_types_oil: Optional[List[Enum]] ``VesselTypesOil``
            sources: Optional[List[Enum]] ``BallastCapacityPortCallsSources``
            vessel_state: Optional[List[Enum]] ``BallastCapacityPortCallsVesselStates``
            size: Optional[int] Maximum number of ballast capacity port calls returned
            vessel_types: Optional[List[Enum]] ``VesselTypesDry`` ``VesselTypesLNG`` ``VesselTypesLPG``
            gte: Optional[int] Get vessels with deadweight/capacity greater or equals to this value by default 0
            lte: Optional[int] Get vessels with deadweight/capacity lower or equals to this value by default 606550
            with_freight_view: bool By default: with_freight_view=False. Provides access to the entire fleet's trades, irrespective of your current cargo subscription. Only available via Freight subscription.

        Examples:
            >>> from kpler.sdk.resources.ballast_capacity_port_calls import BallastCapacityPortCalls
            ... ballast_capacity_port_calls_client = BallastCapacityPortCalls(config)
            ... ballast_capacity_port_calls_client.get(
            ...         zones=["Japan"],
            ...         products=["crude/co"]
            ... )

            .. csv-table::
                :header:  "Date (timestamp)","IMO","Name","Dead Weight Tonnage","Cargo (t)","Next Installation","Next Port","Next Country","Next zone","Next ETA","..."

                "2020-11-24","9868132","Bei Hai Qi Lin","69900.0","75891.0","Kiire","Kiire","Japan","Asia","2020-12-18","..."
                "2020-11-24","9868132","Bei Hai Qi Lin","69900.0","75891.0","Kiire","Kiire","Japan","Asia","2020-12-08","..."
                "2020-11-24","9868132","Bei Hai Qi Lin","69900.0","75891.0","Kiire","Kiire","Japan","Asia","2020-11-28","..."
        """

        query_parameters = {
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "zones": process_list_parameter(zones),
            "products": process_list_parameter(products),
            "vesselTypesCpp": process_enum_parameters(vessel_types_cpp, False),
            "vesselTypesOil": process_enum_parameters(vessel_types_oil, False),
            "sources": process_enum_parameters(sources, False),
            "vesselState": process_enum_parameters(vessel_state, False),
            "size": size,
            "vesselTypes": process_enum_parameters(vessel_types),
            "gte": gte,
            "lte": lte,
            "withFreightView": process_bool_parameter(with_freight_view),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
