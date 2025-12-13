from datetime import date
from enum import Enum
from typing import List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import (
    process_bool_parameter,
    process_date_parameter,
    process_enum_parameter,
    process_list_parameter,
)


class Inventories(KplerClient):

    """
    The ``Inventories`` endpoint returns inland crude oil stocks of a given point of interest, with a specific periodicity over a period of time.
    Waterborne Cargoes, local Supply and Demand will also be returned for the given point of interest.
    """

    RESOURCE_NAME = "inventories"

    AVAILABLE_PLATFORMS = [Platform.Liquids]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint inventories.

        Examples:
            >>> from kpler.sdk.resources.inventories import Inventories
            ... inventories_client = Inventories(config)
            ... inventories_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "date","Date","Date for which values are provided","False","date yyyy-MM-dd"
                "zone_name","Zone","Name of the area of interest","False","string"
                "installation_name","Installation","Name of the installation","False","string"
                "level_barrels","Level (kb)","Amount of crude oil stored in kb","False","double"
                "local_suply_barrels","Local Supply (kbd)","Net overland inflow of crude oil (due to local oilfields, or pipelines) in kbd","False","double"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self,
        size: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        installations: Optional[List[str]] = None,
        zones: Optional[List[str]] = None,
        period: Optional[Enum] = None,
        split: Optional[Enum] = None,
        columns: Optional[List[str]] = None,
        cargo_tracking_enhancement: Optional[bool] = None,
        add_commodities_on_water: Optional[bool] = None,
        floating_storage_duration_min: Optional[str] = None,
        floating_storage_duration_max: Optional[str] = None,
        without_eia_adjustment: Optional[bool] = None,
    ):
        """
        Args:
            size:  Optional[int] Maximum number of contracts returned
            start_date:  Optional[date] Start of the period (YYYY-MM-DD)
            end_date:  Optional[date] End of the period (YYYY-MM-DD)
            installations: Optional[List[str]] Names of installations
            zones: Optional[List[str]] Names of countries/geographical zones
            period: Optional[Enum] ``InventoriesPeriod``
            split: Optional[Enum] ``InventoriesSplit``
            columns: Optional[List[str]] Retrieve all available columns when set to "all"
            cargo_tracking_enhancement:  Optional[bool] Use cargo tracking data to fill the blanks in between satellite images (default: False)
            add_commodities_on_water: Optional[bool] Provides total volume of inventories including offshore and offshore. Default to false if not specified.
            floating_storage_duration_min: Optional[str] Minimum floating days [7-10-12-15-20-30-90]
            floating_storage_duration_max: Optional[str] Maximum floating days [10-12-15-20-30-90-Inf]
            without_eia_adjustment:  Optional[bool] No use of EIA data for enhancing inventories volumes (default: False)

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.inventories import Inventories
            ... from kpler.sdk import InventoriesSplit
            ... inventories_client = Inventories(config)
            ... inventories_client.get(
            ...     start_date=date(2020,10,1),
            ...     end_date=date(2020,11,1),
            ...     zones=["Japan"],
            ...     split=InventoriesSplit.Total
            ... )

            .. csv-table::
                :header: "Date","Zone","Installation","Level (kb)","Local Supply (kbd)","Local Demand (kbd)","Cargoes (kbd)","Capacity (kb)","..."

                "2020-10-01 23:59:00","Japan","NaN","354342","0","2377","2594","474008"","
                "2020-10-02 23:59:00","Japan","NaN","354492","0","2090","2705","474008"
                "2020-10-03 23:59:00","Japan","NaN","354178","0","2087","1101","474008"
                "2020-10-04 23:59:00","Japan","NaN","354073","0","1883","2500","474008"
                "2020-10-05 23:59:00","Japan","NaN","354187","0","1862","916","474008"
                "...","...","...","...","...","...","...","..."

        """

        query_parameters = {
            "size": size,
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "installations": process_list_parameter(installations),
            "zones": process_list_parameter(zones),
            "period": process_enum_parameter(period),
            "split": process_enum_parameter(split),
            "columns": process_list_parameter(columns),
            "cargoTrackingEnhancement": process_bool_parameter(cargo_tracking_enhancement),
            "addCommoditiesOnWater": process_bool_parameter(add_commodities_on_water),
            "floatingStorageDurationMin": floating_storage_duration_min,
            "floatingStorageDurationMax": floating_storage_duration_max,
            "withoutEiaAdjustment": process_bool_parameter(without_eia_adjustment),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
