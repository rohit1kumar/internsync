import os
import csv
import gspread
from gspread.exceptions import WorksheetNotFound
from dotenv import load_dotenv

load_dotenv()

credentials_dict = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
}


class GoogleSheet:
    def __init__(self, headers=[]):
        self.gs = gspread.service_account_from_dict(credentials_dict)
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
            print("=== Data written to Google Sheet ===")
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
        print("=== Data written to CSV file ===")

    def close(self):
        self.csv_file.close()
