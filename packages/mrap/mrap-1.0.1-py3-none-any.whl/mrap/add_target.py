import pandas as pd
from collections.abc import Mapping
from .utils import parse_code_list
from .utils import get_comparison_target_name


def add_comparison_target(dt, code_list, input_data):
    """
    Write a target component instance for group_comparison

    :param dt: a datatype loaded with the dtreg package
    :param code_list: a list with library and code line strings, "N/A" if not given
    :param input_data: pd.DataFrame, a dictionary, or a URL as a string
    :return: a target component instance
    """
    if isinstance(input_data, Mapping):
        target_name = get_comparison_target_name(input_data)
    elif isinstance(input_data, pd.DataFrame):
        target_name = parse_code_list(code_list)["target_name"]
    else:
        target_name = None
    target_variable = dt.component(label=target_name)
    return target_variable


def add_generic_target(dt, code_list, input_data):
    """
    Write a target component instance

    :param dt: a datatype loaded with the dtreg package
    :param code_list: a list with library and code line strings, "N/A" if not given
    :param input_data: pd.DataFrame, a dictionary, or a URL as a string
    :return: a target component instance
    """
    target_name = parse_code_list(code_list)["target_name"]
    target_variable = dt.component(label=target_name)
    return target_variable
