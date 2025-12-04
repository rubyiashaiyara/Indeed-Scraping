
from playwright.sync_api import sync_playwright
from urllib.parse import quote
import time

def generate_indeed_url(job, location):
    """
    Generate Indeed UK URL for a job search.
    """
    job_encoded = quote(job)
    location_encoded = quote(location)
    url = f"https://uk.indeed.com/jobs?q={job_encoded}&l={location_encoded}"
    return url

def scrape_companies_and_addresses(job="Teacher", location="England"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        url = generate_indeed_url(job, location)
        page.goto(url)
        print(f"Navigated to: {url}")

        page.wait_for_timeout(6000)

        # -----------------------------
        # Job card list
        # -----------------------------
        ul_xpath = '//*[@id="mosaic-provider-jobcards"]/div/ul'
        li_xpath = ul_xpath + '/li'

        job_cards = page.locator(f"xpath={li_xpath}")
        count = job_cards.count()
        print(f"Total LI job cards found: {count}")

        job_info = []

        for i in range(count):
            try:
                card = job_cards.nth(i)

                # Extract company name
                try:
                    company = card.locator(".css-1afmp4o.e37uo190").inner_text().strip()
                except:
                    company = "N/A"

                # Extract company address
                try:
                    address = card.locator("div[data-testid='text-location']").inner_text().strip()
                except:
                    address = "N/A"

                job_info.append({"company": company, "address": address})
                print(f"{i+1}. Company: {company} | Address: {address}")

            except Exception as e:
                print("Error:", e)

        print("\nAll extracted job info:")
        for info in job_info:
            print(info)

        print("\nDone. Browser will stay open for 15 seconds...")
        time.sleep(15)
        browser.close()

if __name__ == "__main__":
    scrape_companies_and_addresses(job="IT", location="England")
