import unittest
from mrap.add_level import add_level
from dtreg.load_datatype import load_datatype


class TestAddLevel(unittest.TestCase):

    def test_level_inst_extractable(self):
        dt = load_datatype("https://doi.org/21.T11969/c6b413ba96ba477b5dca")
        code_list = ["statsmodels",
                     "smf.mixedlm('Weight ~ Time', data, groups=data['Pig'])"]
        level_inst = add_level(dt, code_list)
        self.assertEqual(level_inst.label, 'Pig')

    def test_level_inst_no_name(self):
        dt = load_datatype("https://doi.org/21.T11969/c6b413ba96ba477b5dca")
        level_inst = add_level(dt, "N/A")
        self.assertEqual(level_inst.label, None)


if __name__ == '__main__':
    unittest.main()
