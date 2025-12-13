from datetime import date
from typing import List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import process_bool_parameter, process_date_parameter, process_list_parameter


class PortCalls(KplerClient):
    """
    The ``PortCalls`` query returns the cargo-by-cargo details for loadings/discharges taking place in a point of
    interest (installation/zone).
    """

    RESOURCE_NAME = "port-calls"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint port-calls.

        Examples:
            >>> from kpler.sdk.resources.port_calls import PortCalls
            ... port_calls_client = PortCalls(config)
            ... port_calls_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "vessel_name","Vessel","Name of the vessel","False","string"
                "installation_name","Installation","Name of the installation","False","string"
                "eta","ETA","Estimated date and time of arrival at next destination","False","datetime yyyy-MM-dd HH:mm"
                "start","Start","Date and Time when the vessel started berthing at the terminal","False","datetime yyyy-MM-dd HH:mm"
                "end","End","Date and Time of vessel departure from the terminal","False","datetime yyyy-MM-dd HH:mm"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self,
        size: Optional[int] = None,
        vessels: Optional[List[str]] = None,
        installations: Optional[List[str]] = None,
        zones: Optional[List[str]] = None,
        products: Optional[List[str]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        with_forecast: Optional[bool] = None,
        columns: Optional[List[str]] = None,
        with_freight_view: bool = False,
        with_empty_volume: Optional[bool] = None,
    ) -> DataFrame:
        """

        Args:
             size: Optional[int] Maximum number of portcalls
             vessels: Optional[List[str]] Names/IMOs of vessels
             installations: Optional[List[str]] Names of installations
             zones: Optional[List[str]] Names of zones ["port", "region", "country", "continent"]
             products: Optional[List[str]] Names of products
             start_date: Optional[date] Start of the period (YYYY-MM-DD)
             end_date: Optional[date] End of the period (YYYY-MM-DD)
             with_forecast: Optional[bool] By default: withForecast=true. Include trades predicted by our in-house model when set to "true". Use ["true", "false"]
             columns: Optional[List[str]] Retrieve all available columns when set to "all"
             with_freight_view: bool By default: with_freight_view=False. Provides access to the entire fleet's trades, irrespective of your current cargo subscription. Only available via Freight subscription.
             with_empty_volume: Optional[bool] By default: withEmptyVolume=false. Include port calls with empty volumes when set to "true". Use ["true", "false"]

        Examples:
            >>> from kpler.sdk.resources.port_calls import PortCalls
            ... port_calls_client = PortCalls(config)
            ... port_calls_client.get(
            ...     start_date=date.today() - timedelta(days=7),
            ...     zones=["United States"],
            ...     installations=["Everglades"],
            ...     columns=["vessel_name","installation_name","eta","start","end","flow_quantity_cubic_meters"]
            ... )

            .. csv-table::
                :header: "vessel_name","installation_name","eta","start","end","flow_quantity_cubic_meters"

                "Palmetto State","Everglade","2020-12-11 21:00:00","NaT","NaT","-29681.0"
                "Golden State","Everglade","2020-12-10 17:00:00","NaT","NaT","-53477.0"
                "Overseas Houston","Everglade","2020-12-09 11:00:00","NaT","NaT","-51560.0"
                "Garden State","Everglade","2020-12-09 02:00:00","NaT","NaT","-54045.0"
                "American Liberty","Everglade","2020-12-08 22:00:00","NaT","NaT","-54736.0"
                "Louisiana","Everglade","2020-12-06 16:00:00","2020-12-06 18:01:00","2020-12-07 03:05:00","-9445.0"
                "California Voyager","Everglade","2020-12-04 03:00:00","2020-12-04 03:28:00","2020-12-05 11:51:00","-37295.0"
                "Brenton Reef","Everglade","2020-12-02 20:30:00","2020-12-02 21:56:00","2020-12-04 02:00:00","-50339.0"
                "...","...","...","...","...","..."
        """

        query_parameters = {
            "size": size,
            "vessels": process_list_parameter(vessels),
            "installations": process_list_parameter(installations),
            "zones": process_list_parameter(zones),
            "products": process_list_parameter(products),
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "withForecast": process_bool_parameter(with_forecast),
            "columns": process_list_parameter(columns),
            "withFreightView": process_bool_parameter(with_freight_view),
            "withEmptyVolume": process_bool_parameter(with_empty_volume),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
