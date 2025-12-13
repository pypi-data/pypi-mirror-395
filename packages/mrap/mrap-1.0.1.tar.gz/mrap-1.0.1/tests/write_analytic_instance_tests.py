import unittest
from mrap.write_analytic_instance import write_analytic_instance
from dtreg.load_datatype import load_datatype


class TestWriteInstance(unittest.TestCase):

    def test_write_inst_label(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        inst = write_analytic_instance(dt,
                                       "group_comparison",
                                       "N/A",
                                       "XXX")
        self.assertEqual(inst.label, "group_comparison")


if __name__ == '__main__':
    unittest.main()
