from playwright.sync_api import sync_playwright
from urllib.parse import quote
import time
import json 

def generate_indeed_url(job: str, location: str) -> str:
    return (
        "https://uk.indeed.com/jobs"
        f"?q={quote(job)}"
        f"&l={quote(location)}"
    )

def scrape_indeed(job: str = "Teacher", location: str = "England"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        url = generate_indeed_url(job, location)
        print(f"Navigating to: {url}")
        page.goto(url)
        page.wait_for_timeout(3)

        # -------------------------
        # Scroll to load more jobs
        # -------------------------
        previous_height = None
        while True:
            current_height = page.evaluate("document.body.scrollHeight")
            if previous_height == current_height:
                break  # reached the bottom
            previous_height = current_height
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)  

        # -------------------------
        # Grab all job cards
        # -------------------------
        li_selector = '//*[@id="mosaic-provider-jobcards"]/div/ul/li'
        cards = page.locator(f"xpath={li_selector}")
        count = cards.count()
        print(f"Found {count} job cards\n")

        results = []
        for idx in range(count):
            card = cards.nth(idx)

            # ---- title ----
            try:
                title = card.locator(".css-pt3vth.e37uo190").inner_text().strip()
            except Exception:
                title = "N/A"

            # ---- company ----
            try:
                company = card.locator(".css-1afmp4o.e37uo190").inner_text().strip()
            except Exception:
                company = "N/A"

            # ---- location/address ----
            try:
                address = card.locator('div[data-testid="text-location"]').inner_text().strip()
            except Exception:
                address = "N/A"

            results.append({"title": title, "company": company, "address": address})
            print(f"{idx + 1:>2}. {title} | {company} | {address}")

        print("\n--- Finished scraping ---")
        print("Browser stays open for 15 s so you can inspect the page…")
        time.sleep(15)
        browser.close()

        return results

if __name__ == "__main__":
    scrape_indeed(job="IT", location="England")
