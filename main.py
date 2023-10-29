import csv
import random
import argparse
from playwright.sync_api import sync_playwright

run_headless = True  # Default mode as headless


def create_csv(file_name="data.csv"):
    csv_file = open(file_name, "w", newline="", encoding="utf-8")
    fieldnames = ["title", "company", "stipend", "location", "link"]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    return csv_file, csv_writer


def scrape_internships():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=run_headless)
            page = browser.new_page()
            csv_file, csv_writer = create_csv()

            current_page = 1

            while True:
                url = f"https://internshala.com/internships/backend-development,front-end-development,full-stack-development,node-js,node-js-development,python,python-django,software-development-internship/stipend-10000/page-{current_page}"

                page.goto(url)
                page.wait_for_selector(".individual_internship")

                internship_elements = page.query_selector_all(
                    ".individual_internship.visibilityTrackerItem"
                )

                scraped_data = []

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

                    scraped_data.append(
                        {
                            "title": title,
                            "company": company,
                            "stipend": stipend,
                            "location": location,
                            "link": link,
                        }
                    )

                csv_writer.writerows(scraped_data)
                print(f"Scraped data from page {current_page}")

                next_page_button = page.query_selector("#navigation-forward")
                is_last_page = next_page_button.get_attribute(
                    "class"
                ) and "disabled" in next_page_button.get_attribute("class")

                if not is_last_page:
                    # Sleep for a random time between 1 and 6 seconds before going to the next page
                    # random_integer_between_one_and_five = random.randint(1, 6)
                    # page.wait_for_timeout(random_integer_between_one_and_five * 1000)
                    current_page += 1
                else:
                    break
        except Exception as e:
            print(e)
        finally:
            csv_file.close()
            print("Done")
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Internshala for internships.")
    parser.add_argument(
        "--headful", action="store_true", help="Run in non-headless mode."
    )  # If this flag is passed, run in non-headless mode or headful mode (i.e. show browser)
    args = parser.parse_args()
    headless = not args.headful

    scrape_internships()
