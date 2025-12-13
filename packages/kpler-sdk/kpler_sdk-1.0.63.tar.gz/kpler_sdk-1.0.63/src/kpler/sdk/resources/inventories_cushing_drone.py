from datetime import date
from enum import Enum
from typing import Optional

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import process_date_parameter, process_enum_parameter


class InventoriesCushingDrone(KplerClient):

    """
    The `InventoriesCushingDrone` endpoint returns crude inventories of Cushing for a specific  periodicity over a chosen period of time.
    """

    RESOURCE_NAME = "inventories/cushing-drone"

    AVAILABLE_PLATFORMS = [Platform.Liquids]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        period: Optional[Enum] = None,
    ):
        """
        Args:
            start_date:  Optional[date] Start of the period (YYYY-MM-DD)
            end_date:  Optional[date] End of the period (YYYY-MM-DD)
            period: Optional[Enum] ``InventoriesDronePeriod``

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.inventories_cushing_drone import InventoriesCushingDrone
            ... from kpler.sdk.enums import InventoriesDronePeriod
            ... inventories_tank_levels_client=InventoriesCushingDrone(config)
            ... inventories_tank_levels_client.get(
            ...     start_date=date(2021,6,14),
            ...     end_date=date(2021,8,14),
            ...     period=InventoriesDronePeriod.EiaWeeks
            ... )

            .. csv-table::
                :header: "Date","Level (kb)","Capacity (kb)","Capacity Utilization",

                "2021-06-18","45695","96947","0.471"
                "2021-06-25","44200","96947","0.456"
                "2021-07-02","43685","96947","0.451"
                "2021-07-09","42424","96947","0.438"
                "2021-07-16","40684","96947","0.420"
                "2021-07-23","39366","97353","0.404"
                "2021-07-30","39993","97353","0.401"
                "2021-08-06","39652","97353","0.407"
                "2021-08-13","37919","97569","0.389"
        """

        query_parameters = {
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "period": process_enum_parameter(period),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
