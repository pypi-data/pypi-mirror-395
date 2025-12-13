import unittest
import pandas as pd
from mrap.list_algorithm_evaluations import list_algorithm_evaluations


class TestListEvaluations(unittest.TestCase):

    def test_list_evaluations(self):
        code_list = "N/A"
        input_data = pd.DataFrame({'A': [1], 'B': [2]})
        sum_dictionary = {"ABC": {"F1": 0.46, "recall": 0.64},
                          "KLM": {"F1": 0.55, "recall": 0.38},
                          "XYZ": {"F1": 0.87, "recall": 0.78}}
        inst = list_algorithm_evaluations(code_list,
                                          input_data,
                                          "Classification",
                                          sum_dictionary)
        self.assertEqual(inst[0].evaluates_for, 'Classification')


if __name__ == '__main__':
    unittest.main()
