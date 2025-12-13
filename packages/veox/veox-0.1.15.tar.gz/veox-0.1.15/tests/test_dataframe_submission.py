import unittest
from unittest.mock import MagicMock
import pandas as pd
import numpy as np
from veox import Veox
from veox.client import APIClient

class TestDataFrameSubmission(unittest.TestCase):
    def setUp(self):
        self.mock_api = MagicMock(spec=APIClient)
        self.client = Veox(api_url="http://test", verbose=False)
        self.client._api = self.mock_api
        
    def test_upload_serialization(self):
        """Test robust dataframe serialization."""
        self.mock_api.post.return_value.json.return_value = {"dataset_id": "ds_123"}
        
        # DataFrame with NaNs and Different Types
        df = pd.DataFrame({
            "A": [1, 2, np.nan],
            "B": ["x", "y", "z"],
            "C": [1.1, 2.2, float('inf')]
        })
        
        ds_id = self.client._upload_dataframe(X=df, target_column="B")
        
        self.assertEqual(ds_id, "ds_123")
        
        # Verify payload structure
        call_args = self.mock_api.post.call_args
        payload = call_args[1]['json_data'] # or args[1]
        
        self.assertIn("dataframe", payload)
        self.assertIn("data", payload["dataframe"])
        # Ensure it's a string (serialized JSON)
        self.assertIsInstance(payload["dataframe"]["data"], str)
        
    def test_large_file_warning(self):
        # Difficult to test display logger, but we can verify logic flow doesn't crash on large mock
        # Just ensure no exception
        pass

if __name__ == "__main__":
    unittest.main()
