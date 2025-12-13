from datetime import date
from enum import Enum
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


class Contracts(KplerClient):

    """
    The ``Contracts`` endpoint allows you to extract a list of SPAs, TUAs, LTAs, and Tenders for all LNG players, installations and zones.
    """

    RESOURCE_NAME = "contracts"

    AVAILABLE_PLATFORMS = [Platform.LNG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """

        Examples:
           >>> from kpler.sdk.resources.contracts import Contracts
           ... contracts_client = Contracts(config)
           ... contracts_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "type","Type","Type of contracts (SPA, LTA, TUA, Tender)","False","string"
                "seller","Seller","Company name of the seller","False","string"
                "buyer","Buyer","Company name of the buyer","False","string"
                "capacity","Capacity","None","False","float"
                "slots","Slots","None","False","integer"
                "...","...","...","...","..."
        """

        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self,
        columns: Optional[List[str]] = None,
        size: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        players: Optional[List[str]] = None,
        types: Optional[List[Enum]] = None,
        installations: Optional[List[str]] = None,
        zones: Optional[List[str]] = None,
    ):
        """
        This endpoint returns a list of contracts for the given arguments.

        Args:
            size:  Optional[int] Maximum number of contracts returned
            start_date:  Optional[date] Start of the period (YYYY-MM-DD)
            end_date:  Optional[date] End of the period (YYYY-MM-DD)
            players: Optional[str] Represents the buyers/sellers on the contracts
            types: Optional[List[Enum]] ``ContractsTypes``
            installations: Optional[List[str]] Names of installations
            zones: Optional[List[str]] Names of countries/geographical zones

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.contracts import Contracts
            ... from kpler.sdk import ContractsTypes
            ... contracts_client = Contracts(config)
            ... contracts_client.get(
            ...     size=10,
            ...     start_date=date(2018,1,1),
            ...     end_date=date(2020,10,1),
            ...     installations=["Dahej"],
            ...     zones=["India"],
            ...     players=["Shell"],
            ...     types=[ContractsTypes.Tender]
            ... )

            .. csv-table::
                :header: "type","seller","buyer","capacity","slots","delivery","start","end","installations origin","installations destination","origin zone","..."

                "Tender","Shell","IOC","NaN","1","DES","2019-08-15 00:00","2019-08-31 00:00","NaN","Dahej, Ennore LNG","World",".."
                "Tender","Shell","BPCL","NaN","1","DES","2018-08-20 00:00","2018-09-15 00:00","NaN","Dahej, Hazira","World",".."
                "Tender","Shell","IOC","NaN","1","DES","2018-05-01 00:00","2018-05-31 00:00","NaN","Dahej","World",".."
                "Tender","Shell","BPCL","NaN","1","DES","2018-05-01 00:00","2018-05-31 00:00","NaN","Dahej","World",".."
                "Tender","Shell","GAIL","NaN","2","DES","2018-04-10 00:00","2018-05-05 00:00","NaN","Dahej, Dabhol","World",".."
                "Tender","Shell","GAIL","NaN","1","DES","2018-02-15 00:00","2018-02-28 00:00","NaN","Dahej","World",".."
                "Tender","Shell","BPCL","NaN","1","DES","2018-01-19 00:00","2018-01-23 00:00","NaN","Dahej","World",".."
        """

        query_parameters = {
            "columns": process_list_parameter(columns),
            "size": size,
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "players": process_list_parameter(players),
            "types": process_enum_parameters(types),
            "installations": process_list_parameter(installations),
            "zones": process_list_parameter(zones),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
