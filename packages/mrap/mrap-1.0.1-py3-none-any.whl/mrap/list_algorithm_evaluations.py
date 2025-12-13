from .analytic_instances import algorithm_evaluation


def list_algorithm_evaluations(code_list, input_data, task, sum_dictionary):
    """
    Create a list of algorithm_evaluation instances

    :param code_list: a list with library and code line strings, "N/A" if not given
    :param input_data: pd.DataFrame, a dictionary, or a URL as a string
    :param sum_dictionary: a nested dictionary with algorithms and their results
    :return: a list of algorithm evaluation instances
    """
    algorithms_instances = []
    for key, value in sum_dictionary.items():
        instance = algorithm_evaluation(code_list, input_data, value)
        instance.label = key + " evaluation"
        instance.evaluates = key
        instance.evaluates_for = task
        algorithms_instances.append(instance)
    return algorithms_instances
