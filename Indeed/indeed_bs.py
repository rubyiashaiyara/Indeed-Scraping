import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

url = "https://indeed.com/jobs?q=python+developer&l=London"
response = requests.get(url, headers=headers)

# Step 1: Get the page
# response = requests.get(url)
html_content = response.text  # raw HTML

# Step 2: Parse (optional)
soup = BeautifulSoup(html_content, "html.parser")

# Step 3: Save the HTML to a file
with open("indeed.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())    # prettified HTML
    # or: f.write(html_content) # raw HTML
