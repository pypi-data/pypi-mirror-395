import unittest
from mrap.scipy_f_oneway import scipy_f_oneway
from helpers.iris import iris


class TestScipyFOneway(unittest.TestCase):
    def test_scipy_f_oneway_anova(self):
        setosa = iris[iris['Species'] == 'setosa']['Petal.Length']
        versicolor = iris[iris['Species'] == 'versicolor']['Petal.Length']
        virginica = iris[iris['Species'] == 'virginica']['Petal.Length']
        result = scipy_f_oneway(setosa, versicolor, virginica)
        target_label = result['dtreg_object'].targets.label
        self.assertEqual(target_label, 'Petal.Length')


if __name__ == '__main__':
    unittest.main()
