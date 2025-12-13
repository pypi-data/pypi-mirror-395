from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.enums import VesselTypesCPP, VesselTypesOil
from kpler.sdk.exceptions import WithProductEstimationPlatformException
from kpler.sdk.helpers import (
    process_date_parameter,
    process_enum_parameters,
    process_list_parameter,
)


class Fixtures(KplerClient):
    """
    The ``Fixtures`` query returns the Fixtures data.
    """

    RESOURCE_NAME = "fixtures"

    AVAILABLE_PLATFORMS = [Platform.Liquids]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint fixtures.

        Examples:
            >>> from kpler.sdk.resources.fixtures import Fixtures
            ...   fixtures_client = Fixtures(config)
            ...   fixtures_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "reportedDate","Reported date","None","False","date yyyy-MM-dd"
                "vesselName","Vessel","None","False","string"
                "vesselImo","IMO","None","False","long"
                "productQuantityInTons","Quantity (t)","None","False","double"
                "vesselDeadweight","Deadweight (t)","None","False","long"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self,
        size: Optional[int] = None,
        reported_date_after: Optional[date] = None,
        reported_date_before: Optional[date]  = None,
        lay_can_start_after: Optional[date] = None,
        lay_can_start_before: Optional[date]  = None,
        from_zones: Optional[List[str]] = None,
        to_zones: Optional[List[str]] = None,
        products: Optional[List[str]] = None,
        dwt_min: Optional[int] = None,
        dwt_max: Optional[int] = None,
        capacity_min: Optional[int] = None,
        capacity_max: Optional[int] = None,
        statuses: Optional[List[Enum]] = None,
        vessel_types_cpp: Optional[List[Enum]] = None,
        vessel_types_oil: Optional[List[Enum]] = None,
        vessel_types: Optional[List[str]] = None,
        vessels: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
    ) -> DataFrame:
        """

        Args:
            size: Optional[int] By default: size=1000 Maximum number of results returned.
            reported_date_after:Optional[date] Get fixtures reported on or after this date (YYYY-MM-DD)
            reported_date_before: Optional[date] Get fixtures reported on or before this date (YYYY-MM-DD)
            lay_can_start_after: Optional[date] Get fixtures with loading window start date after this date (YYYY-MM-DD)
            lay_can_start_before: Optional[date] Get fixtures with loading window start date before this date (YYYY-MM-DD)
            from_zones: Optional[List[str]] Names of the origin zones (port/region/country/continent)
            to_zones: Optional[List[str]] Names of the destination zones (port/region/country/continent)
            products: Optional[List[str]] Names of products
            dwt_min: Optional[int] Get vessels with deadweight greater or equal to this value by default 0
            dwt_max: Optional[int] Get vessels with deadweight lower or equal to this value by default 606550
            capacity_min: Optional[int] Get vessels with capacity greater or equal to this value by default 0
            capacity_max: Optional[int] Get vessels with capacity lower or equal to this value by default 606550
            statuses: Optional[List[Enum]] ```FixturesStatuses``` Status of the fixture (On Subs/In Progress/Fully Fixed/Finished/Failed/Cancelled)
            vessel_types_cpp: Optional[List[Enum]] ```VesselTypesCPP``` For given cpp vessel types (LR2, VLCC, LR3, MR, GP, LR1), only available for Liquids
            vessel_types_oil: Optional[List[Enum]] ```VesselTypesOil``` For given oil vessel types (Aframax, VLCC, Product Tanker, Suezmax, Panamax, ULCC), only available for Liquids
            vessel_types: Optional[List[str]] For other vessel types
            columns: Optional[List[str]] Retrieve all available columns when set to "all"
            vessels: Optional[List[str]] Names/IMO's of vessels
        Examples:
            >>> from datetime import date, timedelta, datetime
            ... from kpler.sdk.resources.fixtures import Fixtures
            ... fixtures_client = Fixtures(config)
            ... fixtures = fixtures_client.get(
            ... vessel_types_cpp = [VesselTypesCPP.MR],
            ... statuses = [FixturesStatuses.InProgress],
            ... columns=[
            ...         'reportedDate',
            ...         'vesselName',
            ...         'productName',
            ...         'origin',
            ...         'destination',
            ...         'status',
            ...         'vesselTypeCpp',
            ... ]
            ... )

            .. csv-table::
                :header: "Reported date","Vessel","Product","Origin","Destination","Status","Vessel Type CPP"

                "2022-10-27","Baltic Advance","ULSD","Sidi Kerir ","Koper","In Progress","MR"
                "2022-10-27","Libera","Gasoline","Burgas","Libya","In Progress","MR"
                "2022-10-27","Maria M","Gasoline","Petromidia","Corinth","In Progress","MR"
                "2022-10-27","Magnifica","Gasoline","Burgas","Koper","In Progress","MR"
                "2022-10-27","Janine K","Naphtha","Tuapse","Skhira","In Progress","MR"
                "...","...","...","...","...","...","..."
        """

        query_parameters: Dict[str, Optional[Any]] = {
            "size": size,
            "reportedDateAfter": process_date_parameter(reported_date_after),
            "reportedDateBefore": process_date_parameter(reported_date_before),            
            "layCanStartAfter": process_date_parameter(lay_can_start_after),
            "layCanStartBefore": process_date_parameter(lay_can_start_before),
            "fromZones": process_list_parameter(from_zones),
            "toZones": process_list_parameter(to_zones),
            "products": process_list_parameter(products),
            "dwtMin": dwt_min,
            "dwtMax": dwt_max,
            "capacityMin": capacity_min,
            "capacityMax": capacity_max,
            "statuses": process_enum_parameters(statuses),
            "vesselTypesCpp": process_enum_parameters(vessel_types_cpp, False),
            "vesselTypesOil": process_enum_parameters(vessel_types_oil, False),
            "vesselTypes": process_list_parameter(vessel_types),
            "vessels": process_list_parameter(vessels),
            "columns": process_list_parameter(columns),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)

