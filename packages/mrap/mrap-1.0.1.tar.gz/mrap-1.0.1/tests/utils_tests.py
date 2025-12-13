import unittest
from helpers.iris import iris
from mrap.utils import parse_code_list
from mrap.utils import get_comparison_target_name
from mrap.utils import get_library_info
from mrap.utils import standardise_keys


class TestUtils(unittest.TestCase):
    def test_parse_code_list_min(self):
        code_list = ["statistics", "mean(data)"]
        result = parse_code_list(code_list)
        self.assertEqual(result["fun"], 'mean')

    def test_parse_code_list_full(self):
        code_list = ["statsmodels",
                     "smf.mixedlm('Weight ~ Time', data, groups=data['Pig'])"]
        result = parse_code_list(code_list)
        expected = {"fun": "smf.mixedlm",
                    "target_name": "Weight",
                    "level_name": "Pig"}
        self.assertEqual(result, expected)

    def test_get_target_name_extractable(self):
        setosa = iris[iris['Species'] == 'setosa']['Petal.Length']
        versicolor = iris[iris['Species'] == 'versicolor']['Petal.Length']
        input_dict = {"setosa": setosa, "versicolor": versicolor}
        target_name = get_comparison_target_name(input_dict)
        self.assertEqual(target_name, 'Petal.Length')

    def test_get_target_name_unclear(self):
        setosa = iris[iris['Species'] == 'setosa']['Petal.Length']
        versicolor = iris[iris['Species'] == 'versicolor']['Sepal.Length']
        input_dict = {"setosa": setosa, "versicolor": versicolor}
        target_name = get_comparison_target_name(input_dict)
        self.assertEqual(target_name, None)

    def test_get_library_info_none(self):
        lib_info = get_library_info("nonexistent_name")
        self.assertEqual(lib_info["version_lib"], None)

    def test_get_library_info_url(self):
        lib_info = get_library_info("pandas")
        self.assertEqual(lib_info["url_lib"], 'https://pandas.pydata.org/docs/')

    def test_get_library_info_pypi(self):
        lib_info = get_library_info("dtreg")
        self.assertEqual(lib_info["url_lib"], 'https://pypi.org/project/dtreg')

    def test_standardise_keys(self):
        old_dict = {"f_1": 0.43,
                    "auc": 0.65,
                    "Recall": 0.32}
        new_dict = standardise_keys(old_dict)
        expected = {"F1": 0.43,
                    "AUC": 0.65,
                    "recall": 0.32}
        self.assertEqual(new_dict, expected)


if __name__ == '__main__':
    unittest.main()
