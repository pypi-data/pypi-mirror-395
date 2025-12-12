"""Manual integration script that hits the real Google Sheet.

Run with `python -m tests.test_real_google_integration` so it does not
get executed during normal `pytest` runs. It uses the service account
credentials in `credentials.json` and reads the live BS1 worksheet to
verify the end‑to‑end pipeline (fetch -> parse -> print).
"""

from innosched.sheets_client import SheetsClient
from core.parser import ScheduleParser


def main():
    credentials = "credentials.json"
    spreadsheet_id = "1GlRGsy6-UvdIqj_E-iT9UBz9gvBNba5qHTjfm-npyjI"
    sheet_name = "BS1"

    client = SheetsClient(credentials, spreadsheet_id, use_cache=True)
    raw_values = client.get_sheet_data(sheet_name)
    schedule = ScheduleParser().parse(sheet_name, raw_values)

    for day in schedule.days:
        print(day.name)
        for lesson in day.lessons:
            print(" ", lesson.time, lesson.groups)


if __name__ == "__main__":
    main()
