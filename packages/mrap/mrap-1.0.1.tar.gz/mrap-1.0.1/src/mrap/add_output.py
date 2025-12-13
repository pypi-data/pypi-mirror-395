import pandas as pd
from dtreg.load_datatype import load_datatype
from .utils import standardise_keys


def add_generic_output(dt, schema_name, test_results):
    """
    Write a generic output instance to be used by other instances

    :param dt: a datatype loaded with the dtreg package
    :param test_results: a pd.DataFrame or a list of data frames
    :return: a generic output instance
    """
    output = dt.data_item(label=str(schema_name) + " results",
                          source_table=test_results)
    return output


def add_evaluation_output(dt, dictionary_results):
    """
    Write an algorithm_evaluation output instance to be used by other instances

    :param dt: a datatype loaded with the dtreg package
    :param dictionary_results: a dictionary of metrics and values
    :return: an algorithm_evaluation output instance
    """
    dt = load_datatype("https://doi.org/21.T11969/5e782e67e70d0b2a022a")
    new_dictionary = standardise_keys(dictionary_results)
    df_results = pd.DataFrame([new_dictionary])
    df_named = df_results.rename(index={0: 'value'})
    output = dt.data_item(label="algorithm evaluation results",
                          source_table=df_named)
    return output
