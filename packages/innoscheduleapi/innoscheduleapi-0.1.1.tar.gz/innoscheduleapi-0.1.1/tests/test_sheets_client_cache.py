from unittest.mock import MagicMock, patch
import tempfile
from pathlib import Path

from core.sheets_client import SheetsClient
from core.cache import Cache


def test_sheet_cache_reuse(tmp_path):
    db = tmp_path / "cache.db"

    with patch("innosched.sheets_client.Cache", lambda: Cache(db_path=db)):
        with patch("innosched.sheets_client.build") as mock_build:
            # мок сервиса
            service = MagicMock()
            service.spreadsheets().get().execute.return_value = {
                "sheets": [{
                    "data": [{
                        "rowData": [
                            {"values": [{"formattedValue": "A"}]}
                        ]
                    }],
                    "merges": []
                }],
                "revisionId": "rev1"
            }

            mock_build.return_value = service

            client = SheetsClient("credentials.json", "spread", use_cache=True)

            v1 = client.get_sheet_data("BS1")
            assert v1 == [["A"]]
            assert service.spreadsheets().get.call_count == 1

            v2 = client.get_sheet_data("BS1")
            assert v2 == [["A"]]

            assert service.spreadsheets().get.call_count == 1


def test_sheet_cache_invalidated_on_revision_change(tmp_path):
    db = tmp_path / "cache.db"

    with patch("innosched.sheets_client.Cache", lambda: Cache(db_path=db)):
        with patch("innosched.sheets_client.build") as mock_build:
            service = MagicMock()

            service.spreadsheets().get().execute.return_value = {
                "sheets": [{
                    "data": [{
                        "rowData": [
                            {"values": [{"formattedValue": "A"}]}
                        ]
                    }],
                    "merges": []
                }],
                "revisionId": "rev1"
            }

            mock_build.return_value = service
            client = SheetsClient("credentials.json", "spread", use_cache=True)

            v1 = client.get_sheet_data("BS1")
            assert v1 == [["A"]]

            service.spreadsheets().get().execute.return_value = {
                "sheets": [{
                    "data": [{
                        "rowData": [
                            {"values": [{"formattedValue": "B"}]}
                        ]
                    }],
                    "merges": []
                }],
                "revisionId": "rev2"
            }

            v2 = client.get_sheet_data("BS1")
            assert v2 == [["B"]]

            assert service.spreadsheets().get.call_count == 2
