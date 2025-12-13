from typing import List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import process_bool_parameter, process_list_parameter


class Vessels(KplerClient):
    """
    The ``Vessels`` query returns a snapshot of the current status of the fleet, including details on vessels status,
    last port call and next destination.
    """

    RESOURCE_NAME = "vessels"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint vessels.

        Examples:
            >>> from kpler.sdk.resources.vessels import Vessels
            ... vessels_client = Vessels(config)
            ... vessels_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "vessel_name","Vessels","Name of the vessels","False","string"
                "vessel_status","Status","Status of the vessels","False","string"
                "last_port_call_location_name","Last port-call","Vessels's last port call location","False","string"
                "last_port_call_end","Departure date","End of the last port call","False","datetime yyyy-MM-dd HH:mm"
                "cargo_on_board_cubic_meters","Volume","None","False","double"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self, columns: Optional[List[str]] = None, with_freight_view: bool = False
    ) -> DataFrame:
        """

        Args:
             columns: Optional[List[str]] Retrieve all available columns when set to "all"
             with_freight_view: bool By default: with_freight_view=False. Provides access to the entire fleet's trades, irrespective of your current cargo subscription. Only available via Freight subscription.

        Examples:
            >>> from kpler.sdk.resources.vessels import Vessels
            ... vessels_client = Vessels(config)
            ... vessels_client.get(columns=["vessel_name","vessel_status","last_port_call_end"])

            .. csv-table::
                :header: "vessel_name","vessel_status","last_port_call_location_name","next_destination_zone_name"

                "...","...","...","..."
                "Anichkov Bridge","Active","Pelepas Light.","Western Petroleum B Anchorage"
                "Anika","Active","PT SON Edible Oil Refinery","Lahad Datu"
                "Anikitos","Inactive","",""
                "Anikitos","Inactive","",""
                "Anikitos","Active","Rio Grande","Barcarena"
                "...","...","...","..."
        """
        query_parameters = {
            "columns": process_list_parameter(columns),
            "withFreightView": process_bool_parameter(with_freight_view),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)

    def search(self, q: str) -> DataFrame:
        """
        Performs the vessels name search by the given arguments

        Args:
            q: str Argument to search by in vessels names

        Examples:
            >>> from kpler.sdk.resources.vessels import Vessels
            ... vessels_client = Vessels(config)
            ... vessels_client.search("Ab")

            .. csv-table::
                :header: "vessels"

                "Abu Dhabi-Iii"
                "Bolan"
                "D&K Abdul Razzak Khalid Zaid Al-Khalid"
                "Abalone"
                "Abdias Nascimento"
                "..."
        """
        query_parameters = {"q": q, "resources": self.RESOURCE_NAME}
        return self._search(query_parameters)
