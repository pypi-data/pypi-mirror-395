from datetime import date
from enum import Enum
from typing import List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import (
    process_date_parameter,
    process_enum_parameter,
    process_enum_parameters,
    process_list_parameter,
)


class CrudeImports(KplerClient):
    """
    The CrudeImports endpoint returns the 30days moving average crude imports
    for a point of interest (installation/zone) on a daily, weekly, weekly EIA (for US), monthly and yearly basis.
    It also provides the weighted average API and Sulfur values over time.
    """
    API_SULFUR_RESOURCE_NAME = "refineries/api-sulfur"

    RESOURCE_NAME = "refineries/crude-imports"

    AVAILABLE_PLATFORMS = [Platform.Liquids]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint
        refineries crude-imports.


        Examples:
            >>> from kpler.sdk.resources.refineries.crude_imports import CrudeImports
            ... crude_imports_client = CrudeImports(config)
            ... crude_imports_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "date","Date (timestamp)","Date (timestamp)","False","date yyyy-MM-dd"
                "zones","Zones","Zones the row's data uses","False","list of string"
                "installations","Installations","Instalations the row's data uses","False","list of string"
                "splitValue","Split Value","Split Value","False","string"
                "metric","Metric","Metric","False","string"
                "...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get_api_sulfur_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint refineries
        crude-imports api-sulfur.


        Examples:
            >>> from kpler.sdk.resources.refineries.crude_imports import CrudeImports
            ... crude_imports_client = CrudeImports(config)
            ... crude_imports_client.get_api_sulfur_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "date","Date (timestamp)","Date, within the start_date and end_date. Data is provided with ascending order on date. Format YYYY-MM-DD.","False","string"
                "zones","Zones","List of zones specified in the parameter zones.","False","list of string"
                "installations","Installations","List of installations specified in the parameter installations.","False","list of string"
                "splitValue","Split Value","Name of the bucket corresponding to the specified split. EG Americas or Asia for split by Continent.","False","string"
                "metric","Metric","Corresponding to the endpoint.","False","string"
                "...","..."
        """
        return self._get_columns_for_resource(self.API_SULFUR_RESOURCE_NAME)

    def get(
            self,
            players: Optional[List[str]] = None,
            installations: Optional[List[str]] = None,
            zones: Optional[List[str]] = None,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None,
            products: Optional[List[Enum]] = None,
            unit: Optional[Enum] = None,
            granularity: Optional[Enum] = None,
            split: Optional[Enum] = None,
            metric: Optional[Enum] = None

    ) -> DataFrame:
        """
        Args:
            players:  Optional[str] Names of players
            installations: Optional[List[str]] Names of installations
            zones: Optional[List[str]] Names of countries/geographical zones
            start_date:  Optional[date] Start of the period (YYYY-MM-DD), must be after 2017-01-01
            end_date:  Optional[date] End of the period (YYYY-MM-DD), maximum of 7 days from today
            products: Optional[List[Enum]] ``RunsQualities`` Names of qualities
            unit: Optional[Enum] ``ImportsUnit``
            granularity: Optional[Enum] ``ImportsGranularity``
            split: Optional[Enum] ``ImportsSplit``
            metric: Optional[Enum] ``ImportsMetric`` Returns only provided metrics
        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.refineries.crude_imports import CrudeImports
            ... from kpler.sdk import ImportsSplit, ImportsGranularity, RunsQualities, ImportsUnit, ImportsMetric
            ... crude_imports_client = CrudeImports(config)
            ... crude_imports_client.get(
            ...     installations=["xxxx"],
            ...     zones=["United States"],
            ...     start_date=date(2023, 4, 1),
            ...     end_date=date(2023, 7, 31),
            ...     player=["xxx"],
            ...     products=[RunsQualities.All],
            ...     unit=ImportsUnit.KBD,
            ...     granularity=ImportsGranularity.Monthly,
            ...     split=ImportsSplit.Total,
            ...     metric=ImportsMetric.Quantity,
            ... )

            .. csv-table::
                :header: "Date","Zones","Installations","Split Value","Metric","Value","Unit"

                "2023-04-01","United States",,"Total","Imports","79644.0","kbd"
                "2023-05-01","United States",,"Total","Imports","79417.0","kbd"
                "2023-06-01","United States",,"Total","Imports","79540.0","kbd"
                "2023-07-01","United States",,"Total","Imports","81059.0","kbd"

                "2023-04-01","United States",,"Total","API - Weighted average","33.5","° API"
                "2023-04-01","United States",,"Total","Sulfur - Weighted average","1.24","% wt"
                "2023-05-01","United States",,"Total","API - Weighted average","33.4","° API"
                "2023-05-01","United States",,"Total","Sulfur - Weighted average","1.25","% wt"
                "2023-06-01","United States",,"Total","API - Weighted average","33.3","° API"
        """

        query_parameters = {
            "players": process_list_parameter(players),
            "installations": process_list_parameter(installations),
            "zones": process_list_parameter(zones),
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "products": process_enum_parameters(products, to_lower_case=False),
            "split": process_enum_parameter(split, to_lower_case=False),
            "granularity": process_enum_parameter(granularity, to_lower_case=False),
            "unit": process_enum_parameter(unit, to_lower_case=False),
            "metric": process_enum_parameter(metric, to_lower_case=False)
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
