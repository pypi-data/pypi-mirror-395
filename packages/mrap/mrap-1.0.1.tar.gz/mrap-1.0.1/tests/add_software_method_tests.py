import unittest
from mrap.add_software_method import add_software_method
from dtreg.load_datatype import load_datatype


class TestSoftMethod(unittest.TestCase):

    def test_software_method_inst_name(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        sw_method_inst = add_software_method(dt, ["scipy", "f_oneway"])
        self.assertEqual(dt.software_method.dt_name, sw_method_inst.dt_name)

    def test_software_method_label(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        sw_method_inst = add_software_method(dt, ["scipy", "f_oneway"])
        self.assertEqual(sw_method_inst.label, "f_oneway")

    def test_software_method_lib_label(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        sw_method_inst = add_software_method(dt, ["scipy", "f_oneway"])
        self.assertEqual(sw_method_inst.part_of.label, "scipy")

    def test_software_method_software_label(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        sw_method_inst = add_software_method(dt, "N/A")
        self.assertEqual(sw_method_inst.part_of.label, "Python")

    def test_software_method_wrong_argument(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        self.assertRaises(TypeError, "Argument code_list is of a wrong type, see Readme",
                          add_software_method, dt, 7)


if __name__ == '__main__':
    unittest.main()
