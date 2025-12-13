from datetime import date
from typing import List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import (
    process_date_parameter,
    process_enum_parameters,
    process_list_parameter,
)


class Diversions(KplerClient):

    """
    The ``Diversions`` endpoint allows users to extract a list of historical & current diversions for all LNG vessels
    going back to 2019.
    """

    RESOURCE_NAME = "diversions"

    AVAILABLE_PLATFORMS = [Platform.LNG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint diversions.

        Examples:
            >>> from kpler.sdk.resources.diversions import Diversions
            ... diversions_client = Diversions(config)
            ... diversions_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "vessel_name","Vessel","None","False","string"
                "diversion_date","Diversion date","None","False","datetime yyyy-MM-dd HH:mm"
                "origin_diversion_location_name","Origin","None","False","string"
                "origin_diversion_date","Origin Date","None","False","datetime yyyy-MM-dd HH:mm"
                "diverted_from_location_name","Diverted from","None","False","string"
                "new_destination_location_name","New Destination","None","False","string"
                "new_destination_date","New Destination Date","None","False","datetime yyyy-MM-dd HH:mm"
                "vessel_state","Vessel State","None","False","string"
                "charterer_name","Charterer","None","False","string"
                "...","...","...","...","..."
        """

        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self,
        size: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        from_zones: Optional[List[str]] = None,
        to_zones: Optional[List[str]] = None,
        cancelled_zones: Optional[List[str]] = None,
        from_installations: Optional[List[str]] = None,
        to_installations: Optional[List[str]] = None,
        cancelled_installations: Optional[List[str]] = None,
        vessels: Optional[List[str]] = None,
        charterers: Optional[List[str]] = None,
        vessel_states: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
    ):
        """

        Args:
            size: Optional[int] Maximum number of diversions returned
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            from_zones: Optional[List[str]] Names of origin zones ["port", "region", "country", "continent"]
            to_zones: Optional[List[str]] Names of destination zones
            cancelled_zones: Optional[List[str]] Names of diverted zones
            from_installations: Optional[List[str]] Names of origin installations
            to_installations: Optional[List[str]] Names of destination installations
            cancelled_installations: Optional[List[str]] Names of diverted installations
            vessels: Optional[List[str]] Names or IMOs of vessels
            charterers: Optional[List[str]] Names or charterers
            vessel_states: Optional[List[Enum]] = ``DiversionsVesselState``
            columns: Optional[List[str]] Retrieve all available columns when set to "all"

        Examples:
            >>> from kpler.sdk.resources.diversions import Diversions
            ... from kpler.sdk import DiversionsVesselState
            ... diversions_client = Diversions(config)
            ... diversions_client.get(
            ...     from_installations=["Sabine Pass"],
            ...     to_zones=["United States"],
            ...     size=10,
            ...     vessel_states=[DiversionsVesselState.Loaded]
            ... )

            .. csv-table::
                :header: "vessel_name","diversion_date","origin_diversion_location_name","origin_diversion_date","diverted_from_location_name","new_destination_location_name","new_destination_date","vessel_state","charterer_name"

                "Hispania Spirit","2020-12-23 15:31:00","Sabine Pass","2020-12-17 08:57:00","Dragon","Rio","2021-01-11 11:27:00","Loaded","Shell"
                "Gaslog Skagen","2020-11-30 00:00:00","Sabine Pass","2020-11-25 16:31:00","Dragon","Bahia","2020-12-06 16:01:00","Loaded","RWE"
                "Maran Gas Ulysses","2020-03-05 00:00:00","Sabine Pass","2020-03-01 07:02:00","MED Sea","Quintero","2020-06-05 16:42:00","Loaded","Shell"
        """

        query_parameters = {
            "size": size,
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "fromZones": process_list_parameter(from_zones),
            "toZones": process_list_parameter(to_zones),
            "cancelledZones": process_list_parameter(cancelled_zones),
            "fromInstallations": process_list_parameter(from_installations),
            "toInstallations": process_list_parameter(to_installations),
            "cancelledInstallations": process_list_parameter(cancelled_installations),
            "vessels": process_list_parameter(vessels),
            "charterers": process_list_parameter(charterers),
            "vessel_states": process_enum_parameters(vessel_states),
            "columns": process_list_parameter(columns),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
