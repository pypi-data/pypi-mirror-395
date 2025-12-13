from datetime import date
from enum import Enum
from typing import List, Optional

from kpler.sdk import Platform, SupplyDemandUsBalancesCrude, SupplyDemandUsBalancesGasoline
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import (
    process_date_parameter,
    process_enum_parameter,
    process_enum_parameters,
    process_list_parameter,
)


class SupplyDemandUsBalancesMetric:
    crude = SupplyDemandUsBalancesCrude
    gasoline = SupplyDemandUsBalancesGasoline


class SupplyDemand(KplerClient):
    """
    The ``SupplyDemand`` endpoint returns supply and demand metrics data values aggregated or split by country for a given product/ zone/ time period/selected snapshot,
    It also allows listing the available products and snapshots for the main endpoint
    """

    RESOURCE_NAME = "supply-demand"

    AVAILABLE_PLATFORMS = [Platform.Liquids]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get(
        self,
        product: Optional[str] = None,
        metrics: Optional[List[Enum]] = None,
        split: Optional[Enum] = None,
        zones: Optional[List[str]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        snapshot_date: Optional[date] = None,
    ):
        """
        Args:
            product:  Optional[str] Name of product to retrieve data for
            metrics: Optional[List[Enum]] ``SupplyDemandMetric`` Returns only provided metrics
            split: Optional[Enum] ``SupplyDemandSplit`` Choose whether returned data are aggregated or split by country
            zones: Optional[List[str]] Names of countries/geographical zones
            start_date:  Optional[date] Start of the period (YYYY-MM-DD), must be after 2017-01-01
            end_date:  Optional[date] End of the period (YYYY-MM-DD), maximum of 18 month from today
            snapshot_date:  Optional[date] Date of the snapshot to retrieve data from (YYYY-MM-DD)

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.supply_demand import SupplyDemand
            ... from kpler.sdk import SupplyDemandSplit, SupplyDemandMetric
            ... sd_client = SupplyDemand(config)
            ... sd_client.get(
            ...     product="Crude/Co",
            ...     metrics=[SupplyDemandMetric.Supply, SupplyDemandMetric.Demand],
            ...     start_date=date(2020,10,1),
            ...     end_date=date(2020,11,1),
            ...     zones=["Japan"],
            ...     split=SupplyDemandSplit.Total
            ... )

            .. csv-table::
                :header: "Snapshot Date","Date","Product","Metric","Zones","Value","Unit"

                "2022-09-15","2020-10-01","Crude/Co",Supply (kbd),"Japan","3","kbd"
                "2022-09-15","2020-10-01","Crude/Co",Demand (kbd),"Japan","2279","kbd"
                "2022-09-15","2020-10-01","Crude/Co",Supply (kbd),"Japan","3","kbd"
                "2022-09-15","2020-10-01","Crude/Co",Demand (kbd),"Japan","2504","kbd"
        """

        query_parameters = {
            "product": product,
            "metrics": process_enum_parameters(metrics, to_lower_case=False),
            "zones": process_list_parameter(zones),
            "split": process_enum_parameter(split, to_lower_case=False),
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "snapshotDate": process_date_parameter(snapshot_date),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)

    def get_snapshots(
        self,
        product: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ):
        """
        Args:
            product:  Optional[str] Name of product to retrieve snapshots for
            start_date:  Optional[date] Start of the period (YYYY-MM-DD)
            end_date:  Optional[date] End of the period (YYYY-MM-DD)
        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.supply_demand import SupplyDemand
            ... sd_client = SupplyDemand(config)
            ... sd_client.get_snapshots(
            ...     product="Crude/Co",
            ...     start_date=date(2022,08,1),
            ...     end_date=date(2022,10,1),
            ... )

            .. csv-table::
                :header: "Date","Product"

                "2022-08-14","Crude/Co"
                "2022-09-01","Crude/Co"
        """
        query_parameters = {
            "product": product,
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
        }
        return self._get_dataframe(self.RESOURCE_NAME + "/snapshots", query_parameters)

    def get_products(self):
        """
        Args: None
        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.supply_demand import SupplyDemand
            ... sd_client = SupplyDemand(config)
            ... sd_client.get_products()

            .. csv-table::
                :header: "Product","metrics","Snapshot Start Date","Snapshot End Date"

                Crude/Co,"supply,demand,refineryRun,directCrudeUse,balance,netExport,stockChange,balancingFactor",2022-08-15,2022-09-15
        """
        return self._get_dataframe(self.RESOURCE_NAME + "/products", params={})

    def get_us_balances(
        self,
        product: Optional[Enum] = None,
        metrics: Optional[List[Enum]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        granularity: Optional[Enum] = None,
    ):
        """
        Args:
            product:  Optional[Enum] Name of product to retrieve data for
            metrics: Optional[List[Enum]] ``SupplyDemandMetric`` Returns only provided metrics
            start_date:  Optional[date] Start of the period (YYYY-MM-DD), must be after 2017-01-01
            end_date:  Optional[date] End of the period (YYYY-MM-DD), maximum of 12 month from today
            granularity:  Optional[Enum] ``SupplyDemandUsBalancesGranularity`` Choose the granularity of the data

        Examples:
            >>> from datetime import date
            ... from kpler.sdk.resources.supply_demand import SupplyDemand, SupplyDemandUsBalancesMetric
            ... from kpler.sdk import SupplyDemandUsBalancesGranularity, SupplyDemandUsBalancesProduct
            ... sd_client = SupplyDemand(config)
            ... sd_client.get_us_balances(
            ...     product=SupplyDemandUsBalancesProduct.Crude,
            ...     metrics=[SupplyDemandUsBalancesMetric.crude.NetImport],
            ...     start_date=date(2020,1,1),
            ...     end_date=date(2020,6,1),
            ...     granularity=SupplyDemandUsBalancesGranularity.Weekly

            .. csv-table::
                :header: "Snapshot Date","Date","Product","Metric","Zones","Value","Unit"

                "2024-03-28","2023-01-01","Crude/Co","netImport","United States","3243","kbd"
                "2024-03-28","2023-02-01","Crude/Co","netImport","United States","2657","kbd"
                "2024-03-28","2023-03-01","Crude/Co","netImport","United States","2261","kbd"
        """
        query_parameters = {
            "product": process_enum_parameter(product, to_lower_case=False),
            "metrics": process_enum_parameters(metrics, to_lower_case=False),
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "granularity": process_enum_parameter(granularity, to_lower_case=False),
        }
        return self._get_dataframe(self.RESOURCE_NAME + "/us-balances", query_parameters)
