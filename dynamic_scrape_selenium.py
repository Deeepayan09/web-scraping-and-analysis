# dynamic_scrape_selenium.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://quotes.toscrape.com/js")  # example JS version
time.sleep(2)  # wait for JS to render, or use WebDriverWait

quotes = driver.find_elements(By.CSS_SELECTOR, ".quote")
results = []
for q in quotes:
    text = q.find_element(By.CSS_SELECTOR, ".text").text
    author = q.find_element(By.CSS_SELECTOR, ".author").text
    tags = [t.text for t in q.find_elements(By.CSS_SELECTOR, ".tags a.tag")]
    results.append({"text": text, "author": author, "tags": ";".join(tags)})

driver.quit()

with open("quotes_js.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text","author","tags"])
    writer.writeheader()
    for r in results:
        writer.writerow(r)
