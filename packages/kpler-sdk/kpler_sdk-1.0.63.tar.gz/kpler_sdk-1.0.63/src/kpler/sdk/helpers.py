from datetime import date, datetime
import enum
from io import StringIO
import logging
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd


logger = logging.getLogger(__name__)


def filter_nones_from_dict(query_parameters: Dict[str, Optional[Any]]) -> Dict[str, Any]:
    """
    This function takes a list of parameters as a dict, and returns a dict containing only non null parameters

    Examples:
        >>> filter_nones_from_dict({"key1": None, "key2": "some value"})
        {"key2": "some value"}

    Args:
        query_parameters (dict): query parameters in the form of a dict with `None` values

    Returns:
        dict: a dict with None values filtered

    """
    return {k: v for k, v in query_parameters.items() if v}


def process_list_parameter(parameter: Optional[List[str]]) -> Optional[str]:
    return convert_list_to_string_query_params(parameter) if parameter else None


def process_bool_parameter(parameter: Optional[bool]) -> Optional[str]:
    return str(parameter).lower() if parameter is not None else None


def process_date_parameter(parameter: Optional[date]) -> Optional[str]:
    return parameter.isoformat() if parameter else None


def process_date_parameter_no_colon(parameter: Optional[datetime]) -> Optional[str]:
    return parameter.strftime("%Y-%m-%dT%H%M%S") if parameter else None


def process_flow_snapshot_parameter(parameter: Optional[datetime]) -> Optional[str]:
    return parameter.strftime("%Y-%m-%d") if parameter else None


def process_enum_parameters(
    parameter: Optional[List[enum.Enum]], to_lower_case: bool = True
) -> Optional[str]:
    return (
        convert_list_to_string_query_params(
            [p.value.lower() if to_lower_case else p.value for p in parameter]
        )
        if parameter
        else None
    )


def process_enum_parameter(
    parameter: Optional[enum.Enum], to_lower_case: bool = True
) -> Optional[str]:
    return (
        (str(parameter.value.lower()) if to_lower_case else str(parameter.value))
        if parameter
        else None
    )


def convert_list_to_string_query_params(list_of_parameters: Iterable[str]) -> str:
    if type(list_of_parameters) in (list, tuple):
        return ",".join(list_of_parameters)
    else:
        # list_of_parameters is already string here
        # but let's cast it other the tests are failing
        return str(list_of_parameters)


def prepare_pandas_mapping(mapping: Dict[str, Any]) -> Dict[str, str]:
    """
    Will return the pandas mapping based on the kpler one returned by `columns` endpoints.
    """
    pandas_mapping: Dict[str, str] = {}

    for c, _type in mapping.items():
        pt: str = "object"
        if _type in ("integer", "long", "float", "double"):
            pt = "numeric"
        elif _type == "boolean":
            pt = "boolean"
        elif _type.startswith("date"):
            pt = "datetime"
        # else it's object (for strings)
        pandas_mapping[c] = pt
    return pandas_mapping


def bytes_to_pandas_data_frame(byte_contents: bytes, mapping: Dict[str, Any]) -> pd.DataFrame:
    """
    Will convert bytes content to a Pandas dataframe

    - If the mapping is given (not empty), then we just read the dataframe without type infering.
    We then apply the mapping coming from the get_columns endpoint.
    - If the mapping is not given, then we create the dataframe with type infering. But we try to
    set datetime types manually behind just in case.
    """
    if len(mapping) > 0:
        df = pd.read_csv(
            StringIO(byte_contents.decode("utf-8")),
            sep=";",
            dtype="object",
        )

        raw_mapping: Dict[str, str] = prepare_pandas_mapping(mapping)

        for col, _type in raw_mapping.items():
            if col not in df.columns:
                continue

            if _type == "numeric":
                # will return integer when possible, float otherwise
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass  # Keep original values if conversion fails
            elif _type.startswith("datetime"):
                try:
                    df[col] = pd.to_datetime(df[col])
                except (ValueError, TypeError):
                    pass  # Keep original values if conversion fails
            elif _type == "boolean":
                # for boolean, since KPLER API returns "true/false", this is evaluated as a non-null value,
                # hence always TRUE for a pandas boolean. So we need to tweak that a bit.
                df[col] = df[col].str.lower() == "true"

        # now maybe the dataframe contains columns that are not returned by the `columns` endpoint
        # (e.g. for dynamic columns returned when doing a split)
        # let's try to convert them to numeric values
        for col in [col for col in df.columns if col not in raw_mapping.keys()]:
            if pd.api.types.is_string_dtype(df[col]):
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass  # Keep original values if conversion fails

    else:
        df = pd.read_csv(
            StringIO(byte_contents.decode("utf-8")),
            sep=";",
            low_memory=False,
        )
        # let's convert the dates if possible
        # we have at least ETA or date in the column name
        cols_dates = [
            col
            for col in df.columns
            if not any([o.lower() in col.lower() for o in (["jsonupdates"])])
            and any([p.lower() in col.lower() for p in ("from", "until", "date", "eta")])
            and str(df[col].head(1).values).count("-")
            > 1  # Adding this to avoid converting i.e 2016-02 to 2016-02-01
        ]
        for col in cols_dates:
            if pd.api.types.is_string_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except (ValueError, TypeError):
                    pass  # Keep original values if conversion fails

    return df
