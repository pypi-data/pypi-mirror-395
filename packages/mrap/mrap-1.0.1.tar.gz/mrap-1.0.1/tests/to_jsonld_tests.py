import unittest
from dtreg.load_datatype import load_datatype
from mrap.to_jsonld import to_jsonld


class TestToJsonld(unittest.TestCase):

    def test_jsonld(self):
        dt = load_datatype("https://doi.org/21.T11969/aff130c76e68ead3862e")
        url = dt.url()
        instance = dt.data_item(has_expression=url)
        result = to_jsonld(instance)
        expected = ('{\n'
                    '  "@id": "_:n1",\n'
                    '  "@type": "doi:aff130c76e68ead3862e",\n'
                    '  "doi:aff130c76e68ead3862e#has_expression": {\n'
                    '    "@id": "_:n2",\n'
                    '    "@type": "doi:e0efc41346cda4ba84ca"\n'
                    '  },\n'
                    '  "@context": {\n'
                    '    "doi": "https://doi.org/21.T11969/",\n'
                    '    "columns": "https://doi.org/21.T11969/0424f6e7026fa4bc2c4a#columns",\n'
                    '    "col_number": "https://doi.org/21.T11969/65ba00e95e60fb8971e6#number",\n'
                    '    "col_titles": "https://doi.org/21.T11969/65ba00e95e60fb8971e6#titles",\n'
                    '    "rows": "https://doi.org/21.T11969/0424f6e7026fa4bc2c4a#rows",\n'
                    '    "row_number": "https://doi.org/21.T11969/9bf7a8e8909bfd491b38#number",\n'
                    '    "row_titles": "https://doi.org/21.T11969/9bf7a8e8909bfd491b38#titles",\n'
                    '    "cells": "https://doi.org/21.T11969/9bf7a8e8909bfd491b38#cells",\n'
                    '    "column": "https://doi.org/21.T11969/4607bc7c42ac8db29bfc#column",\n'
                    '    "value": "https://doi.org/21.T11969/4607bc7c42ac8db29bfc#value",\n'
                    '    "tab_label": "https://doi.org/21.T11969/0424f6e7026fa4bc2c4a#label"\n'
                    '  }\n'
                    '}')
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
