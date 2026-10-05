import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

# Path to your chromedriver
chrome_driver_path = r"C:\Users\Danish Azizi\Desktop\financial-sentiment-analysis\chromedriver-win64\chromedriver.exe"

# Path to Yahoo links JSON
yahoo_links_path = r"C:\Users\Danish Azizi\Desktop\financial-sentiment-analysis\sources\yahoo_links.json"

# Chrome options
options = Options()
options.add_argument('--headless')  # Uncomment to run headless
options.add_argument('--disable-gpu')
options.add_argument('window-size=1200x800')
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
)

# Service
service = Service(chrome_driver_path)

def load_yahoo_links(json_path):
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading Yahoo links from {json_path}: {e}")
        return []

def scrape_yahoo_news(save_dir):
    """
    Main function to scrape Yahoo Finance news and save to CSV.
    """
    urls = load_yahoo_links(yahoo_links_path)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        all_data = []

        for url in urls:
            headlines = scrape_headlines(driver, url)
            all_data.extend(headlines)
            time.sleep(2)

        filename = save_dir + r"\yahoonews.csv"
        save_to_csv(all_data, filename)

    except Exception as e:
        print(f"Error initializing WebDriver or scraping: {e}")

    finally:
        try:
            driver.quit()
        except:
            pass

def scrape_headlines(driver, url):
    print(f"\nScraping: {url}")
    driver.get(url)
    headlines_data = []

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h3'))
        )

        articles = driver.find_elements(By.CSS_SELECTOR, 'a:has(h3)')[:30]

        count = 0
        for article in articles:
            try:
                headline_elem = article.find_element(By.TAG_NAME, 'h3')
                time_elem = article.find_element(By.XPATH, ".//following::div[contains(@class, 'publishing')][1]")

                headline = headline_elem.text.strip()
                post_text = time_elem.text.strip()
                post_time = post_text.split("•")[1].strip() if "•" in post_text else post_text.strip()

                if len(headline) > 30 and headline not in [h[0] for h in headlines_data]:
                    headlines_data.append((headline, post_time))
                    count += 1
                if count >= 20:
                    break

            except NoSuchElementException:
                continue
            except Exception as e:
                print(f"Skipping article due to error: {e}")
                continue

        if headlines_data:
            print(f"Collected {len(headlines_data)} headlines.")
        else:
            print("No valid headlines found.")

    except TimeoutException:
        print("Timeout: Page didn't load expected content.")
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    except Exception as e:
        print(f"General error scraping {url}: {e}")

    return headlines_data

def save_to_csv(data, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Headline', 'Time'])
            for row in data:
                writer.writerow(row)
        print(f"\n✅ Data saved to: {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Prevent auto-running during import
if __name__ == "__main__":
    scrape_yahoo_news(r"C:\Users\Danish Azizi\Desktop\financial-sentiment-analysis\nsource")
