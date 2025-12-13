from typing import List, Optional

from pandas import DataFrame

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.helpers import process_list_parameter


class Products(KplerClient):
    """
    The ``Products`` endpoint allows to perform full-text search on products,
    in order to find names used in Kpler referential.
    """

    RESOURCE_NAME = "products"

    AVAILABLE_PLATFORMS = [Platform.Dry, Platform.Liquids, Platform.LNG, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get_columns(self) -> DataFrame:
        """
        This endpoint returns a recent and updated list of all columns available for the endpoint products.

        Examples:
            >>> from kpler.sdk.resources.products import Products
            ... products_client = Products(config)
            ... products_client.get_columns()

            .. csv-table::
                :header: "id","name","description","deprecated","type"

                "id","Id (Product)","Identifier in the database of Kpler","False","long"
                "name","Name","Name of the product","False","string"
                "product_type","Type (Product)","Product Type","False","string"
                "family_name","Family","closest Family to the product","False","string"
                "family_id","Family Id","Id of the closest Family to the product","False","long"
                "...","...","...","...","..."
        """
        return self._get_columns_for_resource(self.RESOURCE_NAME)

    def get(
        self,
        columns: Optional[List[str]] = None,
        size: Optional[int] = None,
        ancestor_family_ids: Optional[List[int]] = None,
        ancestor_family_names: Optional[List[str]] = None,
        ancestor_group_ids: Optional[List[int]] = None,
        ancestor_group_names: Optional[List[str]] = None,
        ancestor_product_ids: Optional[List[int]] = None,
        ancestor_product_names: Optional[List[str]] = None,
        ancestor_grade_ids: Optional[List[int]] = None,
        ancestor_grade_names: Optional[List[str]] = None,
        products: Optional[List[str]] = None,
        product_ids: Optional[List[int]] = None,
    ) -> DataFrame:
        """

        Args:
            size:  Optional[int]
            ancestor_family_ids:  Optional[List[int]] IDs of a product Family. Can be separated by a coma
            ancestor_family_names:  Optional[List[str]] Default to the whole tree if not specified. Possible values are : Light Ends, NPC, DPP, Middle Distillate, Dirty
            ancestor_group_ids:  Optional[List[int]] IDs of a product Group. Can be separated by a coma
            ancestor_group_names:  Optional[List[str]] Default to the whole tree if not specified. Possible values are : Kero/Jet, Crude/Co, , Fuel Oils, etc...
            ancestor_product_ids:  Optional[List[int]] IDs of a product Product. Can be separated by a coma.
            ancestor_product_names:  Optional[List[str]] Default to the whole tree if not specified. Possible values are : Jet, Crude, Clean Condensate, etc ...
            ancestor_grade_ids:  Optional[List[int]] IDs of a product Grade. Can be separated by a coma.
            ancestor_grade_names:  Optional[List[str]] Default to the whole tree if not specified. Possible values are : RBOB, Solvent Naphtha, LSHO, 91 Gasoline,...
            products:  Optional[List[str]] Names of Products of all different tree levels (Family, Group, Product, Grade)
            product_ids: Optional[List[int]] Ids of possible products. Can be separated by a coma
            columns: Optional[List[str]] Retrieve all available columns when set to "all"

        Examples:
            >>> from kpler.sdk.resources.products import Products
            ... products_client = Products(config)
            ... products_client.get(ancestor_group_names=["Fuel Oils"], columns=["id", "family_name", "group_name", "product_name", "grade_name"])

            .. csv-table::
                :header: "id", "family_name", "group_name", "product_name", "grade_name"

                "2715","Dirty","Crude/Co","Crude","EOPL Heavy"
                "2716","Chem/Bio","Vegoils/Biofuels","Biofuels","SAF"
                "2717","Middle Distillates","Gasoil/Diesel","Diesel","Diesel B5"
                "2718","Dirty","Crude/Co","Crude","Suez Blend"
                "2728","Chem/Bio","Vegoils/Biofuels","Animal Fats",""
                "...","...","...","..."
        """
        query_parameters = {
            "size": process_list_parameter(size),
            "ancestorFamilyIds": process_list_parameter(ancestor_family_ids),
            "ancestorFamilyNames": process_list_parameter(ancestor_family_names),
            "ancestorGroupIds": process_list_parameter(ancestor_group_ids),
            "ancestorGroupNames": process_list_parameter(ancestor_group_names),
            "ancestorProductIds": process_list_parameter(ancestor_product_ids),
            "ancestorProductNames": process_list_parameter(ancestor_product_names),
            "ancestorGradeIds": process_list_parameter(ancestor_grade_ids),
            "ancestorGradeNames": process_list_parameter(ancestor_grade_names),
            "products": process_list_parameter(products),
            "productIds": process_list_parameter(product_ids),
            "columns": process_list_parameter(columns),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)

    def search(self, q: str) -> DataFrame:
        """

        Args:
            q: str Argument to search by in products names

        Examples:
            >>> from kpler.sdk.resources.products import Products
            ... products_client=Products(config)
            ... products_client.search("Arab")

            .. csv-table::
                :header: "products"

                "Arab"
                "Arab M"
                "Arab M Abu Safah"
                "Arab SLt."
                "Arab XLt."
                "Arab Hy."
                "Arab Lt."
        """
        query_parameters = {"q": q, "resources": self.RESOURCE_NAME}
        return self._search(query_parameters)
