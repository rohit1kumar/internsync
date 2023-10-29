# Internshala-Scraper-Py
A Playwright based web scraper to scrape internships from [Internshala](https://internshala.com/), written in Python. Data is stored in a CSV file.

## Disclaimer
*This is for educational purpose only. I am not responsible for any misuse of this code.*

## Prerequisites
Make sure you have the following dependencies installed:

- [Playwright](https://playwright.dev/python/docs/library/) library for Python 
- Python 3.x

*you can install them using the following commands too:* 
```bash
pip install playwright && playwright install
```

## Usage
1. Clone the repository
2. Install the dependencies using `pip install -r requirements.txt`
3. Run the script using `python main.py`

## Options
- `--headful`: Run the script in non-headless mode (show the browser)
    ```bash
    python main.py --headful
    ```

[//]: # (- `--limit`: Limit the number of internships to scrape &#40;default: 10&#41;)

[//]: # (- `--output`: Output file name &#40;default: internships.csv&#41; )