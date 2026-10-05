import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException
from datetime import datetime

# Load Binance links from JSON
def load_binance_links(json_path):
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading links from {json_path}: {e}")
        return []

chrome_driver_path = r"C:\Users\Danish Azizi\Desktop\financial-sentiment-analysis\chromedriver-win64\chromedriver.exe"
binance_links_path = r"C:\Users\Danish Azizi\Desktop\financial-sentiment-analysis\sources\binance_links.json"

options = Options()
options.add_argument('--headless')  # Uncomment this for headless mode
options.add_argument('--disable-gpu')
options.add_argument('window-size=1200x800')
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
)

service = Service(chrome_driver_path)

def scrape_binance_news(url, max_posts=20):
    print(f"\nScraping: {url}")
    driver.get(url)
    headlines = []
    times = []

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h3, a[class="css-1xzdbqq"]'))
        )

        retry_count = 0
        max_retries = 2

        while len(headlines) < max_posts and retry_count < max_retries:
            try:
                prev_len = len(headlines)

                headline_elements = driver.find_elements(By.CSS_SELECTOR, 'h3, a[class="css-1xzdbqq"]')
                time_elements = driver.find_elements(By.CSS_SELECTOR, 'div.create-time')

                print(f"Found {len(headline_elements)} headlines and {len(time_elements)} time elements.")

                for i, elem in enumerate(headline_elements):
                    text = elem.text.strip()
                    if len(text) > 30 and text not in headlines:
                        headlines.append(text)
                        if i < len(time_elements):
                            time_text = time_elements[i].text.strip()
                            times.append(time_text)

                    if len(headlines) >= max_posts:
                        break

                if len(headlines) == prev_len:
                    retry_count += 1
                    print(f"No new headlines. Retry {retry_count}/{max_retries}")
                    time.sleep(1)

            except StaleElementReferenceException:
                print("Element became stale, retrying...")
                time.sleep(1)

        if headlines:
            print(f"Found {len(headlines)} headlines:")
            for idx, (headline, post_time) in enumerate(zip(headlines, times), 1):
                print(f"{idx}. {headline} - {post_time}")
        else:
            print("No readable headlines found.")

    except TimeoutException:
        print("Timeout: Page didn't load expected content.")
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    except Exception as e:
        print(f"General error scraping {url}: {e}")

    return headlines, times

def save_to_csv(headlines, times, filename=r'C:\Users\Danish Azizi\Desktop\financial-sentiment-analysis\nsource\binancenews.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Headline', 'Time'])
        for headline, time in zip(headlines, times):
            writer.writerow([headline, time])

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(service=service, options=options)

        # Load URLs from JSON
        binance_urls = load_binance_links(binance_links_path)

        all_headlines = []
        all_times = []

        for url in binance_urls:
            max_posts = 10 if 'decryptotokentalks' in url else 20
            headlines, times = scrape_binance_news(url, max_posts=max_posts)
            all_headlines.extend(headlines)
            all_times.extend(times)

        save_to_csv(all_headlines, all_times)

    finally:
        try:
            driver.quit()
        except:
            pass
