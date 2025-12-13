import pandas as pd
from collections.abc import Mapping
from varname import argname


def add_input(dt, input_data):
    """
    Write an input instance to be used by other instances

    :param dt: a datatype loaded with the dtreg package
    :param input_data: pd.DataFrame, a dictionary, or a URL as a string
    :return: an input instance
    """
    if isinstance(input_data, Mapping):
        inputs = []
        for key in input_data:
            inp_inst = dt.data_item(
                label=key,
                has_characteristic=dt.matrix_size(
                    number_of_rows=len(input_data[key]),
                    number_of_columns=1
                )
            )
            inputs.append(inp_inst)
    elif isinstance(input_data, pd.DataFrame):
        nrows, ncols = input_data.shape
        input_label = argname('input_data')
        inputs = dt.data_item(
            label=input_label,
            has_characteristic=dt.matrix_size(
                number_of_rows=nrows,
                number_of_columns=ncols
            )
        )
    elif isinstance(input_data, str):
        inputs = dt.data_item(source_url=input_data)
    else:
        raise TypeError("Argument input_data should be a pd.DataFrame, a dictionary, or a string")
    return inputs
