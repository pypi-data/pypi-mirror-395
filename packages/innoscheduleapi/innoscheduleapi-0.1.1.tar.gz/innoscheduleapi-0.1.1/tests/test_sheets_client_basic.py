from unittest.mock import MagicMock, patch

from core.sheets_client import SheetsClient


def fake_sheet_response():
    return {
        "sheets": [{
            "data": [{
                "rowData": [
                    {"values": [{"formattedValue": "A"}, {"formattedValue": "B"}]},
                    {"values": [{"formattedValue": "C"}, {"formattedValue": "D"}]},
                ]
            }],
            "merges": []
        }]
    }


@patch("innosched.sheets_client.build")
def test_sheet_parsing_basic(mock_build):
    service = MagicMock()
    service.spreadsheets().get().execute.return_value = fake_sheet_response()
    service.spreadsheets().get().execute.return_value["revisionId"] = "123"

    mock_build.return_value = service

    client = SheetsClient("credentials.json", "spread_id", use_cache=False)

    data = client.get_sheet_data("BS1", "A1:B2")

    assert data == [["A", "B"], ["C", "D"]]
