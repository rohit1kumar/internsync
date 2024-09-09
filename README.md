# InternSync
A Playwright based web scraper to scrape internships from [Internshala](https://internshala.com/), written in Python. Data is stored in a CSV file.

## Disclaimer
*This is for educational purposes only. I am not responsible for any misuse of this code.*

## Features
- Store data in a CSV file
- Store data in a Google Sheet (optional)
- Keeps the Google Sheet data synced using GitHub Actions (optional)

## Prerequisites
Make sure you have the following dependencies installed:

- [Playwright](https://playwright.dev/python/docs/library/) library for Python 
- Python 3.x

*you can install them using the following commands too:* 
```bash
pip install playwright && playwright install chromium
```

## Usage
1. Clone the repository
2. Install the dependencies using `pip install -r requirements.txt`
3. Run the script using `python main.py`

Optional steps (for Google Sheets mode only):
1. Create a new Google Sheet
2. Create a new project in [Google Cloud Platform](https://console.cloud.google.com/)
3. Follow this guide for setting up the [Google Sheets API](https://docs.gspread.org/en/v5.12.0/oauth2.html#for-bots-using-service-account)
4. Download the JSON file and add all the credentials to the `.env` file (refer to `.env.example`)
5. Get the Google Sheet ID from the URL e.g `https://docs.google.com/spreadsheets/d/GOOGLE_SHEET_ID/edit`
6. Add to `GOOGLE_SHEET_ID` to the `.env` file

Optional steps (for syncing Google Sheets using GitHub Actions):
1. GitHub Actions are already setup in the repository
2. Download GitHub CLI or add secrets manually to the repository from `.env` file
3. With GitHub CLI run `gh secret set -R <your-username/your-repo> -f .env`

## Options
- `--headful`: Run the script in non-headless mode (show the browser)
    ```bash
    python main.py --headful
    ```
- `--gs`: Run the script in Google Sheets mode (store data in Google Sheets)
    ```bash
    python main.py --gs
    ```
[//]: # (- `--limit`: Limit the number of internships to scrape &#40;default: 10&#41;)

[//]: # (- `--output`: Output file name &#40;default: internships.csv&#41; )
