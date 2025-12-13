from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import (
    process_date_parameter,
    process_date_parameter_no_colon,
    process_enum_parameters,
    process_list_parameter,
)


class TradesSnapshot(KplerClient):
    """
    The ``TradesSnapshot`` query returns a snapshot of our trades data at a specified time.
    """

    RESOURCE_NAME = "trades/snapshot"
    COLUMNS_RESOURCE_NAME = "trades"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint trades.

        Examples:
            >>> from kpler.sdk.resources.trades_snapshot import TradesSnapshot
            ...   trades_snapshot_client = TradesSnapshot(config)
            ...   trades_snapshot_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "vessel_name","Vessel","Name of the vessel","False","string"
                "start","Date (origin)","Departure date of the vessel","False","datetime yyyy-MM-dd HH:mm"
                "origin_location_name","Origin","Origin location of the cargo","False","string"
                "origin_eta_source","Eta source (origin)","Source of the Estimated Time of Arrival to the Installation of Origin information (Port, Analyst, etc.)","False","string"
                "cargo_origin_cubic_meters","Volume (origin m3)","None","False","long"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.COLUMNS_RESOURCE_NAME)

    def get(
        self,
        snapshot_date: Optional[date] = None,
        vessels: Optional[List[str]] = None,
        from_installations: Optional[List[str]] = None,
        to_installations: Optional[List[str]] = None,
        from_zones: Optional[List[str]] = None,
        to_zones: Optional[List[str]] = None,
        buyers: Optional[List[str]] = None,
        sellers: Optional[List[str]] = None,
        products: Optional[List[str]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        trade_status: Optional[List[Enum]] = None,
        columns: Optional[List[str]] = None,
    ) -> DataFrame:
        """

        Args:
            snapshot_date: Optional[date] Date of the snapshot, if empty it returns the most recent snapshot
            vessels: Optional[List[str]] Names/IMO's of vessels
            from_installations: Optional[List[str]] Names of the origin installations
            to_installations: Optional[List[str]] Names of the destination installations (terminal/refinery)
            from_zones: Optional[List[str]] Names of the origin zones (port/region/country/continent)
            to_zones: Optional[List[str]] Names of the destination zones (port/region/country/continent)
            buyers: Optional[List[str]] Buyers of the cargo
            sellers: Optional[List[str]] Sellers of the cargo
            products: Optional[List[str]] Names of products
            start_date: Optional[date] Start of the period
            end_date: Optional[date] End of the period
            trade_status: Optional[List[Enum]] ``TradesStatus`` Return only trades of a particular status. By default value is scheduled.
            columns: Optional[List[str]] Retrieve all available columns when set to "all"
        Examples:
            >>> from datetime import date, timedelta, datetime
            ... from kpler.sdk.resources.trades_snapshot import TradesSnapshot
            ... trades_snapshot_client = TradesSnapshot(config)
            ... snapshots = trades_snapshot_client.get(
            ... snapshot_date = datetime.strptime('2022/01/01', '%Y/%m/%d'),
            ... to_zones = ["France"],
            ... products = ["crude"],
            ... start_date = datetime.strptime('2021/01/01', '%Y/%m/%d'),
            ... columns=[
            ...         "vessel_name",
            ...         "origin_country_name",
            ...         "origin_location_name",
            ...         "destination_location_name",
            ...         "start",
            ...         "end"
            ... ]
            ... )
            >>> print(snapshots.headers['snapshotName'])
            "2022-01-01T000100"
            >>> print(snapshots.headers['lastAvailableDate'])
            "2022-10-19T034600"

            .. csv-table::
                :header: "vessel_name", "origin_country_name", "origin_location_name","destination_location_name","start","end","trade_id","product_id"

                "Sakura Princess", "Russian Federation", "Novorossiysk", "Fos", "2022-02-05 18:48:00", "2022-02-18 23:36:00", "13163188", "1360"
                "Alfa Baltica", "United Kingdom", "Hound Point", "Le Havre", "2022-01-29 08:31:00", "2022-02-09 22:25:00", "13214389", "1502"
                "Scf Baikal", "Equatorial Guinea", "Zafiro FPSO", "Fos", "2022-01-27 14:18:00", "2022-02-20 02:17:00", "13263935", "2430"
                "Calida", "Russian Federation", "Umba FSO", "Le Havre", "2022-01-25 21:59:00", "2022-02-02 11:00:00", "13107517", "1940"
                "Siri Knutsen", "United Kingdom", "Culzean", "Le Havre", "2022-01-25 18:50:00", "2022-01-27 17:01:00", "13208418", "2488"
                "...", "...", "...", "...", "...", "...", "...", "..."

        """

        query_parameters: Dict[str, Optional[Any]] = {
            "snapshotDate": process_date_parameter_no_colon(snapshot_date),
            "vessels": process_list_parameter(vessels),
            "fromInstallations": process_list_parameter(from_installations),
            "toInstallations": process_list_parameter(to_installations),
            "fromZones": process_list_parameter(from_zones),
            "toZones": process_list_parameter(to_zones),
            "buyers": process_list_parameter(buyers),
            "sellers": process_list_parameter(sellers),
            "products": process_list_parameter(products),
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "tradeStatus": process_enum_parameters(trade_status),
            "columns": process_list_parameter(columns),
        }
        header_parameters: List[str] = ["snapshotName", "lastAvailableDate"]
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters, header_parameters)
