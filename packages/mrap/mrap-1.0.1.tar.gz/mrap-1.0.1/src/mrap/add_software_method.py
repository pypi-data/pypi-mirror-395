import sys
from .utils import get_library_info
from .utils import parse_code_list


def add_software_method(dt, code_list):
    """
    Write a software_method instance to be used by other instances

    :param dt: a datatype loaded with the dtreg package
    :param code_list: a list with library and code line strings, "N/A" if not given
    :return: a software_method instance
    """
    vers = sys.version_info
    version_py = str(vers[0]) + "." + str(vers[1]) + "." + str(vers[2])
    software = dt.software(label="Python",
                           version_info=version_py,
                           has_support_url="https://www.python.org")
    if code_list == "N/A":
        software_method = dt.software_method(part_of=software)
    elif isinstance(code_list, list):
        lib = code_list[0]
        fun = parse_code_list(code_list)["fun"]
        library_info = get_library_info(lib)
        version_lib = library_info["version_lib"]
        url_lib = library_info["url_lib"]
        software_library = dt.software_library(label=lib,
                                               version_info=version_lib,
                                               has_support_url=url_lib,
                                               part_of=software)
        software_method = dt.software_method(label=fun,
                                             part_of=software_library,
                                             is_implemented_by=code_list[1])
    else:
        raise TypeError("Argument code_list is of a wrong type, see Readme")
    return software_method
