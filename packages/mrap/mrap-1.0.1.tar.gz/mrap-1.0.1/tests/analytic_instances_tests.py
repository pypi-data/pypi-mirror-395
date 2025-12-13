import unittest
import pandas as pd
from mrap.analytic_instances import data_analysis
from mrap.analytic_instances import descriptive_statistics
from mrap.analytic_instances import algorithm_evaluation
from mrap.analytic_instances import multilevel_analysis
from mrap.analytic_instances import correlation_analysis
from mrap.analytic_instances import group_comparison
from mrap.analytic_instances import regression_analysis
from mrap.analytic_instances import class_prediction
from mrap.analytic_instances import class_discovery
from mrap.analytic_instances import factor_analysis


class TestAnalyticInstances(unittest.TestCase):
    def test_data_analysis(self):
        code_list = "N/A"
        input_data = pd.DataFrame({'A': [1], 'B': [2]})
        test_results = pd.DataFrame({'C': [3], 'D': [4]})
        inst_gc = group_comparison(code_list, input_data, test_results)
        inst_da = data_analysis(inst_gc)
        self.assertEqual(inst_da.dt_id, "feeb33ad3e4440682a4d")

    def test_descriptive_statistics(self):
        code_list = "N/A"
        input_data = pd.DataFrame({'A': [1], 'B': [2]})
        test_results = pd.DataFrame({'C': [3], 'D': [4]})
        inst = descriptive_statistics(code_list, input_data, test_results)
        self.assertEqual(inst.dt_id, "5b66cb584b974b186f37")

    def test_algorithm_evaluation(self):
        code_list = "N/A"
        input_data = pd.DataFrame({'A': [1], 'B': [2]})
        dictionary_results = {'C': [3], 'D': [4]}
        inst = algorithm_evaluation(code_list, input_data, dictionary_results)
        self.assertEqual(inst.dt_id, "5e782e67e70d0b2a022a")

    def test_multilevel_analysis(self):
        code_list = ["statsmodels",
                     "smf.mixedlm('Weight ~ Time', data, groups=data['Pig'])"]
        input_data = pd.DataFrame({'A': [1], 'B': [2]})
        test_results = pd.DataFrame({'C': [3], 'D': [4]})
        inst = multilevel_analysis(code_list, input_data, test_results)
        self.assertEqual(inst.dt_id, "c6b413ba96ba477b5dca")

    def test_correlation_analysis(self):
        code_list = "N/A"
        input_data = pd.DataFrame({'A': [1], 'B': [2]})
        test_results = pd.DataFrame({'C': [3], 'D': [4]})
        inst = correlation_analysis(code_list, input_data, test_results)
        self.assertEqual(inst.dt_id, "3f64a93eef69d721518f")

    def test_group_comparison(self):
        code_list = "N/A"
        input_data = pd.DataFrame({'A': [1], 'B': [2]})
        test_results = pd.DataFrame({'C': [3], 'D': [4]})
        inst = group_comparison(code_list, input_data, test_results)
        self.assertEqual(inst.dt_id, "b9335ce2c99ed87735a6")

    def test_regression_analysis(self):
        code_list = "N/A"
        input_data = pd.DataFrame({'A': [1], 'B': [2]})
        test_results = pd.DataFrame({'C': [3], 'D': [4]})
        inst = regression_analysis(code_list, input_data, test_results)
        self.assertEqual(inst.dt_id, "286991b26f02d58ee490")

    def test_class_prediction(self):
        code_list = "N/A"
        input_data = pd.DataFrame({'A': [1], 'B': [2]})
        test_results = pd.DataFrame({'C': [3], 'D': [4]})
        inst = class_prediction(code_list, input_data, test_results)
        self.assertEqual(inst.dt_id, "6e3e29ce3ba5a0b9abfe")

    def test_class_discovery(self):
        code_list = "N/A"
        input_data = pd.DataFrame({'A': [1], 'B': [2]})
        test_results = pd.DataFrame({'C': [3], 'D': [4]})
        inst = class_discovery(code_list, input_data, test_results)
        self.assertEqual(inst.dt_id, "c6e19df3b52ab8d855a9")

    def test_factor_analysis(self):
        code_list = "N/A"
        input_data = pd.DataFrame({'A': [1], 'B': [2]})
        test_results = pd.DataFrame({'C': [3], 'D': [4]})
        inst = factor_analysis(code_list, input_data, test_results)
        self.assertEqual(inst.dt_id, "437807f8d1a81b5138a3")


if __name__ == '__main__':
    unittest.main()
