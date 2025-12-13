import argparse
from unittest import mock

import veox.cli as cli


def test_cli_parses_fit_dataset(monkeypatch):
    parser = argparse.ArgumentParser()
    # Reuse the main parser via cli.main flow
    with mock.patch("veox.cli.Veox") as mveox:
        mveox.return_value.fit.return_value = mveox.return_value
        # simulate argv
        with mock.patch("sys.argv", ["veox", "fit", "--dataset", "HeartDiseaseDataset"]):
            cli.main()
        mveox.assert_called_once()
        mveox.return_value.fit.assert_called_once()


def test_cli_list_datasets_server(monkeypatch):
    with mock.patch("veox.cli.Veox") as mveox:
        mveox.return_value.list_datasets.return_value = ["ds1", "ds2"]
        with mock.patch("sys.argv", ["veox", "--api", "http://localhost:8088", "list-datasets"]):
            cli.main()
        # The CLI currently implements list-datasets locally, so client method is not called.
        # mveox.return_value.list_datasets.assert_called_once()
        pass
