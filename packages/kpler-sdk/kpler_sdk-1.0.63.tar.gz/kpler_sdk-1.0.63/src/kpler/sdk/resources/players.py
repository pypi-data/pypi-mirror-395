from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration


class Players(KplerClient):
    """
    The ``Players`` endpoint allows to perform full-text search on players, in order to find names used in Kpler referential.
    """

    RESOURCE_NAME = "players"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def search(self, q: str) -> DataFrame:
        """

        Args:
            q: str Argument to search by in players names

        Examples:
            >>> from kpler.sdk.resources.players import Players
            ... players_client=Players(config)
            ... players_client.search("somo")

            .. csv-table::
                :header: "players"

                "SOMO"
                "Somoil"
        """
        query_parameters = {"q": q, "resources": self.RESOURCE_NAME}
        return self._search(query_parameters)
