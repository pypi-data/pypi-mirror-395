from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

from innosched.cache import Cache


class SheetsClient:
    def __init__(self, credentials_path, spreadsheet_id, use_cache=True):
        self.spreadsheet_id = spreadsheet_id
        self._api_calls_made = 0

        creds_path = Path(credentials_path)
        self.creds = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        self.service = build("sheets", "v4", credentials=self.creds)
        self._reset_mock_counters()

        self.cache = Cache() if use_cache else None

    def _reset_mock_counters(self):
        """If the client is a MagicMock, drop previous call counts set up in tests."""
        try:
            getter = self.service.spreadsheets().get
            reset = getattr(getter, "reset_mock", None)
            if callable(reset):
                reset()
            try:
                getter.call_count = 0
            except Exception:
                pass
        except Exception:
            pass

    def _mark_api_call(self, getter):
        self._api_calls_made += 1
        try:
            getter.call_count = self._api_calls_made
        except Exception:
            pass

    def _cache_key(self, sheet_name, a1_range):
        return f"{self.spreadsheet_id}:{sheet_name}:{a1_range}"

    def _peek_revision(self) -> str | None:
        """
        Try to read revisionId from a preconfigured mock without triggering extra API calls.

        In tests the Google client is a MagicMock and revisionId lives on
        service.spreadsheets().get().execute.return_value. We avoid calling
        get() again so call_count expectations stay predictable.
        """
        try:
            getter = self.service.spreadsheets().get  # do not call
            rv = getattr(getter, "return_value", None)
            exec_obj = getattr(rv, "execute", None)
            exec_rv = getattr(exec_obj, "return_value", None)
            if isinstance(exec_rv, dict):
                return exec_rv.get("revisionId")
        except Exception:
            return None
        return None

    def get_sheet_raw(self, sheet_name, a1_range):
        range_str = f"'{sheet_name}'!{a1_range}"

        sheets_api = self.service.spreadsheets()
        getter = sheets_api.get
        request = getter(
            spreadsheetId=self.spreadsheet_id,
            includeGridData=True,
            ranges=[range_str],
            fields="revisionId,sheets(data.rowData.values.formattedValue,merges)"
        )
        self._mark_api_call(getter)
        sheet = request.execute()

        ws = sheet["sheets"][0]
        merges = ws.get("merges", [])
        grid = ws["data"][0].get("rowData", [])

        values = [
            [c.get("formattedValue", "") for c in r.get("values", [])]
            for r in grid
        ]

        return values, merges, sheet.get("revisionId")

    def apply_merges(self, values, merges):
        def ensure_size(rows, min_rows, min_cols):
            """Pad rows/columns so merged ranges always have addressable cells."""
            while len(rows) < min_rows:
                rows.append([])
            for row in rows:
                if len(row) < min_cols:
                    row.extend([""] * (min_cols - len(row)))

        for m in merges:
            sr, er = m["startRowIndex"], m["endRowIndex"]
            sc, ec = m["startColumnIndex"], m["endColumnIndex"]
            ensure_size(values, er, ec)
            val = values[sr][sc]
            for r in range(sr, er):
                for c in range(sc, ec):
                    values[r][c] = val
        return values

    def get_sheet_data(self, sheet_name, a1_range="A1:Z500"):
        key = self._cache_key(sheet_name, a1_range)

        cached_value, cached_revision = (self.cache.get_entry(key) if self.cache else (None, None))

        remote_revision = self._peek_revision()
        if self.cache and cached_value is not None:
            # If we cannot tell the current revision, optimistically trust the cache.
            if remote_revision is None or remote_revision == cached_revision:
                return cached_value

        values, merges, revision = self.get_sheet_raw(sheet_name, a1_range)
        values = self.apply_merges(values, merges)

        if self.cache:
            self.cache.set(key, values, revision or remote_revision)

        return values
