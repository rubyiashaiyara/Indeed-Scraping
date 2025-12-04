#job companyname and location and company name

from playwright.sync_api import sync_playwright
from urllib.parse import quote
import time
import json 

def generate_indeed_url(job: str, location: str) -> str:
    site_url  = "https://www.indeed.com/jobs?q=it+support&l=Orlando%2C+FL"
    return site_url
    # return (
    #     https://www.indeed.com/jobs?q=it+support&l=Orlando%2C+FL
    #     "https://www.indeed.com/jobs"
    #     f"?q={quote(job)}"
    #     f"&l={quote(location)}"
    # )

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
        
        lis = page.locator("li.css-1ac2h1w.eu4oa1w0")
        count = lis.count()
        
        print(f"Pages Found : {count}")
        
        results = []
        for i in range(1, lis.count()):
            li = lis.nth(i)

            # extract company name
            # company = li.locator("span[data-testid='company-name']").inner_text()
            
            
             # safely extract company name
            company_loc = li.locator("span[data-testid='company-name']").first

            try:
                company = company_loc.inner_text(timeout=0)
            except:
                company = "N/A"
                
            results.append(company)

        # ----------------------------------------------------------
        # Grab all job cards inside the mosaic-provider-jobcards UL
        # ----------------------------------------------------------
        # li_selector = '//*[@id="mosaic-provider-jobcards"]/div/ul/li'
        # cards = page.locator(f"xpath={li_selector}")
        # count = cards.count()
        # print(f"Found {count} job cards\n")

        # results = []
        # for idx in range(count):
        #     card = cards.nth(idx)

        #     # ---- title ----
        #     try:
        #         title = card.locator(".css-pt3vth.e37uo190").inner_text().strip()
        #     except Exception:
        #         title = "N/A"

        #     # ---- company ----
        #     try:
        #         company = card.locator(".css-1afmp4o.e37uo190").inner_text().strip()
        #     except Exception:
        #         company = "N/A"

        #     # ---- location/address ----
        #     try:
        #         address = card.locator('div[data-testid="text-location"]').inner_text().strip()
        #     except Exception:
        #         address = "N/A"

        #     results.append({"title": title, "company": company, "address": address})
        #     print(f"{idx + 1:>2}. {title} | {company} | {address}")

        print("\n--- Finished scraping ---")
        print("Browser stays open for 15 s so you can inspect the page…")
        time.sleep(5)
        browser.close()

        return results

if __name__ == "__main__":
    scrape_indeed(job="IT", location="England")