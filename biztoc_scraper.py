import requests
from bs4 import BeautifulSoup
import csv
import json

# Path to JSON file containing desired sources
biztoc_sources_path = r"C:\Users\Danish Azizi\Desktop\financial-sentiment-analysis\sources\biztoc_sources.json"

# Load desired sources from JSON
def load_desired_sources(json_path):
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading sources from {json_path}: {e}")
        return []

# Send a GET request to the website
url = 'https://biztoc.com/'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Load desired sources from JSON file
desired_sources = load_desired_sources(biztoc_sources_path)

# Initialize lists to store sources and headlines
sources = []
headlines = []

# Function to extract headlines and sources
def extract_headlines_and_sources(tag, source_name):
    # Find all headlines inside the <h2> tags within this section
    for h2 in tag.find_all('h2'):
        a_tag = h2.find('a')
        if a_tag:
            headline = a_tag.text.strip()
            headlines.append(headline)
            sources.append(source_name)

# Function to save data to CSV
def save_to_csv(headlines, sources, filename=r'C:\Users\Danish Azizi\Desktop\financial-sentiment-analysis\nsource\biztocnews.csv'):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Headline', 'Source'])  # Writing headers
            for source, headline in zip(sources, headlines):
                writer.writerow([headline, source])
        print(f"Filtered news data has been saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Add a check to avoid automatic execution when imported
if __name__ == "__main__":
    # Find and extract sources and headlines for "Bullish" and "Bearish"
    bullish_section = soup.find_all('div', class_='ngrid_pos')
    print(f"Found {len(bullish_section)} 'Bullish' sections")
    for section in bullish_section:
        source_name = "Bullish"
        extract_headlines_and_sources(section, source_name)

    # For "Bearish" - Target div with class "ngrid_neg"
    bearish_section = soup.find_all('div', class_='ngrid_neg')
    print(f"Found {len(bearish_section)} 'Bearish' sections")
    for section in bearish_section:
        source_name = "Bearish"
        extract_headlines_and_sources(section, source_name)

    # Extract Trending Posts
    trending_posts_section = soup.find('div', id='trendingposts')
    if trending_posts_section:
        print(f"Found 'Trending Posts' section")
        for a_tag in trending_posts_section.find_all('a', href=True):
            headline = a_tag.text.strip()
            link = a_tag['href']
            headlines.append(f"{headline} - {link}")
            sources.append("Trending")

    # Extract headlines from "ag_newsgrid"
    ag_newsgrid_section = soup.find_all('div', class_='ag_newsgrid')
    for section in ag_newsgrid_section:
        news_header = section.find('div', class_='news-header')
        if news_header:
            a_tag = news_header.find('a')
            if a_tag:
                headline = a_tag.text.strip()
                headlines.append(headline)
                sources.append("ag_newsgrid")

        # Extract additional news items from this section
        news_items = section.find_all('div', class_='news-item')
        for news_item in news_items:
            a_tag = news_item.find('a')
            if a_tag:
                headline = a_tag.text.strip()
                headlines.append(headline)
                sources.append("ag_newsgrid")

    # Find all columns with specific sources
    for column in soup.find_all('div', class_='column'):
        source_tag = column.find('h4')
        if source_tag:
            source_name = source_tag.text.strip()

            if source_name in desired_sources:
                for li in column.find_all('li'):
                    a_tag = li.find('a')
                    if a_tag:
                        headline = a_tag.text.strip()
                        headlines.append(headline)
                        sources.append(source_name)

    # Save the filtered data to a CSV file
    save_to_csv(headlines, sources)
