from datetime import date
from typing import List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import process_bool_parameter, process_date_parameter, process_list_parameter


class ShipToShips(KplerClient):
    """
    The ``ShipToShips`` endpoint returns the ship-to-ships loadings/discharges in a given zone,with details on the
    vessels taking part in the operation and crude grades being exchanged for a given time period.
    """

    RESOURCE_NAME = "ship-to-ships"

    AVAILABLE_PLATFORMS = [Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint ship-to-ships.

        Examples:
            >>> from kpler.sdk.resources.ship_to_ships import ShipToShips
            ... ship_to_ships_client = ShipToShips(config)
            ... ship_to_ships_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "load_vessel_name","Vessel (load)","Name of the vessel load","False","string"
                "load_vessel_imo","IMO (load)","IMO of the vessel load","False","string"
                "discharge_vessel_name","Vessel (discharge)","Name of the vessel discharge","False","string"
                "discharge_vessel_imo","IMO (discharge)","IMO of the vessel discharge","False","string"
                "flow_quantity_cms","Volume (cm)","None","False","long"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self,
        size: Optional[int] = None,
        vessels: Optional[List[str]] = None,
        zones: Optional[List[str]] = None,
        products: Optional[List[str]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        columns: Optional[List[str]] = None,
        with_freight_view: bool = False,
    ):
        """

        Args:
             size: Optional[int] Maximum number of sts returned
             vessels: Optional[List[str]] Names/IMOs of vessels
             zones: Optional[List[str]] Names of zones ["port", "lightering", "region", "country", "continent"]
             products: Optional[List[str]] Names of products
             start_date: Optional[date] Start of the period (YYYY-MM-DD)
             end_date: Optional[date] End of the period (YYYY-MM-DD)
             columns: Optional[List[str]] Retrieve all available columns when set to "all"
             with_freight_view: bool By default: with_freight_view=False. Provides access to the entire fleet's trades, irrespective of your current cargo subscription. Only available via Freight subscription.

        Examples:
            >>> from kpler.sdk.resources.ship_to_ships import ShipToShips
            ... ship_to_ships_client = ShipToShips(config)
            ... ship_to_ships_client.get(
            ...     zones=["Zeebrugge"],
            ...     columns=["load_vessel_name","load_vessel_imo","discharge_vessel_name","discharge_vessel_imo","flow_quantity_cms","zone_name","start","end"]
            ... )

            .. csv-table::
                :header: "load_vessel_name","load_vessel_imo","discharge_vessel_name","discharge_vessel_imo","zone_name","start","end"

                "Red Opal","9381512","Team Falcon","9396012","Zeebrugge","2017-06-02 18:06:00","2017-06-02 18:06:00"
                "Adebomi 3","9210907","Dong-A Maia","9749544","Zeebrugge","2017-04-26 01:02:00","2017-04-26 05:05:00"
                "Lafayette Bay","9717785","Sloman Themis","9306677","Zeebrugge","2017-02-24 02:00:00","2017-02-24 04:00:00"
                "Talara","9569994","Lafayette Bay","9717785","Zeebrugge","2017-02-23 22:31:00","2017-02-23 23:00:00"
                "Hafnia Hope","9360415","Nave Bellatrix","9459084","Zeebrugge","2017-01-12 22:01:00","2017-01-12 23:01:00"
                "...","...","...","...","...","...","...","..."

        """

        query_parameters = {
            "size": size,
            "vessels": process_list_parameter(vessels),
            "zones": process_list_parameter(zones),
            "products": process_list_parameter(products),
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "columns": process_list_parameter(columns),
            "withFreightView": process_bool_parameter(with_freight_view),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
