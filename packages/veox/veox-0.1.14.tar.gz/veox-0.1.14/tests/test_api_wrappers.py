from unittest import mock
from veox import Veox


def test_status_progress_report_calls_api():
    client = Veox(api_url="http://x")
    client._api = mock.MagicMock()
    client.last_job_id = "job123"

    client.status()
    client.get_progress()
    client.get_report()

    client._api.get_job_status.assert_called_once_with("job123")
    client._api.get_job_progress.assert_called_once_with("job123")
    client._api.get_job_report.assert_called_once_with("job123")


def test_control_calls_api():
    client = Veox(api_url="http://x")
    client._api = mock.MagicMock()
    client.last_job_id = "job123"

    client.pause()
    client.resume()
    client.cancel()

    client._api.pause_job.assert_called_once_with("job123")
    client._api.resume_job.assert_called_once_with("job123")
    client._api.cancel_job.assert_called_once_with("job123")


def test_dataset_info_and_list():
    client = Veox(api_url="http://x")
    client._api = mock.MagicMock()

    client.list_datasets(task="binary")
    client.get_dataset_info("HeartDiseaseDataset")

    client._api.list_datasets.assert_called_once_with(task="binary")
    client._api.get_dataset_info.assert_called_once_with("HeartDiseaseDataset")


def test_pull_code_prefers_run_id_calls_get():
    client = Veox(api_url="http://x")
    client._api = mock.MagicMock()
    response = mock.MagicMock()
    response.text = "code"
    client._api.get.return_value = response

    code = client.pull_code(run_id="run123")

    client._api.get.assert_called_once_with("/v1/runs/run123/pipeline/source")
    assert code == "code"
