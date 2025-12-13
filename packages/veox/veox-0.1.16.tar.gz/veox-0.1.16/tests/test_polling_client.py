import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from veox import Veox
from veox.client import APIClient

class TestPollingClient(unittest.TestCase):
    def setUp(self):
        self.mock_api = MagicMock(spec=APIClient)
        self.client = Veox(api_url="http://test", verbose=True)
        self.client._api = self.mock_api
        
    def test_fit_forces_polling(self):
        """Test that use_polling=True skips streaming."""
        # Setup mocks
        self.mock_api.submit_job.return_value = {"job_id": "job_123"}
        self.mock_api.get_job_progress.side_effect = [
            {"status": "running", "job_progress_pct": 50, "is_terminal": False},
            {"status": "completed", "job_progress_pct": 100, "is_terminal": True},
        ]
        
        # Execute
        self.client.fit(dataset="test", use_polling=True, poll_interval=0.1)
        
        # Verify stream was NOT called
        self.mock_api.stream_job_events.assert_not_called()
        # Verify polling loop called get_job_progress
        self.assertGreater(self.mock_api.get_job_progress.call_count, 1)
        
    def test_hybrid_fallback(self):
        """Test that stream failure triggers polling."""
        self.mock_api.submit_job.return_value = {"job_id": "job_123"}
        self.mock_api.stream_job_events.side_effect = Exception("Stream died")
        self.mock_api.get_job_progress.side_effect = [
             {"status": "running", "job_progress_pct": 50, "is_terminal": False},
             {"status": "completed", "job_progress_pct": 100, "is_terminal": True},
        ]
        
        self.client.fit(dataset="test", use_polling=False, poll_interval=0.1)
        
        # Verify stream WAS called
        self.mock_api.stream_job_events.assert_called_once()
        # Verify fallback to polling
        self.assertGreater(self.mock_api.get_job_progress.call_count, 1)

if __name__ == "__main__":
    unittest.main()
