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
    process_list_parameter,
)


class CongestionVessels(KplerClient):

    """
    The ``CongestionVessels`` endpoint returns current and historical waiting time for vessels spent in waiting areas before going to berth.
    """

    RESOURCE_NAME = "congestion/vessels"
    COLUMNS_RESOURCE_NAME = "congestion"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint congestion vessels.

        Examples:
            >>> from kpler.sdk.resources.congestion_vessels import CongestionVessels
            ... congestion_vessels_client=CongestionVessels(config)
            ... congestion_vessels_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "date","Date","Day of vessel in the waiting zone","False","date yyyy-MM-dd"
                "vessel_imo","IMO","IMO of the vessel","False","long"
                "vessel","Name","Name of the vessel","False","string"
                "vessel_dwt_tons","Dead Weight Tonnage","Dead Weight Tonnage","False","long"
                "cargo_tons","Cargo (t)","Cargo in tons","False","double"
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
        size: Optional[int] = None,
        vessel_types: Optional[List[Enum]] = None,
        gte: Optional[int] = None,
        lte: Optional[int] = None,
        congestion_only: bool = None,
        vessel_operation: Optional[str] = None,
        waiting_duration_min: Optional[int] = None,
        waiting_duration_max: Optional[int] = None,
        with_freight_view: bool = False,
        period: Optional[Enum] = None,
        vessels: Optional[List[str]] = None,
    ):

        """
        Args:
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            zones: Optional[List[str]] Names of countries/geographical zones
            products: Optional[List[str]] Names of products
            vessel_types_cpp: Optional[List[Enum]] ``VesselsTypesCpp``
            vessel_types_oil: Optional[List[Enum]] ``VesselsTypesOil``
            size: Optional[int] Maximum number of fleet utilization vessels returned
            vessel_types: Optional[List[Enum]] ``VesselsTypesDry`` ``VesselsTypesLNG`` ``VesselsTypesLPG``
            gte: Optional[int] Get vessels with deadweight/capacity greater or equals to this value by default 0
            lte: Optional[int] Get vessels with deadweight/capacity lower or equals to this value by default 606550
            congestion_only: bool Exclude vessels in the waiting zone not tagged as congestion (lays ups,open vessels,floating storage,distressed cargoes etc).Use ["true", "false"]
            vessel_operation: ``CongestionVesselsOperation``
            waiting_duration_min: Optional[int] Minimum waiting duration of vessel. Default to 0 days if not specified.
            waiting_duration_max: Optional[int] Maximum waiting duration of vessel. Default to 1000000 days if not specified.
            with_freight_view: bool By default: with_freight_view=False. Provides access to the entire fleet's trades, irrespective of your current cargo subscription. Only available via Freight subscription.
            period: Optional[Enum] ``CongestionVesselsPeriod``
            vessels: Optional[List[str]] Names or IMOs of the vessels

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.congestion_vessels import CongestionVessels
            ... congestion_vessels_client=CongestionVessels(config)
            ... congestion_vessels_client.get(
            ...         start_date=date(2020, 10, 1),
            ...         end_date=date(2020, 11, 1),
            ...         zones=["Japan"],
            ...         products=["gasoline", "DPP"]
            ...     )

            .. csv-table::
                :header:  "Date (timestamp)","IMO","Name","Dead Weight Tonnage","Cargo(t)","Family","Group","Products","Installation","Port","..."

                "2020-10-25","9392808","Alpine Mystery","49999","16521.72","DPP","NaN","NaN","Kawasaki Refinery","Kawasaki","..."
                "2020-10-11","9317078","Haruna Express","45761","32449.03","Light Ends","Gasoline/Naphtha","Gasoline","Showa Yokkaichi Refinery","Yokkaichi","Japan","..."
                "2020-10-31","9392808","Alpine Mystery","49999","21028.51","DPP","Fuel Oils","FO","Sakai Refinery","Osaka","..."
                "2020-10-26","9392808","Alpine Mystery","49999","16521.72","DPP","NaN","NaN","Kawasaki Refinery","Kawasaki","..."
                "2020-10-28","9290646","Torm Kansas","46922","16825.78","Light Ends","Gasoline/Naphtha","Gasoline","Showa Yokkaichi Refinery","Yokkaichi","..."
        """

        query_parameters = {
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "zones": process_list_parameter(zones),
            "products": process_list_parameter(products),
            "vesselTypesCpp": process_enum_parameters(vessel_types_cpp, False),
            "vesselTypesOil": process_enum_parameters(vessel_types_oil, False),
            "size": size,
            "vesselTypes": process_enum_parameters(vessel_types, False),
            "gte": gte,
            "lte": lte,
            "congestionOnly": process_bool_parameter(congestion_only),
            "vesselOperation": process_enum_parameter(vessel_operation),
            "waitingDurationMin": waiting_duration_min,
            "waitingDurationMax": waiting_duration_max,
            "withFreightView": process_bool_parameter(with_freight_view),
            "period": process_enum_parameter(period),
            "vessels": process_list_parameter(vessels),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
