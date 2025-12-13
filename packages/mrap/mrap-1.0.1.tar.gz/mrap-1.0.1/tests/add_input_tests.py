import unittest
from helpers.iris import iris
from mrap.add_input import add_input
from dtreg.load_datatype import load_datatype


class TestAddInput(unittest.TestCase):

    def test_input_inst_name(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        input_inst = add_input(dt, "XXX")
        self.assertEqual(dt.data_item.dt_name, input_inst.dt_name)

    def test_input_string(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        input_inst = add_input(dt, "XXX")
        self.assertEqual(input_inst.source_url, "XXX")

    def test_input_dataframe_dimensions(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        input_inst = add_input(dt, iris)
        self.assertEqual(input_inst.has_characteristic.number_of_rows, iris.shape[0])

    def test_input_series_dimensions(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        setosa = iris[iris['Species'] == 'setosa']['Petal.Length']
        virginica = iris[iris['Species'] == 'virginica']['Petal.Length']
        my_dict = {"setosa": setosa, "virginica": virginica}
        input_inst = add_input(dt, my_dict)
        self.assertEqual(input_inst[0].has_characteristic.number_of_rows, setosa.size)

    def test_input_wrong_argument(self):
        dt = load_datatype("https://doi.org/21.T11969/b9335ce2c99ed87735a6")
        self.assertRaises(TypeError,
                          "Argument input_data should be a pd.DataFrame, a dictionary, or a string",
                          add_input, dt, 7)


if __name__ == '__main__':
    unittest.main()
