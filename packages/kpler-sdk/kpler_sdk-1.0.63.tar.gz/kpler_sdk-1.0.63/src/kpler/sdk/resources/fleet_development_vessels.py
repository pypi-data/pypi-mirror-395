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


class FleetDevelopmentVessels(KplerClient):

    """
    The ``FleetDevelopmentVessels`` endpoint provides In-Service fleet, new vessel deliveries and old vessels sold for scrap as well as vessels with Scrubbers installed and planned.
    """

    RESOURCE_NAME = "fleet-development/vessels"
    RESOURCE_GET_COLUMN_NAME = "fleet-development"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the fleet_development endpoints

        Examples:
            >>> from kpler.sdk.resources.fleet_development_vessels import FleetDevelopmentVessels
            ... fleet_development_vessels_client=FleetDevelopmentVessels(config)
            ... fleet_development_vessels_client.get_columns()

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
        metric: Enum = None,
        vessel_types_cpp: Optional[List[Enum]] = None,
        vessel_types_oil: Optional[List[Enum]] = None,
        compliance_methods: Optional[List[Enum]] = None,
        columns: Optional[List[str]] = None,
        size: Optional[int] = None,
        vessel_types: Optional[List[Enum]] = None,
        gte: Optional[int] = None,
        lte: Optional[int] = None,
        with_orderbook: bool = False,
        vessels: Optional[List[str]] = None,
    ):

        """
        Args:
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            metric: Enum ``FleetDevelopmentVesselsMetric``
            vessel_types_cpp: Optional[List[Enum]] ``VesselTypesCPP``
            vessel_types_oil: Optional[List[Enum]] ``VesselTypesOil``
            compliance_methods: Optional[List[Enum]] ``FleetDevelopmentVesselsComplianceMethods``
            columns: Optional[List[str]] Retrieve all available columns when set to "all"
            size:  Optional[int] Maximum number of fleet development vessels returned
            vessel_types: Optional[Enum] ``VesselTypesDry`` ``VesselTypesLNG`` ``VesselTypesLPG``
            gte: Optional[int] Get vessels with deadweight/capacity greater or equals to this value by default 0
            lte: Optional[int] Get vessels with deadweight/capacity lower or equals to this value by default 606550
            with_orderbook: bool = False Access vessels in fleet orderbook, scheduled for future delivery
            vessels: Optional[List[str]] Names or IMOs of the vessels

        Examples:

            >>> from datetime import date
            ... from kpler.sdk.resources.fleet_development_vessels import FleetDevelopmentVessels
            ... from kpler.sdk import FleetDevelopmentVesselsMetric, FleetDevelopmentVesselsComplianceMethods
            ... fleet_development_vessels_client=FleetDevelopmentVessels(config)
            ... fleet_development_vessels_client.get(
            ...     start_date=date(2020,11,1),
            ...     end_date=date(2020,12,1),
            ...     metric=FleetDevelopmentVesselsMetric.Available,
            ...     compliance_methods=[FleetDevelopmentVesselsComplianceMethods.Scrubber],
            ...     size=5
            ... )

            .. csv-table::
                :header:  "Day","Name","IMO","MMSI","Status","Build year","Carrier type","Flag name","Engine type","Cargo system","..."

                "2020-11-01","Marlin Modest","9833577","563087800","Active","2019","NaN","Singapore","NaN","NaN","..."
                "2020-11-01","Silver Emily","9682356","538005680","Active","2014","NaN","Marshall Islands","NaN","NaN","..."
                "2020-11-01","Trf Mobile","9732802","538006545","Active","2016","NaN","Marshall Islands","NaN","NaN","..."
                "2020-11-01","Plover Pacific","9399911","563037200","Active","2009","NaN","Marshall Islands","NaN","NaN","..."
                "2020-11-01","Torm Atlantic","9433509","566428000","Active","2010","NaN","Singapore","NaN","NaN","..."
        """

        query_parameters = {
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "metric": process_enum_parameter(metric),
            "vesselTypesCpp": process_enum_parameters(vessel_types_cpp, False),
            "vesselTypesOil": process_enum_parameters(vessel_types_oil, False),
            "complianceMethods": process_enum_parameters(compliance_methods, False),
            "columns": process_list_parameter(columns),
            "size": size,
            "vesselTypes": process_enum_parameters(vessel_types),
            "gte": gte,
            "lte": lte,
            "withOrderbook": process_bool_parameter(with_orderbook),
            "vessels": process_list_parameter(vessels),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
