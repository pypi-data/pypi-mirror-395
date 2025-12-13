from typing import List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import process_list_parameter


class Zones(KplerClient):
    """
    The ``Zones`` endpoint allows to perform full-text search on zones,
    in order to find names used in Kpler referential.
    """

    RESOURCE_NAME = "zones"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint zones.

        Examples:
            >>> from kpler.sdk.resources.zones import Zones
            ... zones_client = Zones(config)
            ... zones_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "ancestor_id","Ancestor Id","Identifier in the database of Kpler","False","long"
                "ancestor_name","Ancestor Name","Name of the Ancestor Zone","False","string"
                "ancestor_type","Ancestor Type","Ancestor Zone Type","False","string"
                "descendant_id","Descendant Id","Identifier in the database of Kpler","False","long"
                "descendant_name","Descendant Name","Name of the Descendant Zone","False","string"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self,
        columns: Optional[List[str]] = None,
        ancestor_id: Optional[List[int]] = None,
        ancestor_name: Optional[List[str]] = None,
        ancestor_type: Optional[List[str]] = None,
        descendant_id: Optional[List[int]] = None,
        descendant_name: Optional[List[str]] = None,
        descendant_type: Optional[List[str]] = None,
    ) -> DataFrame:
        """

        Args:
            ancestor_id:  Optional[int] IDs ancestor zones. Can be separated by a coma.
            ancestor_name:  Optional[str] Names ancestor zones. Can be separated by a coma.
            ancestor_type:  Optional[str] Type of ancestor zones. Can be separated by a coma. e.g. continent, subcontinent, region, subregion, country, port, custom, bay, cape, gulf, ocean, sea, strait, ...
            descendant_id:  Optional[str] IDs descendant zones. Can be separated by a coma.
            descendant_name:  Optional[int] Names descendant zones. Can be separated by a coma.
            descendant_type:  Optional[int] Type of descendant zones. Can be separated by a coma. e.g. continent, subcontinent, region, subregion, country, port, custom, bay, cape, gulf, ocean, sea, strait, ...
            columns: Optional[List[str]] Retrieve all available columns when set to "all"

        Examples:
            >>> from kpler.sdk.resources.zones import Zones
            ... zones_client = Zones(config)
            ... zones_client.get(ancestor_id=[515])

            .. csv-table::
                :header: "ancestor_id","ancestor_name", "ancestor_type","descendant_id","descendant_name","descendant_type"

                "515;Latin America","custom","209","Chile","country"
                "515","Latin America","custom","283","East Coast Mexico","subregion"
                "515","Latin America","custom","177","Caribbean Islands","subcontinent"
                "515","Latin America","custom","187","Cayman Islands","country"
                "515","Latin America","custom","239","Curacao","country"
                "...","...","...","..."
        """
        query_parameters = {
            "ancestorId": process_list_parameter(ancestor_id),
            "ancestorName": process_list_parameter(ancestor_name),
            "ancestorType": process_list_parameter(ancestor_type),
            "descendantId": process_list_parameter(descendant_id),
            "descendantName": process_list_parameter(descendant_name),
            "descendantType": process_list_parameter(descendant_type),
            "columns": process_list_parameter(columns),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)

    def search(self, q: str) -> DataFrame:
        """

        Args:
            q: str Argument to search by in zones names

        Examples:
            >>> from kpler.sdk.resources.zones import Zones
            ... zones_client=Zones(config)
            ... zones_client.search("oecd europe")

            .. csv-table::
                :header: "zones"

                "OECD Europe"
                "NON-OECD Europe"

        """
        query_parameters = {"q": q, "resources": self.RESOURCE_NAME}
        return self._search(query_parameters)
