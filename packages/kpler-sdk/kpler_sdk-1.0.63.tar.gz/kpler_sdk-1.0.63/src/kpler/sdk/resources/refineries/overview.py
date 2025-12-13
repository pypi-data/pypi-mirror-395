from datetime import date
from typing import List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import (
    process_date_parameter,
    process_list_parameter,
)


class Overview(KplerClient):
    """
    The Overview endpoint returns a list of refineries along
    with their respective characteristics for a point of interest (installation/zone).
    """

    RESOURCE_NAME = "refineries/overview"

    AVAILABLE_PLATFORMS = [Platform.Liquids]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint refineries overview.

        Examples:
            >>> from kpler.sdk.resources.refineries.overview import Overview
            ... overview_client = Overview(config)
            ... overview_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "date","Date (timestamp)","Date, within the start_date and end_date. Data is provided with ascending order on date. Format YYYY-MM-DD.","False","string"
                "zones","Zones","List of zones specified in the parameter zones.","False","list of string"
                "installations","Installations","List of installations specified in the parameter installations.","False","list of string"
                "refinery","Refinery","Name of the refinery","False","string"
                "owner","Owner","Name of the owner","False","string"
                "...","...","...","...","...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
            self,
            players: Optional[List[str]] = None,
            installations: Optional[List[str]] = None,
            zones: Optional[List[str]] = None,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None,
    ) -> DataFrame:
        """
        Args:
            players:  Optional[str] Names of players
            installations: Optional[List[str]] Names of installations
            zones: Optional[List[str]] Names of countries/geographical zones
            start_date:  Optional[date] Start of the period (YYYY-MM-DD), must be after 2017-01-01
            end_date:  Optional[date] End of the period (YYYY-MM-DD), maximum of 7 days from today

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.refineries.overview import Overview
            ... overview_client = Overview(config)
            ... overview_client.get(
            ...     installations=["xxxx"],
            ...     zones=["United States"],
            ...     start_date=date(2023, 4, 1),
            ...     end_date=date(2023, 7, 31),
            ...     player=["xxx"],
            ... )

            .. csv-table::
                :header: "Start Date","End Date","Zones","Installations","Refinery","Owner","Age (years)","NCI","Type","..."


                "2023-04-01","2023-07-01","Tacoma","Targa Tacoma","Seaport Sound Refinery","Targa Resources","46","None","Other","..."
                "2023-04-01","2023-07-01","Lovington","Lovington Refinery","Lovington Refinery","HollyFrontier","2","10.3","Complex","..."
                "2023-04-01","2023-07-01","Indianapolis","Indianapolis Refinery","Indianapolis Refinery","Marathon Oil Corporation","63","None","Other","..."
         """

        query_parameters = {
            "players": players,
            "installations": process_list_parameter(installations),
            "zones": process_list_parameter(zones),
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
