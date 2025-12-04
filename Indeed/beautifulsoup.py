import requests
from  bs4 import BeautifulSoup


def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q=python+developer&l=London&vjk=23661a9e95992609' 
    r = requests.get(url, headers=headers)
    return r.status_code

print(extract(0))