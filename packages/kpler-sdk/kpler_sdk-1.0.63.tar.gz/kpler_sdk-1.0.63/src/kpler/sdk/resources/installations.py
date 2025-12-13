from typing import List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import process_list_parameter


class Installations(KplerClient):
    """
    The ``Installations`` endpoint allows to perform full-text search on installations,
    in order to find names used in Kpler referential.
    """

    RESOURCE_NAME = "installations"

    AVAILABLE_PLATFORMS = [Platform.LNG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint installations.

        Examples:
            >>> from kpler.sdk.resources.installations import Installations
            ... installations_client = Installations(config)
            ... installations_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "continent","Continent","The installation's continent","False","string"
                "subcontinent","Subcontinent","The installation's subcontinent","False","string"
                "country","Country","The installation's country","False","string"
                "port","Port","The installation's port","False","string"
                "installation","Installation","The Installation's name","False","string"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self,
        columns: Optional[List[str]] = None,
        continent: Optional[str] = None,
        country: Optional[str] = None,
        port: Optional[str] = None,
        installation: Optional[str] = None,
        continent_id: Optional[int] = None,
        country_id: Optional[int] = None,
        port_id: Optional[int] = None,
        installation_id: Optional[int] = None,
        type: Optional[str] = None,
        owner: Optional[str] = None,
    ) -> DataFrame:
        """

        Args:
            continent:  Optional[str] The installation's continent name
            country:  Optional[str] The installation's country name
            port:  Optional[str] The installation's port name
            installation:  Optional[str] The installation's name
            continent_id:  Optional[int] The installation's continent ID in the Kpler system
            country_id:  Optional[int] The installation's country ID in the Kpler system
            port_id:  Optional[int] The installation's port ID in the Kpler system
            installation_id:  Optional[int] The installation's ID in the Kpler system
            type:  Optional[str] The installation's type, Import/Export
            owner:  Optional[str] The installation's owner
            columns: Optional[List[str]] Retrieve all available columns when set to "all"

        Examples:
            >>> from kpler.sdk.resources.installations import Installations
            ... installations_client = Installations(config)
            ... installations_client.get(columns=["installation","installation_type", "status","lng_storage_capacity"])

            .. csv-table::
                :header: "installation","installation_type", "status","lng_storage_capacity"

                "Fos Tonkin","Import","Active","80000"
                "Fos Cavaou","Import","Active","330000"
                "Freeport (Reg.)","Import","Decommissioned","480000"
                "Delfin FLNG","Export","Approved",""
                "Freeport","Export","Active","480000"
                "...","...","...","..."
        """
        query_parameters = {
            "continent": process_list_parameter(continent),
            "country": process_list_parameter(country),
            "port": process_list_parameter(port),
            "installation": process_list_parameter(installation),
            "continentId": process_list_parameter(continent_id),
            "countryId": process_list_parameter(country_id),
            "portId": process_list_parameter(port_id),
            "installationId": process_list_parameter(installation_id),
            "type": process_list_parameter(type),
            "owner": process_list_parameter(owner),
            "columns": process_list_parameter(columns),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)

    def search(self, q: str) -> DataFrame:
        """

        Args:
            q: str Argument to search by in installation names

        Examples:
            >>> from kpler.sdk.resources.installations import Installations
            ... installations_client=Installations(config)
            ... installations_client.search("abidjan")

            .. csv-table::
                :header: "installations"

                "SIR Abidjan"
                "Abidjan Terminal"

        """
        query_parameters = {"q": q, "resources": self.RESOURCE_NAME}
        return self._search(query_parameters)
