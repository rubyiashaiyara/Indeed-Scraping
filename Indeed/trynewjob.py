import requests

# The page you want to scrape
url = "https://d3fw5vlhllyvee.cloudfront.net/one-trust/dist/97713fd03bac2bb463568ba9c73b45b2/indeed/consent/0d4d9047-e9bb-46ba-b003-a0bd1f4a7d4f/01929162-0d1e-7e10-a768-2c4a24019f82/en.json"

# Fetch the page
response = requests.get(url)

# Print the page HTML
print(response.text)
