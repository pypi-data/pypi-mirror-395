import unittest
import pandas as pd
from mrap.add_output import add_evaluation_output
from mrap.add_output import add_generic_output
from dtreg.load_datatype import load_datatype


class TestAddOutput(unittest.TestCase):

    def test_generic_output_inst_name(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        my_df = pd.DataFrame({'A': [1], 'B': [2]})
        generic_output_inst = add_generic_output(dt, "group_comparison", my_df)
        self.assertEqual(dt.data_item.dt_name, generic_output_inst.dt_name)

    def test_evaluation_output_inst_name(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        my_dict = {'F1': 0.75, 'recall': 0.77}
        evaluation_output_inst = add_evaluation_output(dt, my_dict)
        self.assertEqual(dt.data_item.dt_name, evaluation_output_inst.dt_name)

    def test_evaluation_output_dict(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        my_dict = {'F1': 0.75, 'recall': 0.77}
        evaluation_output_inst = add_evaluation_output(dt, my_dict)
        df = pd.DataFrame([my_dict]).rename(index={0: 'value'})
        self.assertEqual(evaluation_output_inst.source_table.F1.value, df.F1.value)


if __name__ == '__main__':
    unittest.main()
