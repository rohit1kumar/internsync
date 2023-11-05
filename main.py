import argparse, os
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from sheet import GoogleSheet, CSVFile

load_dotenv()

run_headless = True  # Default mode as headless
headers = ["title", "company", "stipend", "location", "link", "scraped_at"]


def scrape_internships():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=run_headless)
            page = browser.new_page()

            current_page = 1
            scraped_data = []

            while True:
                url = f"https://internshala.com/internships/backend-development,front-end-development,full-stack-development,node-js,node-js-development,python,python-django,software-development-internship/stipend-10000/page-{current_page}"

                page.goto(url)
                page.wait_for_selector(".individual_internship")

                internship_elements = page.query_selector_all(
                    ".individual_internship.visibilityTrackerItem"
                )

                for element in internship_elements:
                    title = (
                        element.query_selector(".profile").inner_text().strip() or "N/A"
                    )
                    company = (
                        element.query_selector(".link_display_like_text")
                        .inner_text()
                        .strip()
                        or "N/A"
                    )
                    stipend_element = element.query_selector(".stipend")
                    stipend = (
                        stipend_element.inner_text().replace("₹", "").strip()
                        if stipend_element
                        else "N/A"
                    )
                    location = (
                        element.query_selector(".location_link").inner_text().strip()
                        or "N/A"
                    )
                    link_element = element.query_selector(".view_detail_button")
                    link = (
                        "https://internshala.com"
                        + link_element.get_attribute("href").strip()
                        if link_element
                        else "N/A"
                    )
                    scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    scraped_data.append(
                        {
                            "title": title,
                            "company": company,
                            "stipend": stipend,
                            "location": location,
                            "link": link,
                            "scraped_at": scraped_at,
                        }
                    )

                print(f"Scraped data from page {current_page}")

                next_page_button = page.query_selector("#navigation-forward")
                is_last_page = next_page_button.get_attribute(
                    "class"
                ) and "disabled" in next_page_button.get_attribute("class")

                if not is_last_page:
                    current_page += 1
                else:
                    break
            print("=== Scraping completed ===")
            return scraped_data
        except Exception as e:
            print("Error while scraping: ", str(e))
        finally:
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Internshala for internships.")
    parser.add_argument(
        "--headful", action="store_true", help="Run in non-headless mode."
    )  # If this flag is passed, run in non-headless mode or headful mode (i.e. show browser)
    parser.add_argument(
        "--gs", action="store_true", help="Write data to Google Sheet."
    )  # If this flag is passed, write data to Google Sheet
    args = parser.parse_args()
    run_headless = not args.headful
    print(f"=== Running in {'headless' if run_headless else 'headful'} mode ===")
    scraped_json = scrape_internships()

    if args.gs:
        # Write to Google Sheet
        gs = GoogleSheet(headers=headers)
        gs.write(scraped_json)
    else:
        # Write to a local CSV file
        csv = CSVFile(headers=headers)
        for data in scraped_json:
            csv.write(data)
        csv.close()
