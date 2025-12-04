import requests
from bs4 import BeautifulSoup

def extract(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    }

    url = f"https://indeed.com/jobs?q=python+developer&l=London&start={page}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def transform(soup):
    job_cards = soup.find_all("div", class_="job_seen_beacon")

    for job in job_cards:
        # title
        title_tag = job.find("h2", class_="jobTitle")
        title = title_tag.find("span").text if title_tag else "No Title"

        print(title)

    return

# run
s = extract(0)
transform(s)
