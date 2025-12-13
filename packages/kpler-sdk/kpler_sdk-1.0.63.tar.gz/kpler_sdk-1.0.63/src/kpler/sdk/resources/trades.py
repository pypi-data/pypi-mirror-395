from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.exceptions import WithProductEstimationPlatformException
from kpler.sdk.helpers import (
    process_bool_parameter,
    process_date_parameter,
    process_enum_parameters,
    process_list_parameter,
)


class Trades(KplerClient):
    """
    The ``Trades`` query returns the volumes from one point of interest to another (installation/zone) on a cargo-by-cargo basis.
    """

    RESOURCE_NAME = "trades"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint trades.

        Examples:
            >>> from kpler.sdk.resources.trades import Trades
            ...   trades_client = Trades(config)
            ...   trades_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "vessel_name","Vessel","Name of the vessel","False","string"
                "start","Date (origin)","Departure date of the vessel","False","datetime yyyy-MM-dd HH:mm"
                "origin_location_name","Origin","Origin location of the cargo","False","string"
                "origin_eta_source","Eta source (origin)","Source of the Estimated Time of Arrival to the Installation of Origin information (Port, Analyst, etc.)","False","string"
                "cargo_origin_cubic_meters","Volume (origin m3)","None","False","long"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self,
        size: Optional[int] = None,
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
        destination_start_date: Optional[date] = None,
        destination_end_date: Optional[date] = None,
        trade_status: Optional[List[Enum]] = None,
        with_forecast: Optional[bool] = None,
        with_intra_country: Optional[bool] = None,
        with_intra_region: Optional[bool] = None,
        columns: Optional[List[str]] = None,
        with_freight_view: Optional[bool] = False,
        with_product_estimation: Optional[bool] = False,
    ) -> DataFrame:
        """

        Args:
            size: Optional[int] Maximum number of trades returned (a trade can result in more than one row if multi-products one)
            vessels: Optional[List[str]] Names/IMO's of vessels
            from_installations: Optional[List[str]] Names of the origin installations
            to_installations: Optional[List[str]] Names of the destination installations (terminal/refinery)
            from_zones: Optional[List[str]] Names of the origin zones (port/region/country/continent)
            to_zones: Optional[List[str]] Names of the destination zones (port/region/country/continent)
            buyers: Optional[List[str]] Buyers of the cargo
            sellers: Optional[List[str]] Sellers of the cargo
            products: Optional[List[str]] Names of products
            start_date: Optional[date] Start of the vessel departure period
            end_date: Optional[date] End of the vessel departure period
            destination_start_date: Optional[date] Start of the vessel arrival period
            destination_end_date: Optional[date] End of the vessel arrival period
            trade_status: Optional[List[Enum]] ``TradesStatus`` Return only trades of a particular status. By default value is scheduled.
            with_forecast: Optional[bool] By default: withForecast=true. Include trades predicted by our in-house model when set to "true". Use ["true", "false"]
            with_intra_country: Optional[bool] By default: withIntraCountry=true. Takes into account the trades within the selected country. Use ["true", "false"]
            with_intra_region: Optional[bool] By default: withIntraRegion=true. Takes into account the trades within the selected region. Use ["true", "false"]
            columns: Optional[List[str]] Retrieve all available columns when set to "all"
            with_freight_view: bool By default: with_freight_view=False. Provides access to the entire fleet's trades, irrespective of your current cargo subscription. Only available via Freight subscription.
            with_product_estimation: bool By default withProductEstimation=False. Activate the product estimation feature. When set to true, the estimated product will overwrite the existing product information.
        Examples:
            >>> from datetime import date, timedelta
            ... from kpler.sdk.resources.trades import Trades
            ... trades_client = Trades(config)
            ... trades_client.get(
            ... to_zones=["United States"],
            ... products=["crude"],
            ... with_forecast=False,
            ... with_intra_country=True,
            ... start_date=date.today() - timedelta(days=7),
            ... columns=[
            ...     "vessel_name",
            ...     "closest_ancestor_product",
            ...     "closest_ancestor_grade",
            ...     "start",
            ...     "end",
            ...     "origin_location_name",
            ...     "destination_location_name"
            ... ]
            ... )

            .. csv-table::
                :header: "vessel_name","closest_ancestor_product","closest_ancestor_grade","start","end","origin_location_name","destination_location_name"

                "Eco Bel Air","crude","Basrah","2020-11-01 14:20:00","2020-12-14 01:02:00","Al Basrah","PADD 5"
                "Stella","crude","NaN","2020-10-30 09:48:00","2020-12-09 21:30:00","Angra dos Reis","PADD 5"
                "Cap Charles","crude","NaN","2020-10-21 05:47:00","2020-11-20 23:15:00","Angra dos Reis","Long Beach"
                "Sebarok Spirit","crude","Maya","2020-10-21 01:00:00","2020-10-24 06:49:00","Yuum Kak Naab FPSO","Houston"
                "Montreal Spirit","crude","NaN","2020-10-20 13:30:00","2020-11-24 01:18:00","Sao Sebastiao","Cherry Point"
                "Washington","crude","ANS","2020-10-19 14:48:00","2020-10-27 00:00:00","Valdez","San Francisco"
                "...","...","...","...","...","...","..."
        """

        self.with_product_estimation = with_product_estimation

        query_parameters: Dict[str, Optional[Any]] = {
            "size": size,
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
            "destinationStartDate": process_date_parameter(destination_start_date),
            "destinationEndDate": process_date_parameter(destination_end_date),
            "tradeStatus": process_enum_parameters(trade_status),
            "withForecast": process_bool_parameter(with_forecast),
            "withIntraCountry": process_bool_parameter(with_intra_country),
            "withIntraRegion": process_bool_parameter(with_intra_region),
            "columns": process_list_parameter(columns),
            "withFreightView": process_bool_parameter(with_freight_view),
            "withProductEstimation": process_bool_parameter(with_product_estimation),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)

    def validate(self):
        if self.with_product_estimation and self.configuration.platform != Platform.Liquids:
            raise WithProductEstimationPlatformException()
