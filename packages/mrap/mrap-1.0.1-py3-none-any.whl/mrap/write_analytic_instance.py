from .add_input import add_input
from .add_software_method import add_software_method


def write_analytic_instance(dt, schema_name,
                            code_list, input_data):
    """
    Write a generic part of analytic instances

    :param dt: datatype loaded with the dtreg package
    :param schema_name: an analytic schema name as a string
    :param code_list: a list with library and code line strings, "N/A" if not given
    :param input_data: pd.DataFrame, a dictionary, or a URL as a string
    :return: a generic instance to be used by any analytic instance
    """
    schema = getattr(dt, schema_name)
    software_method = add_software_method(dt, code_list)
    inputs = add_input(dt, input_data)
    instance = schema(
        label=schema_name,
        executes=software_method,
        has_input=inputs
    )
    return instance
