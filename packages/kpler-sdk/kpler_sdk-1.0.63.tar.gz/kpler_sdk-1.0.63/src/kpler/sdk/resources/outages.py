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


class Outages(KplerClient):

    """
    The ``Outages`` endpoint allows users to view all current, future, and historic outages, planned and unplanned,
    going back to 2016.
    """

    RESOURCE_NAME = "outages"

    AVAILABLE_PLATFORMS = [Platform.LNG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint outages.

        Examples:
            >>> from kpler.sdk.resources.outages import Outages
            ... outages_client = Outages(config)
            ... outages_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "outagetype","Outages Type","Planned or unplanned","False","string"
                "installationName","Installation Name","None","False","string"
                "installationCountry","Installation Country","None","False","string"
                "start","Start","None","False","datetime yyyy-MM-dd HH:mm"
                "end","End","None","False","datetime yyyy-MM-dd HH:mm"
                "comment","Comment","None","False","string"
                "installationId","Installation Id","Identifier in the database of Kpler","False","long"
        """

        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self,
        size: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        installations: Optional[List[str]] = None,
        zones: Optional[List[str]] = None,
        outage_types: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
    ):
        """

        Args:
            size: Optional[int] Maximum number of outages returned
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            installations: Optional[List[str]] Names of installations
            zones: Optional[List[str]] Names of zones ["port", "region", "country", "continent"]
            outage_types: Optional[List[Enum]] = ``OutagesTypes``
            columns: Optional[List[str]] Retrieve all available columns when set to "all"

        Examples:
            >>> from kpler.sdk.resources.outages import Outages
            ... from kpler.sdk import OutagesTypes
            ... outages_client = Outages(config)
            ... outages_client.get(
            ...     installations=["Sabine Pass"],
            ...     zones=["United States"],
            ...     size=10,
            ...     outage_types=[OutagesTypes.Planned]
            ... )

            .. csv-table::
                :header: "outagetype","installationName","installationCountry","start","end","comment","installationId"

                "Planned","Sabine Pass","United States","2020-02-10 00:00","2020-02-14 00:00","Compressor and electrical maintenance of the G...","3605"
                "Planned","Sabine Pass","United States","2019-09-01 16:05","2019-09-20 16:05","Scheduled turnarounds on train 5","3605"
                "Planned","Sabine Pass","United States","2019-08-05 00:00","2019-08-13 00:00","Maintenance at the Gillis compressor station r...","3605"
                "Planned","Sabine Pass","United States","2019-08-05 00:00","2019-08-26 00:00","Scheduled turnarounds on train 3 and 4","3605"
                "Planned","Sabine Pass","United States","2019-04-01 00:00","2019-04-11 00:00","2 trains are down for maintenance (T3 & T4)","3605"
                "Planned","Sabine Pass","United States","2019-03-22 00:00","2019-04-01 00:00","2 trains are under maintenance (T1&T2)","3605"
                "Planned","Sabine Pass","United States","2017-07-31 11:12","2017-09-15 09:32","The outages is on Train 3, with the end date to...","3605"
                "Planned","Sabine Pass","United States","2016-09-17 00:00","2016-10-26 00:00","Train 1 & 2 Shutdown","3605"
        """

        query_parameters = {
            "size": size,
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "installations": process_list_parameter(installations),
            "zones": process_list_parameter(zones),
            "outageTypes": process_enum_parameters(outage_types),
            "columns": process_list_parameter(columns),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
