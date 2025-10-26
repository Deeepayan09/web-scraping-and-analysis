# scrape_quotes_bs4.py
import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE = "http://quotes.toscrape.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DataScraper/1.0; +https://example.com/bot)"
}

def parse_quote_block(block):
    text = block.find("span", class_="text").get_text(strip=True)
    author = block.find("small", class_="author").get_text(strip=True)
    tags = [t.get_text(strip=True) for t in block.select(".tags a.tag")]
    return {"text": text, "author": author, "tags": ";".join(tags)}

def scrape_quotes(max_pages=5, delay=1.0):
    results = []
    url = BASE
    for page in range(1, max_pages+1):
        print(f"Fetching page {page}: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print("Non-200 response:", resp.status_code)
            break
        soup = BeautifulSoup(resp.text, "lxml")
        quote_blocks = soup.select(".quote")
        if not quote_blocks:
            break
        for b in quote_blocks:
            results.append(parse_quote_block(b))
        # find next
        next_link = soup.select_one("li.next > a")
        if not next_link:
            break
        url = urljoin(BASE, next_link["href"])
        time.sleep(delay)  # polite
    return results

def save_to_csv(data, fname="quotes.csv"):
    keys = ["text", "author", "tags"]
    with open(fname, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"Saved {len(data)} rows to {fname}")

if __name__ == "__main__":
    data = scrape_quotes(max_pages=10, delay=1.0)
    save_to_csv(data)
