"""This module provides various utilities functions."""

from typing import List, Literal, Any
from datetime import date
from pydoc import locate
from operator import itemgetter


@staticmethod
def split_str_to_list(
    values: str,
    split_by: str = ",",
    dtype: Literal["int", "str", "float", "dict", "list"] = "str",
) -> List[Any]:
    """
    Splits a string into a list of values of the specified data type.

    Args:
        values (str): The string to be split.\n
        split_by (str, optional):
        The character to split the string by. Defaults to ",".\n
        dtype (Literal["int", "str", "float", "dict", "list"], optional):
        The data type of the values. Defaults to "str".

    Returns:
        List[dtype]: A list of values converted to the specified data type.
    """
    data_type = locate(dtype)
    if isinstance(values, str):
        return [data_type(element) for element in values.split(split_by)]
    else:
        return values


@staticmethod
def filter_dict_with_falsy_values(dictionary: dict) -> dict:
    """
    Filters a dictionary by removing key-value pairs where the value is falsy.

    Args:
        dictionary (dict): The dictionary to filter.

    Returns:
        dict: The filtered dictionary.
    """
    return dict(filter(itemgetter(1), dictionary.items()))


@staticmethod
def convert_dict_dates_to_isoformat(dictionary: dict) -> dict:
    """
    Converts date values in a dictionary to ISO 8601 format.
    Nested dictionaries and lists are supported.

    Args:
        dictionary (dict): The dictionary to convert.

    Returns:
        dict: The dictionary with date values converted to ISO 8601 format.
    """

    def convert_value(value):
        if isinstance(value, date):
            return value.isoformat()
        elif isinstance(value, dict):
            return convert_dict_dates_to_isoformat(value)
        elif isinstance(value, list):
            return [convert_value(item) for item in value]
        else:
            return value

    return {key: convert_value(value) for key, value in dictionary.items()}
