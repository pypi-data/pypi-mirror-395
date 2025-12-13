from datetime import date
from enum import Enum
from typing import List, Optional

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import (
    process_bool_parameter,
    process_date_parameter,
    process_enum_parameter,
    process_enum_parameters,
    process_list_parameter,
)


class FleetMetrics(KplerClient):

    """
    The ``FleetMetrics`` endpoint provides you with aggregated fleet data per day or week, either the floating storage or all
    the loaded vessels.
    """

    RESOURCE_NAME = "fleet-metrics"

    AVAILABLE_PLATFORMS = [Platform.Liquids, Platform.LPG, Platform.LNG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        zones: Optional[List[str]] = None,
        metric: Optional[Enum] = None,
        period: Optional[Enum] = None,
        floating_storage_duration_min: Optional[str] = None,
        floating_storage_duration_max: Optional[str] = None,
        products: Optional[List[str]] = None,
        unit: Optional[Enum] = None,
        split: Optional[Enum] = None,
        with_freight_view: bool = False,
        vessel_types: Optional[List[Enum]] = None,
        vessel_types_alt: Optional[List[Enum]] = None,
    ):

        """
        Args:
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            zones: Optional[List[str]] Names of countries/geographical zones
            metric: Optional[Enum] ``FleetMetricsAlgo``
            period: Optional[Enum] ``FleetMetricsPeriod``
            floating_storage_duration_min: Optional[str] Minimum floating days [7-10-12-15-20-30-90] or [1-3-5-7-10-12-15-20-30-90] on LNG platform
            floating_storage_duration_max: Optional[str] Maximum floating days [7-10-12-15-20-30-90-Inf] or [1-3-5-7-10-12-15-20-30-90-Inf] on LNG platform
            products: Optional[List[str]] Names of products. Not available on LNG platform
            unit: Optional[Enum] ``FleetMetricsMeasurementUnit`` by default return in bbl unit or cm on LNG platform
            split: Optional[Enum] ``FleetMetricsSplit``
            with_freight_view: bool By default: with_freight_view=False. Provides access to the entire fleet's trades, irrespective of your current cargo subscription. Only available via Freight subscription.
            vessel_types: Optional[List[Enum]] = Vessel types, pick types based on platform.
            vessel_types_alt: Optional[List[Enum]] = For oil vessel types, only available for Liquids

        Examples:

            >>> from kpler.sdk.resources.fleet_metrics import FleetMetrics
            ... from kpler.sdk import FleetMetricsAlgo, FleetMetricsSplit, FleetMetricsPeriod
            ... fleet_metrics_client = FleetMetrics(config)
            ... fleet_metrics_client.get(
            ...     metric=FleetMetricsAlgo.LoadedVessels,
            ...     zones=["China"],
            ...     period=FleetMetricsPeriod.Daily,
            ...     split=FleetMetricsSplit.CurrentSubregions
            ... )

             .. csv-table::
                :header:  "Date","Hubei","Jiangsu Province","Anhui","Shanghai Province","Liaoning","Zhejiang","Hainan","Hunan","Fujian","..."

                "2019-10-27","0.0","5162437.50","0.00","2701888.77","11170477.14","13718894.53","713446.92","0.0","3467654.33","..."
                "2019-10-28","0.0","4570962.59","0.00","3004283.99","10789081.90","13882417.02","1083772.10","0.0","2644236.36","..."
                "2019-10-29","0.0","6341355.57","149716.36","4651774.07","11371285.63","14548268.95","1672749.96","0.0","4543149.04","..."
                "2019-10-30","0.0","4157074.18","0.00","2306649.65","14003942.45","13719347.39","1443052.37","0.0","2017324.65","..."
                "2019-10-31","0.0","4251597.45","0.00","4825448.32","10310188.30","13959762.82","3180612.54","0.0","2523402.81","..."
                "..","..","..","..","..","..","..","..","..","..",".."
        """

        query_parameters = {
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "zones": process_list_parameter(zones),
            "metric": process_enum_parameter(metric),
            "period": process_enum_parameter(period),
            "floatingStorageDurationMin": floating_storage_duration_min,
            "floatingStorageDurationMax": floating_storage_duration_max,
            "products": process_list_parameter(products),
            "unit": process_enum_parameter(unit),
            "split": process_enum_parameter(split),
            "withFreightView": process_bool_parameter(with_freight_view),
            "vesselTypes": process_enum_parameters(vessel_types, to_lower_case=False),
            "vesselTypesAlt": process_enum_parameters(vessel_types_alt, to_lower_case=False),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
