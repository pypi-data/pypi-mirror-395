import unittest
from helpers.iris import iris
from mrap.add_target import add_comparison_target, add_generic_target
from dtreg.load_datatype import load_datatype


class TestAddTarget(unittest.TestCase):

    def test_generic_target_inst_name(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        target_inst = add_generic_target(dt, "N/A", iris)
        self.assertEqual(dt.component.dt_name, target_inst.dt_name)

    def test_generic_target_extractable(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        code_list = ["statsmodels",
                     "smf.mixedlm('Weight ~ Time', data, groups=data['Pig'])"]
        target_inst = add_generic_target(dt, code_list, "data_url")
        self.assertEqual(target_inst.label, 'Weight')

    def test_generic_target_none(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        target_inst = add_generic_target(dt, "N/A", "data_url")
        self.assertEqual(target_inst.label, None)

    def test_comparison_target_inst_name(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        target_inst = add_comparison_target(dt, "N/A", iris)
        self.assertEqual(dt.component.dt_name, target_inst.dt_name)

    def test_add_comparison_target_extractable(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        setosa = iris[iris['Species'] == 'setosa']['Petal.Length']
        versicolor = iris[iris['Species'] == 'versicolor']['Petal.Length']
        input_dict = {"setosa": setosa, "versicolor": versicolor}
        target_inst = add_comparison_target(dt, "N/A", input_dict)
        self.assertEqual(target_inst.label, 'Petal.Length')

    def test_add_comparison_target_none(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        target_inst = add_comparison_target(dt, "N/A", "data_url")
        self.assertEqual(target_inst.label, None)


if __name__ == '__main__':
    unittest.main()
