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


class TonnageSupplySeries(KplerClient):
    """
    The ``TonnageSupplySeries`` endpoint returns lists of vessels which can arrive at a queried destination zone within a specified timeframe assuming a specified speed.
    """

    RESOURCE_NAME = "tonnage-supply/series"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get(
        self,
        destination: str,
        eta: int,
        speed: int,
        metric: Enum,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        split: Optional[Enum] = None,
        products: Optional[List[str]] = None,
        vessel_states: Optional[List[Enum]] = None,
        vessel_types: Optional[List[Enum]] = None,
        gte: Optional[int] = None,
        lte: Optional[int] = None,
        match_next_port_call: Optional[bool] = None,
        build_year: Optional[int] = None,
        build_year_min: Optional[int] = None,
        build_year_max: Optional[int] = None,
        is_open: Optional[bool] = None,
    ):
        """
        Args:
            destination: str Destination name (zone)
            eta: int ETA in days
            speed: int Speed in knots
            metric: Enum ``TonnageSupplySeriesMetric``
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            split: Optional[Enum] ``TonnageSupplySeriesSplit``
            products: Optional[List[str]] Names of products/grades eg: crude/co, gasoil
            vessel_states: Optional[List[Enum]] ``TonnageSupplyVesselsState``
            vessel_types: Optional[List[Enum]] ``TonnageSupplyVesselTypes``
            gte: Optional[int] Get vessels with deadweight/capacity greater or equals to this value by default 0
            lte: Optional[int] Get vessels with deadweight/capacity lower or equals to this value by default 606550
            match_next_port_call: Optional[bool] Filter to vessels for which the zone of the next port call matches the destination
            build_year: Optional[int] Filter for vessels built in a specific year (exact match). Cannot be used together with build_year_min or build_year_max
            build_year_min: Optional[int] Filter for vessels built from this year onwards (inclusive). Use with build_year_max to define a range
            build_year_max: Optional[int] Filter for vessels built up to this year (inclusive). Use with build_year_min to define a range
            is_open: Optional[bool] Filter to vessels marked as open

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.tonnage_supply_series import TonnageSupplySeries
            ... from kpler.sdk import TonnageSupplySeriesMetric, TonnageSupplySeriesSplit, TonnageSupplyVesselTypes
            ... tonnage_supply_series_client = TonnageSupplySeries(config)
            ... tonnage_supply_series_client.get(
            ...     destination="Houston",
            ...     eta=7,
            ...     speed=11,
            ...     start_date=date(2025,10,1),
            ...     end_date=date(2025,11,1),
            ...     metric=TonnageSupplySeriesMetric.Count,
            ...     split=TonnageSupplySeriesSplit.VesselType,
            ...     vessel_types=[TonnageSupplyVesselTypes.VLCC],
            ...     build_year_min=2010
            ... )

            .. csv-table::
                :header:  "Date","VLCC"

                "2025-10-01","17"
                "2025-10-02","15"
                "2025-10-03","18"
                "2025-10-04","18"
                "2025-10-05","19"
                "2025-10-06","19"
                "2025-10-07","19"
                "2025-10-08","21"
                "2025-10-09","20"
                "2025-10-10","20"
                "2025-10-11","20"
                "2025-10-12","20"
                "2025-10-13","19"
                "2025-10-14","20"
                "2025-10-15","20"
                "2025-10-16","19"
                "2025-10-17","21"
                "2025-10-18","18"
                "2025-10-19","17"
                "2025-10-20","18"
                "2025-10-21","15"
                "2025-10-22","15"
                "2025-10-23","17"
                "2025-10-24","17"
                "2025-10-25","19"
                "2025-10-26","17"
                "2025-10-27","16"
                "2025-10-28","17"
                "2025-10-29","18"
                "2025-10-30","14"
                "2025-10-31","15"
                "2025-11-01","18"
        """

        query_parameters = {
            "destination": destination,
            "eta": eta,
            "speed": speed,
            "metric": process_enum_parameter(metric),
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "split": process_enum_parameter(split),
            "products": process_list_parameter(products),
            "vesselStates": process_enum_parameters(vessel_states, False),
            "vesselTypes": process_enum_parameters(vessel_types, False),
            "gte": gte,
            "lte": lte,
            "matchNextPortCall": process_bool_parameter(match_next_port_call),
            "buildYear": build_year,
            "buildYearMin": build_year_min,
            "buildYearMax": build_year_max,
            "isOpen": process_bool_parameter(is_open),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
