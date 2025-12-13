from datetime import date
from typing import List, Optional

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import process_date_parameter, process_list_parameter


class InventoriesTankLevels(KplerClient):

    """
    The `InventoriesTankLevels` endpoint provides with the level of each and every tank in the indicated installation or zone, on a configurable period of maximum 31 days.
    """

    RESOURCE_NAME = "inventories/tank-levels"

    AVAILABLE_PLATFORMS = [Platform.Liquids]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        installations: Optional[List[str]] = None,
        zones: Optional[List[str]] = None,
    ):
        """
        Args:
            start_date:  Optional[date] Start of the period (YYYY-MM-DD)
            end_date:  Optional[date] End of the period (YYYY-MM-DD)
            installations: Optional[List[str]] Names of installations
            zones: Optional[List[str]] Names of countries/geographical zones

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.inventories_tank_levels import InventoriesTankLevels
            ... inventories_tank_levels_client=InventoriesTankLevels(config)
            ... inventories_tank_levels_client.get(
            ...     start_date=date(2020,11,1),
            ...     end_date=date(2020,11,1),
            ...     zones=["Japan"]
            ... )

            .. csv-table::
                :header: "Country","Installation","Tank","Date","Level","Capacity","Capacity","Utilization","Tank","Type"

                "Japan","Kamigoto Storage","JP_KAM.001","2020-11-01","2.337356e+07","2.767516e+07","0.844568","spr"
                "Japan","Kikuma Underground","JP_KIK.001","2020-11-01","7.565012e+06","8.900012e+06","0.850000","spr"
                "Japan","Kuji","JP_KUJ.001","2020-11-01","8.925014e+06","1.050001e+07","0.850000","spr"
                "Japan","Kushikino National Petroleum Stockpiling Base","JP_KUS.001","2020-11-01","8.925014e+06","1.050001e+07","0.850000","spr"
                "Japan","White Island","JP_WHI.001","2020-11-01","3.330794e+07","3.522294e+07","0.945632","spr"
        """

        query_parameters = {
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "installations": process_list_parameter(installations),
            "zones": process_list_parameter(zones),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
