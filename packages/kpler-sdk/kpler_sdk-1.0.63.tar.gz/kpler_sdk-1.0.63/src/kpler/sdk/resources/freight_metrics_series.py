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
    process_enum_parameters,
    process_list_parameter,
)


class FreightMetricsSeries(KplerClient):

    """
    The ``FreightMetricsSeries`` endpoint returns demand metrics like tonmiles & tondays as well as other metrics like average speed for laden fleet and average distance under this metric
    """

    RESOURCE_NAME = "freight-metrics/series-alt"
    COLUMNS_RESOURCE_NAME = "freight-metrics"
    COLUMNS_PATH = "columns-alt"

    AVAILABLE_PLATFORMS = [Platform.Liquids, Platform.LPG, Platform.LNG, Platform.Dry]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint freight-metrics.


        Examples:
            >>> from kpler.sdk.resources.freight_metrics_series import FreightMetricsSeries
            ... freight_metrics_series_client = FreightMetricsSeries(config)
            ... freight_metrics_series_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "date","Date (timestamp)","","False","string"
                "vessel_imo","IMO","IMO of the vessel","False","long"
                "vessel","Name","Name of the vessel","False","string"
                "vessel_dwt_tons","Dead Weight Tonnage","Dead Weight Tonnage","False","long"
                "vessel_type","Vessel Type","Type of the vessel","False","string"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.COLUMNS_RESOURCE_NAME, self.COLUMNS_PATH)

    def get(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        from_locations: Optional[List[str]] = None,
        to_locations: Optional[List[str]] = None,
        from_installations: Optional[List[str]] = None,
        to_installations: Optional[List[str]] = None,
        metric: Optional[Enum] = None,
        vessel_types_cpp: Optional[List[Enum]] = None,
        vessel_types_oil: Optional[List[Enum]] = None,
        products: Optional[List[str]] = None,
        period: Optional[Enum] = None,
        split: Optional[Enum] = None,
        unit: Optional[Enum] = None,
        with_intra_country: Optional[bool] = None,
        gte: Optional[int] = None,
        lte: Optional[int] = None,
        vessel_types: Optional[List[Enum]] = None,
        with_freight_view: bool = False,
        avg_speed_min: Optional[int] = None,
        avg_speed_max: Optional[int] = None,
        status: Optional[Enum] = None,
    ):

        """
        Args:
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            from_locations: Optional[str] Names of locations
            to_locations: Optional[str] Names of locations
            from_installations: Optional[str] Names of installations
            to_installations: Optional[str] Names of installations
            metric: Optional[Enum] ``FreightMetricsSeriesMetric``
            vessel_types_cpp: Optional[Enum] ``VesselTypesCPP``
            vessel_types_oil: Optional[Enum] ``VesselTypesOil``
            products: Optional[str] Names of products
            period: Optional[Enum] ``FreightMetricsSeriesPeriod``
            split: Optional[Enum] ``FreightMetricsSeriesSplit``
            unit: Optional[Enum] ``FreightMetricsSeriesUnit``
            with_intra_country: Optional[bool] By default: false. Takes into account the freight metric series within the selected region. Use ["true", "false"]
            gte: Optional[int] Get vessels with deadweight/capacity greater or equals to this value by default 0
            lte: Optional[int] Get vessels with deadweight/capacity lower or equals to this value by default 606550
            vessel_types: Optional[Enum] ``VesselTypesDry`` ``VesselTypesLNG`` ``VesselTypesLPG``
            with_freight_view: bool By default: with_freight_view=False. Provides access to the entire fleet's trades, irrespective of your current cargo subscription. Only available via Freight subscription.
            avg_speed_min: Optional[int] Get vessel legs with average speed greater or equal to this value
            avg_speed_max: Optional[int] Get vessel legs with average speed less than or equal to this value
            status: Optional[Enum] ``FreightMetricsSeriesStatus``

        Examples:

            >>> from datetime import date
            ... from kpler.sdk.resources.freight_metrics_series import FreightMetricsSeries
            ... from kpler.sdk import FreightMetricsSeriesMetric, FreightMetricsSeriesSplit, FreightMetricsSeriesUnit, FreightMetricsSeriesPeriod
            ... freight_metrics_series_client = FreightMetricsSeries(config)
            ... freight_metrics_series_client.get(
            ...     metric=FreightMetricsSeriesMetric.TonMiles,
            ...     split=FreightMetricsSeriesSplit.VesselTypeCpp,
            ...     products=["gasoline", "DPP"],
            ...     unit=FreightMetricsSeriesUnit.KTNMI,
            ...     period=FreightMetricsSeriesPeriod.Monthly,
            ...     start_date=date(2020,1,1)
            ... )

            .. csv-table::
                :header:  "Date","MR","GP","LR2","LR1","LR3","VLCC"

                "2020-01-01","47167787.97","4805725.69","46909311.58","20111132.52","25888954.41","1212255.41"
                "2020-02-01","44779639.94","4799508.63","48502313.55","19338796.56","18212888.97","1907541.54"
                "2020-03-01","53292249.51","5701420.14","46698177.92","22726753.15","14412986.37","3788115.98"
                "2020-04-01","41957007.33","5138045.73","48438084.70","20037436.18","11140717.43","2933625.42"
                "2020-05-01","43838067.51","5344708.32","50284110.11","13431154.99","13004547.35","3421934.68"
                "2020-06-01","42789911.76","4894000.27","41481731.47","13896678.66","13061101.23","3511137.65"
                "2020-07-01","45617055.75","5043752.13","46691881.74","21080645.36","10519866.61","2661771.76"
                "2020-08-01","44716307.74","4320194.82","48217646.71","16982323.71","9916214.49","5142621.42"
                "2020-09-01","43714237.43","4754961.40","38954591.64","17309605.01","15690640.13","784688.29"
                "2020-10-01","42514077.39","4729507.01","42225374.83","17845363.26","15703871.72","3513174.00"
                "2020-11-01","15881015.99","1990767.03","17269526.99","5727516.67","8022010.01","1737537.15"
        """

        query_parameters = {
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "fromLocations": process_list_parameter(from_locations),
            "toLocations": process_list_parameter(to_locations),
            "fromInstallations": process_list_parameter(from_installations),
            "toInstallations": process_list_parameter(to_installations),
            "metric": process_enum_parameter(metric),
            "vesselTypesCpp": process_enum_parameters(vessel_types_cpp),
            "vesselTypesOil": process_enum_parameters(vessel_types_oil),
            "products": process_list_parameter(products),
            "period": process_enum_parameter(period),
            "split": process_enum_parameter(split),
            "unit": process_enum_parameter(unit),
            "withIntraCountry": process_bool_parameter(with_intra_country),
            "gte": gte,
            "lte": lte,
            "vesselTypes": process_enum_parameters(vessel_types),
            "withFreightView": process_bool_parameter(with_freight_view),
            "avgSpeedMin": avg_speed_min,
            "avgSpeedMax": avg_speed_max,
            "status": process_enum_parameter(status),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
