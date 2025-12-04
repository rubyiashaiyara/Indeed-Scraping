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
        page.wait_for_timeout(3000)

        # -------------------------
        # Scroll to load job cards
        # -------------------------
        print("Scrolling to load job cards...")
        for _ in range(3):  # scroll only 3 times (fast)
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(1)

        # -------------------------
        # Collect job card elements
        # -------------------------
        card_xpath = '//*[@id="mosaic-provider-jobcards"]/div/ul/li'
        cards = page.locator(f"xpath={card_xpath}")
        count = cards.count()
        print(f"Found {count} job cards\n")

        results = []

        # -------------------------
        # Loop through each job card
        # -------------------------
        for idx in range(count):
            print(f"\nScraping job {idx+1}/{count}")

            card = cards.nth(idx)

            # ---- title ----
            try:
                title = card.locator(".css-pt3vth.e37uo190").inner_text().strip()
            except:
                title = "N/A"

            # ---- company ----
            try:
                company = card.locator(".css-1afmp4o.e37uo190").inner_text().strip()
            except:
                company = "N/A"

            # ---- location ----
            try:
                address = card.locator('div[data-testid="text-location"]').inner_text().strip()
            except:
                address = "N/A"

            # -------------------------
            # SALARY (1st Try: From Job Card)
            # -------------------------
            try:
                salary = card.locator('span[data-testid="attribute_snippet_testid"]').inner_text().strip()
            except:
                salary = None  # fallback

            # -------------------------
            # SALARY (2nd Try: Click job to get detail salary)
            # -------------------------
            card.click()
            page.wait_for_timeout(1500)  # wait for right panel

            if salary is None:
                # Try salary snippet container
                try:
                    salary = page.locator('div[data-testid="salary-snippet-container"]').inner_text().strip()
                except:
                    # Try fallback container
                    try:
                        salary = page.locator('#salaryInfoAndJobType span').inner_text().strip()
                    except:
                        salary = "N/A"

            # -------------------------
            # Append result
            # -------------------------
            results.append({
                "title": title,
                "company": company,
                "address": address,
                "salary": salary,
            })

            print(f"→ {title} | {company} | {address} | Salary: {salary}")

        # -------------------------
        # Save results to JSON
        # -------------------------
        with open("indeed_jobs.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        print("\n--- Finished scraping. Data saved to 'indeed_jobs.json' ---")
        time.sleep(5)
        browser.close()

        return results


if __name__ == "__main__":
    scrape_indeed(job="IT", location="England")
