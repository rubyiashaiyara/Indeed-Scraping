from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fast_scrape(job="IT", location="England"):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        url = f"https://uk.indeed.com/jobs?q={job}&l={location}"
        page.goto(url)

        page.wait_for_selector("div.job_seen_beacon")  # only real job posts

        # 1) Get full HTML once
        html = page.content()

        # 2) Parse with BeautifulSoup (SUPER FAST)
        soup = BeautifulSoup(html, "html.parser")

        results = []

        # 3) Select only real job cards
        cards = soup.select("div.job_seen_beacon")

        for card in cards:
            # job title
            title_tag = card.select_one("h2.jobTitle span")
            title = title_tag.text.strip() if title_tag else "N/A"

            # company
            company_tag = card.select_one("span[data-testid='company-name']")
            company = company_tag.text.strip() if company_tag else "N/A"

            # location
            loc_tag = card.select_one("[data-testid='text-location']")
            location = loc_tag.text.strip() if loc_tag else "N/A"

            results.append({
                "title": title,
                "company": company,
                "location": location
            })

        browser.close()
        return results


data = fast_scrape()
for d in data:
    print(d)
