from datetime import datetime
from typing import Any, Dict, List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import (
    process_bool_parameter,
    process_date_parameter_no_colon,
    process_list_parameter,
)


class TradesUpdates(KplerClient):
    """
    The ``TradesUpdates`` query returns a updates of our trades data at a specified time.
    """

    RESOURCE_NAME = "trades/updates"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = False, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get(
        self,
        products: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        show_all_history: Optional[str] = "false",
        columns: Optional[List[str]] = None,
        return_columns_ids: Optional[bool] = False,
    ) -> DataFrame:
        """

        Args:
            products: Optional[List[str]] Names of products
            start_date: Optional[datetime] The starting point in time of the returned "diffs", in UTC 0 time. All diffs that have been computed strictly after that date will be returned. Note: a time window of 15 days of diffs are kept, you can't look before in the past
            show_all_history: Optional [String]: Use ['true', 'false']. Default to false if not specified.
            columns: Optional[List[str]] Columns in the jsonUpdates field, Retrieve all available columns when set to "all"
            return_columns_ids: Optional[bool] set it to True to use columns ids instead of names in the jsonUpdates column. Default to False if not specified.
        Examples:
            >>> from datetime import date, timedelta, datetime
            ... from kpler.sdk.resources.trades_updates import TradesUpdates
            ... trades_updates_client = TradesUpdates(config)
            ... updates = trades_updates_client.get(
            ... products = ["crude"],
            ... start_date = datetime.strptime('2023-07-21T160000', '%Y-%m-%dT%H%M%S'),
            ... columns = [
            ...         "vessel_name",
            ...         "origin_location_name",
            ...         "destination_location_name",
            ...         "start",
            ...         "end"
            ... ]
            ... )
            >>> print(updates.headers['lastAvailableDate'])
            "2022-10-19T034600"

            .. csv-table::
                :header: "productId", "tradeId", "date", "operation", "jsonUpdates"

                "1096", "14686898", "2022-09-21 14:01:00", "UPDATE", "{'Date (destination)':'2022-09-21 02:30','Dest..."
                "1780", "14870244", "2022-09-21 14:01:00", "UPDATE", "{'Date (destination)':'2022-09-28 12:14'}"
                "1248", "15141376", "2022-09-21 14:01:00", "UPDATE", "{'Date (destination)':'2022-09-21 10:00','Dest..."
                "1280", "15269441", "2022-09-21 14:01:00", "INSERT", "{'Vessel':'San Matias I','Date (origin)':'2022..."
                "1932", "15269510", "2022-09-21 14:01:00", "INSERT", "{'Vessel':'Aretea','Date (origin)':'2022-10-17..."
                "...", "...", "...", "...", "..."

        """

        query_parameters: Dict[str, Optional[Any]] = {
            "products": process_list_parameter(products),
            "startDate": process_date_parameter_no_colon(start_date),
            "showAllHistory": process_bool_parameter(show_all_history),
            "columns": process_list_parameter(columns),
        }
        header_parameters: List[str] = ["lastAvailableDate"]

        self.column_ids = return_columns_ids

        return self._get_dataframe(self.RESOURCE_NAME, query_parameters, header_parameters)
