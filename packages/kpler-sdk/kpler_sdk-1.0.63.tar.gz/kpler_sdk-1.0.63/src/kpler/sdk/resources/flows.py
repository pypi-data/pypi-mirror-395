from datetime import date
from enum import Enum
from typing import List, Optional

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import (
    process_bool_parameter,
    process_date_parameter,
    process_enum_parameters,
    process_flow_snapshot_parameter,
    process_list_parameter,
)


class Flows(KplerClient):
    """
    The ``Flows`` endpoint returns the aggregated flows for a point of interest (installation/zone) on a daily, weekly,
    weekly EIA (for US), monthly and yearly basis.
    """

    RESOURCE_NAME = "flows"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get(
        self,
        flow_direction: Optional[List[Enum]] = None,
        split: Optional[List[Enum]] = None,
        granularity: Optional[List[Enum]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        from_installations: Optional[List[str]] = None,
        to_installations: Optional[List[str]] = None,
        from_zones: Optional[List[str]] = None,
        to_zones: Optional[List[str]] = None,
        products: Optional[List[str]] = None,
        only_realized: Optional[bool] = None,
        unit: Optional[List[Enum]] = None,
        with_intra_country: Optional[bool] = None,
        with_intra_region: Optional[bool] = None,
        with_forecast: Optional[bool] = None,
        with_freight_view: bool = False,
        vessel_types: Optional[List[Enum]] = None,
        vessel_types_alt: Optional[List[Enum]] = None,
        with_product_estimation: bool = False,
        snapshot_date: Optional[date] = None, 
    ):
        """

        Args:
             flow_direction: Optional[List[Enum]] ``FlowsDirection``
             split: Optional[List[Enum]] ``FlowsSplit``
             granularity: Optional[List[Enum]] ``FlowsPeriod``
             start_date: Optional[date] Start of the period (YYYY-MM-DD)
             end_date: Optional[date] End of the period (YYYY-MM-DD)
             from_installations: Optional[List[str]] Names of installations
             to_installations: Optional[List[str]] Names of installations
             from_zones: Optional[List[str]] Names of zones ["port", "region", "country", "continent"]
             to_zones: Optional[List[str]] = Names of zones ["port", "region", "country", "continent"]
             products: Optional[List[str]] = Names of products
             only_realized: Optional[bool] By default: onlyRealized=false. Takes into account only the trades that have been finished. Use ["true", "false"]
             unit: Optional[List[Enum]] ``FlowsMeasurementUnit``
             with_intra_country: Optional[bool] By default: withIntraCountry=false. Takes into account the trades within the selected country. Use ["true", "false"]
             with_intra_region: Optional[bool] By default: withIntraRegion=true. Takes into account the trades within the selected region. Use ["true", "false"]
             with_forecast: Optional[bool] By default: withForecast=true. Include trades predicted by our in-house model when set to "true". Use ["true", "false"]
             with_freight_view: bool By default: with_freight_view=False. Provides access to the entire fleet's trades, irrespective of your current cargo subscription. Only available via Freight subscription.
             vessel_types: Optional[List[Enum]] = Vessel types, pick types based on platform.
             vessel_types_alt: Optional[List[Enum]] = For oil vessel types, only available for Liquids
             with_product_estimation: bool By default withProductEstimation=False. Activate the product estimation feature. When set to true, the estimated product will overwrite the existing product information.
             snapshot_date: Optional[date] Flows snapshot date, If not provided, will return the live results (YYYY-MM-DD)
             
        Examples:

            >>> from datetime import date
            ... from kpler.sdk.resources.flows import Flows
            ... from kpler.sdk import FlowsDirection, FlowsSplit, FlowsPeriod, FlowsMeasurementUnit
            ... flows_client = Flows(config)
            ... flows_client.get(
            ...     flow_direction=[FlowsDirection.Export],
            ...     split=[FlowsSplit.OriginCountries],
            ...     granularity=[FlowsPeriod.Daily],
            ...     unit=[FlowsMeasurementUnit.T],
            ...     start_date=date(2020,9,1),
            ...     end_date=date(2020,10,1)
            ... )

            .. csv-table::
                :header:  "","Belgium","Singapore Republic","Equatorial Guinea","Trinidad and Tobago","Peru","Qatar","Netherlands","Cameroon","France","..."

                "2020-09-01","0.00","0.00","0.00","31503.98","0.00","444830.12","0.0","0.00","0.00","..."
                "2020-09-02","0.00","0.00","0.00","29470.38","0.00","127286.51","0.0","0.00","0.00","..."
                "2020-09-03","0.00","0.00","0.00","0.00","0.00","217991.87","0.0","0.00","0.00","..."
                "2020-09-04","0.00","0.00","0.00","0.00","0.00","279156.75","0.0","0.00","75441.15","..."
                "2020-09-05","0.00","450.00","0.00","55242.96","77166.98","96567.48","3038.4","0.00","0.00","..."
                "2020-09-06","0.00","0.00","0.00","66487.50","0.00","281436.69","71762.4","34352.10","0.00",".."
                "..","..","..","..","..","..","..","..","..","..",".."
        """

        query_parameters = {
            "flowDirection": process_enum_parameters(flow_direction),
            "split": process_enum_parameters(split),
            "granularity": process_enum_parameters(granularity),
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "fromInstallations": process_list_parameter(from_installations),
            "toInstallations": process_list_parameter(to_installations),
            "fromZones": process_list_parameter(from_zones),
            "toZones": process_list_parameter(to_zones),
            "products": process_list_parameter(products),
            "onlyRealized": process_bool_parameter(only_realized),
            "unit": process_enum_parameters(unit),
            "withIntraCountry": process_bool_parameter(with_intra_country),
            "withIntraRegion": process_bool_parameter(with_intra_region),
            "withForecast": process_bool_parameter(with_forecast),
            "withFreightView": process_bool_parameter(with_freight_view),
            "vesselTypes": process_enum_parameters(vessel_types, to_lower_case=False),
            "vesselTypesAlt": process_enum_parameters(vessel_types_alt, to_lower_case=False),
            "withProductEstimation": process_bool_parameter(with_product_estimation),
            "snapshotDate": process_flow_snapshot_parameter(snapshot_date), 
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)
