from unittest.mock import MagicMock, patch

from core.cache import Cache
from core.sheets_client import SheetsClient


def make_mock_service():
    service = MagicMock()
    service.spreadsheets.return_value.get.return_value.execute.return_value = {}
    return service


@patch("innosched.sheets_client.service_account.Credentials.from_service_account_file")
@patch("innosched.sheets_client.build")
def test_apply_merges_fills_all_cells(mock_build, mock_creds):
    mock_build.return_value = make_mock_service()
    mock_creds.return_value = MagicMock()

    client = SheetsClient("credentials.json", "spread", use_cache=False)
    values = [["X", ""], ["", "Y"]]
    merges = [
        {
            "startRowIndex": 0,
            "endRowIndex": 2,
            "startColumnIndex": 0,
            "endColumnIndex": 2,
        }
    ]

    merged = client.apply_merges(values, merges)

    assert merged == [["X", "X"], ["X", "X"]]


@patch("innosched.sheets_client.service_account.Credentials.from_service_account_file")
@patch("innosched.sheets_client.build")
def test_apply_merges_pads_missing_cells(mock_build, mock_creds):
    mock_build.return_value = make_mock_service()
    mock_creds.return_value = MagicMock()

    client = SheetsClient("credentials.json", "spread", use_cache=False)
    values = [["X"], []]
    merges = [
        {
            "startRowIndex": 0,
            "endRowIndex": 2,
            "startColumnIndex": 0,
            "endColumnIndex": 3,
        }
    ]

    merged = client.apply_merges(values, merges)

    assert merged == [
        ["X", "X", "X"],
        ["X", "X", "X"],
    ]


@patch("innosched.sheets_client.service_account.Credentials.from_service_account_file")
@patch("innosched.sheets_client.build")
def test_cache_used_when_remote_revision_unknown(mock_build, mock_creds, tmp_path):
    service = make_mock_service()
    mock_build.return_value = service
    mock_creds.return_value = MagicMock()

    with patch("innosched.sheets_client.Cache", lambda: Cache(db_path=tmp_path / "cache.db")):
        client = SheetsClient("cred.json", "spread", use_cache=True)
        key = client._cache_key("Sheet1", "A1:Z500")
        client.cache.set(key, [["cached"]], revision="rev1")

        service.spreadsheets().get.return_value.execute.return_value = {}

        data = client.get_sheet_data("Sheet1")

        assert data == [["cached"]]
        assert service.spreadsheets().get.call_count == 0


@patch("innosched.sheets_client.service_account.Credentials.from_service_account_file")
@patch("innosched.sheets_client.build")
def test_get_sheet_data_peeks_revision_without_extra_calls(mock_build, mock_creds, tmp_path):
    service = make_mock_service()
    service.spreadsheets().get.return_value.execute.return_value = {
        "sheets": [],
        "revisionId": "rev123",
    }
    mock_build.return_value = service
    mock_creds.return_value = MagicMock()

    with patch("innosched.sheets_client.Cache", lambda: Cache(db_path=tmp_path / "cache.db")):
        client = SheetsClient("cred.json", "spread", use_cache=True)
        key = client._cache_key("Sheet1", "A1:Z500")
        client.cache.set(key, [["cached"]], revision="rev123")

        data = client.get_sheet_data("Sheet1")

        assert data == [["cached"]]
        assert service.spreadsheets().get.call_count == 0


@patch("innosched.sheets_client.service_account.Credentials.from_service_account_file")
@patch("innosched.sheets_client.build")
def test_merges_applied_and_cached(mock_build, mock_creds, tmp_path):
    service = make_mock_service()
    service.spreadsheets().get.return_value.execute.return_value = {
        "sheets": [
            {
                "data": [
                    {
                        "rowData": [
                            {"values": [{"formattedValue": "X"}, {"formattedValue": ""}]},
                            {"values": [{"formattedValue": ""}, {"formattedValue": ""}]},
                        ]
                    }
                ],
                "merges": [
                    {
                        "startRowIndex": 0,
                        "endRowIndex": 2,
                        "startColumnIndex": 0,
                        "endColumnIndex": 2,
                    }
                ],
            }
        ],
        "revisionId": "r1",
    }
    mock_build.return_value = service
    mock_creds.return_value = MagicMock()

    with patch("innosched.sheets_client.Cache", lambda: Cache(db_path=tmp_path / "cache.db")):
        client = SheetsClient("cred.json", "spread", use_cache=True)

        data = client.get_sheet_data("Sheet1", "A1:B2")

        assert data == [["X", "X"], ["X", "X"]]
        assert service.spreadsheets().get.call_count == 1

        cached_value, cached_revision = client.cache.get_entry(client._cache_key("Sheet1", "A1:B2"))
        assert cached_value == [["X", "X"], ["X", "X"]]
        assert cached_revision == "r1"
