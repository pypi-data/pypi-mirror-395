import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from veox import Veox

def make_response(payload):
    """Helper to mimic requests.Response.json() for unit tests."""
    return MagicMock(json=MagicMock(return_value=payload))

@pytest.fixture
def mock_api():
    with patch('veox.client.APIClient') as mock:
        yield mock

@pytest.fixture
def mock_display():
    with patch('veox.client.DisplayManager') as mock:
        yield mock

def test_instantiation():
    client = Veox(api_url="http://test:8000")
    assert client._api_config.url == "http://test:8000"

def test_upload_dataframe_list():
    client = Veox()
    # Mock the API post response
    client._api.post = MagicMock(return_value=make_response({"dataset_id": "ds_123"}))
    
    data = [[1, 2], [3, 4]]
    ds_id = client._upload_dataframe(X=data, target_column=1) # DataFrame col names are 0, 1
    
    assert ds_id == "ds_123"
    client._api.post.assert_called_once()
    args, kwargs = client._api.post.call_args
    payload = kwargs.get("json_data") or kwargs.get("json")
    assert payload['target_column'] == 1
    assert "dataframe" in payload

def test_fit_full_flow():
    client = Veox()
    
    # Mock responses
    client._api.post = MagicMock(return_value=make_response({"dataset_id": "ds_123"})) # upload
    client._api.submit_job = MagicMock(return_value={"job_id": "job_456"}) # submit
    client._api.stream_job_events = MagicMock(return_value=([], {})) # stream
    client._report_generator.generate_final_report = MagicMock(return_value="Report Content")
    
    # Run fit
    client.fit(
        X=[[1, 0], [0, 1]], 
        y=[0, 1], 
        task="binary", 
        show_pipeline=False
    )
    
    # Verify sequence
    client._api.post.assert_called() # upload called
    client._api.submit_job.assert_called()
    submitted = client._api.submit_job.call_args[0][0]
    assert submitted['dataset_id'] == "ds_123"
    assert submitted['task'] == "binary"
    assert submitted['population'] == 2 or submitted['population'] is not None
    client._api.stream_job_events.assert_called()
    assert client._api.stream_job_events.call_args[0][0] == "job_456"

def test_fit_with_existing_dataset():
    client = Veox()
    client._api.submit_job = MagicMock(return_value={"job_id": "job_999"})
    client._api.stream_job_events = MagicMock(return_value=([], {}))
    client._report_generator.generate_final_report = MagicMock(return_value="Report")
    
    client.fit(dataset="existing_ds", show_pipeline=False)
    
    # Upload should NOT be called
    client._api.post = MagicMock()
    client._api.post.assert_not_called()
    
    client._api.submit_job.assert_called()
    submitted = client._api.submit_job.call_args[0][0]
    assert submitted['dataset_id'] == "existing_ds"
