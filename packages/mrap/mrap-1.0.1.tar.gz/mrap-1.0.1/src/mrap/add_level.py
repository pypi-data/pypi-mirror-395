from .utils import parse_code_list


def add_level(dt, code_list):
    """
    Write a level component instance

    :param dt: a datatype loaded with the dtreg package
    :param code_list: a list with library and code line strings, "N/A" if not given
    :return: a level component instance
    """
    level_name = parse_code_list(code_list)["level_name"]
    level_variable = dt.component(label=level_name)
    return level_variable
