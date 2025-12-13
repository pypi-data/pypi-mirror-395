import unittest
import pandas as pd
from ppc.helpers.pandas_helper import PandasHelper

class TestPandasHelper(unittest.TestCase):

    def test_transform_col_in_tuple(self):
        # Setup: DataFrame with varied cases (multiple values, single, null, extra spaces)
        data = {
            'col1': ['A; B', 'C', '', 'D;  E ', None]
        }
        df = pd.DataFrame(data)

        result = PandasHelper.transform_col_in_tuple(df['col1'], ';')

        # Assertions
        self.assertEqual(result[0], ('A', 'B')) # Sorted and clean
        self.assertEqual(result[1], ('C',))     # Single item tuple
        self.assertEqual(result[2], ())         # Empty becomes empty tuple
        self.assertEqual(result[3], ('D', 'E')) # Removes extra spaces
        self.assertEqual(result[4], ())         # None becomes empty

if __name__ == '__main__':
    unittest.main()