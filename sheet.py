import os
import csv
import gspread
from gspread.exceptions import WorksheetNotFound
from dotenv import load_dotenv

load_dotenv()


class GoogleSheet:
    def __init__(self, headers=[]):
        self.gs = gspread.service_account(filename="credentials.json")
        self.spreadsheet_id = os.getenv("GOOGLE_SPREADSHEET_ID")
        self.headers = headers
        self.ws_format = {
            "backgroundColor": {"red": 1.0, "green": 1.0, "blue": 0.0},
            "horizontalAlignment": "CENTER",
            "textFormat": {
                "bold": True,
                "fontSize": 12,
                "foregroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0},
            },
        }

    def _get_or_create_worksheet(self, sheet_name):
        try:
            return self.gs.open_by_key(self.spreadsheet_id).worksheet(sheet_name)
        except WorksheetNotFound:
            return self.gs.open_by_key(self.spreadsheet_id).add_worksheet(
                title=sheet_name, rows=0, cols=5
            )

    def write(self, json_data, sheet_name="Internships"):
        try:
            worksheet = self._get_or_create_worksheet(sheet_name)
            worksheet.clear()

            # convert list of dict to list of list with fieldnames as header
            list_data = [self.headers]
            for data in json_data:
                list_data.append([data[header] for header in self.headers])

            worksheet.update("A1", list_data)
            worksheet.format("A1:E1", self.ws_format)
            print("Data written to Google Sheet.")
        except Exception as e:
            print(f"Error while writing to Google Sheet: {str(e)}")


class CSVFile:
    def __init__(self, headers=[], file_name="internships.csv"):
        self.csv_file = open(file_name, "w", newline="", encoding="utf-8")
        self.headers = headers
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=self.headers)
        self.csv_writer.writeheader()

    def write(self, data):
        self.csv_writer.writerow(data)

    def close(self):
        self.csv_file.close()