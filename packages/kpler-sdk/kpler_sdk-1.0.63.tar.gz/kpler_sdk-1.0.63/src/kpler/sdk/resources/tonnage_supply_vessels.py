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


class TonnageSupplyVessels(KplerClient):
    """
    The ``TonnageSupplyVessels`` provides lists of individual vessels which can arrive at a queried destination zone within a specified timeframe assuming a specified speed.
    """

    RESOURCE_NAME = "tonnage-supply/vessels"
    COLUMNS_RESOURCE_NAME = "tonnage-supply"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint tonnage-supply.

        Examples:
            >>> from kpler.sdk.resources.tonnage_supply_vessels import TonnageSupplyVessels
            ... tonnage_supply_vessels_client=TonnageSupplyVessels(config)
            ... tonnage_supply_vessels_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "date","Date (timestamp)","","False","date yyyy-MM-dd"
                "vessel_imo","IMO","IMO of the vessel","False","long"
                "vessel","Name","Name of the vessel","False","string"
                "vessel_dwt_tons","Dead Weight Tonnage","Dead Weight Tonnage","False","long"
                "vessel_type","Vessel Type","Type of the vessel","False","string"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.COLUMNS_RESOURCE_NAME)

    def get(
        self,
        destination: str,
        eta: int,
        speed: int,
        start_date: date,
        end_date: date,
        products: Optional[List[str]] = None,
        vessel_states: Optional[List[Enum]] = None,
        vessel_types: Optional[List[Enum]] = None,
        gte: Optional[int] = None,
        lte: Optional[int] = None,
        columns: Optional[List[str]] = None,
        match_next_port_call: Optional[bool] = None,
        vessels: Optional[List[str]] = None,
        build_year: Optional[int] = None,
        build_year_min: Optional[int] = None,
        build_year_max: Optional[int] = None,
        is_open: Optional[bool] = None,
    ):
        """
        Args:
            destination: str Destination name used for Vessel Matcher algorithm
            eta: int ETA in days used for Vessel Matcher algorithm
            speed: int Speed in knots used for Vessel Matcher algorithm
            start_date: date Start of the period (YYYY-MM-DD)
            end_date: date End of the period (YYYY-MM-DD). Cannot exceed start_date by more than 6 days
            products: Optional[List[str]] Names of products eg: crude/co, gasoil
            vessel_states: Optional[List[Enum]] ``TonnageSupplyVesselsState``
            vessel_types: Optional[List[Enum]] ``TonnageSupplyVesselTypes``
            gte: Optional[int] Get vessels with deadweight/capacity greater or equals to this value by default 0
            lte: Optional[int] Get vessels with deadweight/capacity lower or equals to this value by default 606550
            columns: Optional[List[str]] List of column names to return. Use "all" to retrieve all available columns
            match_next_port_call: Optional[bool] Filter to vessels for which the zone of the next port call matches the destination
            vessels: Optional[List[str]] Names or IMOs of the vessels
            build_year: Optional[int] Filter for vessels built in a specific year (exact match). Cannot be used together with build_year_min or build_year_max
            build_year_min: Optional[int] Filter for vessels built from this year onwards (inclusive). Use with build_year_max to define a range
            build_year_max: Optional[int] Filter for vessels built up to this year (inclusive). Use with build_year_min to define a range
            is_open: Optional[bool] Filter to vessels marked as open

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.tonnage_supply_vessels import TonnageSupplyVessels
            ... from kpler.sdk import TonnageSupplyVesselTypes
            ... tonnage_supply_vessels_client=TonnageSupplyVessels(config)
            ... tonnage_supply_vessels_client.get(
            ...     destination="Houston",
            ...     eta=7,
            ...     speed=11,
            ...     start_date=date(2025,11,1),
            ...     end_date=date(2025,11,7),
            ...     vessel_types=[TonnageSupplyVesselTypes.VLCC],
            ...     build_year_min=2010
            ... )

            .. csv-table::
                :header:  "Date (timestamp)","IMO","Name","Dead Weight Tonnage","Vessel Type","Vessel State","Last Product on board","Current Continent"

                "2025-11-01","9816323","Almi Atlas","315221","VLCC","Ballast","Crude/Co","Americas"
                "2025-11-01","9597240","Eagle Vancouver","320299","VLCC","Ballast","Crude/Co","Americas"
                "2025-11-01","9595216","Boston","299996","VLCC","Ballast","Crude/Co","Americas"
                "2025-11-01","9733947","Dht Jaguar","299629","VLCC","Ballast","Crude/Co","Americas"
                "2025-11-01","9537769","South Loyalty","323182","VLCC","Ballast","Crude/Co","Americas"
                "...","...","...","...","...","...","...","..."
        """

        query_parameters = {
            "destination": destination,
            "eta": eta,
            "speed": speed,
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "products": process_list_parameter(products),
            "vesselStates": process_enum_parameters(vessel_states, False),
            "vesselTypes": process_enum_parameters(vessel_types, False),
            "gte": gte,
            "lte": lte,
            "columns": process_list_parameter(columns),
            "matchNextPortCall": process_bool_parameter(match_next_port_call),
            "vessels": process_list_parameter(vessels),
            "buildYear": build_year,
            "buildYearMin": build_year_min,
            "buildYearMax": build_year_max,
            "isOpen": process_bool_parameter(is_open),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
