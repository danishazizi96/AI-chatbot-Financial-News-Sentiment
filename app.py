from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import threading 
import logging
from pathlib import Path
from sentiment_analysis.finbert_analysis import run_finbert_analysis
from chatbot.chatgpt_handler import chat_with_gpt
import json
import requests
import yfinance as yf
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
from collections import Counter
import time
from threading import Thread
import os
import signal
import subprocess



# Initialize Flask app
app = Flask(__name__)

# Define project paths
PROJECT_ROOT = Path(__file__).parent
DATA_FOLDER = PROJECT_ROOT / "nsource"
OUTPUT_FOLDER = PROJECT_ROOT / "sentiment_analysis"
REDDIT_SCRAPER = PROJECT_ROOT / "news_scrapper" / "reddit_scraper.py"
BINANCE_SCRAPER = PROJECT_ROOT / "news_scrapper" / "binance_scraper.py"
BIZTOC_SCRAPER = PROJECT_ROOT / "news_scrapper" / "biztoc_scraper.py"
YAHOO_SCRAPER = PROJECT_ROOT / "news_scrapper" / "yahoo_scraper.py"
JSON_FILE_PATH = OUTPUT_FOLDER / "finbert_analyzed_news.json"
STOCKS_JSON_PATH = PROJECT_ROOT / "stocks.json"  # Assuming the JSON file with stock symbols

# Alpha Vantage API Key
API_KEY = 'ROE55NCMHOHUSSM3'  # Replace with your actual API key

# Log configuration
logging.basicConfig(level=logging.INFO)

# Global process variable to handle stopping the task
scraping_process = None

# ------------------------
# ROUTES
# ------------------------

# Welcome page route
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Main dashboard route (after pressing START)
@app.route('/index')
def index():
    return render_template('index.html')

# Stock Screener Route (via Yahoo Finance API)
@app.route('/stock_screener')
def stock_screener():
    return render_template('stock_screener.html')  # Ensure stock_screener.html is present

@app.route('/loading')
def loading():
    # Start the background task for scraping and analysis
    thread = Thread(target=run_scrapers)
    thread.start()
    
    # Render the loading page while the background task is running
    return render_template('loading.html')  # Loading page with animation

@app.route('/done')
def done():
    # After the task is completed, show the 'done' page
    return render_template('done.html')

# ------------------------
# New Route to Fetch FinBERT Analyzed News (Skip first 2 rows)
# ------------------------

@app.route('/get_finbert_news', methods=['GET'])
def get_finbert_news():
    try:
        # Get the page and pageSize from the request parameters
        page = int(request.args.get('page', 0))  # Default to page 0 (first page)
        page_size = int(request.args.get('pageSize', 10))  # Default to 10 headlines per page

        # Load the FinBERT analyzed news data from JSON file
        file_path = "C:/Users/Danish Azizi/Desktop/financial-sentiment-analysis/sentiment_analysis/finbert_analyzed_news.json"
        sentiment_data = load_json(file_path)
        
        # Skip the first two rows (entries)
        sentiment_data = sentiment_data[2:]

        # Get the headlines for the current page
        start_index = page * page_size
        end_index = start_index + page_size
        finbert_news = [{'Headline': entry['Headline'], 'Time': entry['Time'], 'Sentiment': entry['Sentiment']} for entry in sentiment_data[start_index:end_index]]
        
        return jsonify({"status": "success", "data": finbert_news})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})



# ------------------------
# Fetch Latest News Headlines
# ------------------------
@app.route('/get_latest_news', methods=['GET'])
def get_latest_news():
    try:
        # Load sentiment data
        sentiment_data = load_json("C:/Users/Danish Azizi/Desktop/financial-sentiment-analysis/sentiment_analysis/finbert_analyzed_news.json")
        
        # Get the most recent 5 news headlines from the sentiment data
        latest_headlines = [entry['Headline'] for entry in sentiment_data[:5]]

        return jsonify({"status": "success", "headlines": latest_headlines})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ------------------------
# Get Stock Data (1 Day) for multiple stocks
# ------------------------
@app.route('/get_multiple_stock_data', methods=['GET'])
def get_multiple_stock_data():
    # Load the stocks.json file
    with open(STOCKS_JSON_PATH) as f:
        stocks_data = json.load(f)

    symbols = [stock['symbol'] for stock in stocks_data["stocks"]]
    stock_data_list = []

    for symbol in symbols:
        try:
            # Fetch the 1-day stock data using yfinance
            stock = yf.Ticker(symbol)
            stock_data = stock.history(period="1d")
            
            if stock_data.empty:
                stock_data_list.append({"symbol": symbol, "error": "Stock data not available"})
                continue

            # Extract relevant stock data and convert to JSON serializable values
            stock_info = {
                'symbol': symbol,
                'name': stock.info.get('longName', 'N/A'),
                'price': float(stock_data['Close'].iloc[0]),  # Convert to float
                'change': float(stock_data['Close'].iloc[0] - stock_data['Open'].iloc[0]),  # Convert to float
                'volume': int(stock_data['Volume'].iloc[0]),  # Convert to int
                'marketCap': stock.info.get('marketCap', 'N/A'),
                'peRatio': stock.info.get('trailingPE', 'N/A')
            }
            stock_data_list.append(stock_info)

        except Exception as e:
            stock_data_list.append({"symbol": symbol, "error": f"Error fetching stock data: {str(e)}"})

    return jsonify(stock_data_list)

# ------------------------
# Scraping functions and other routes
# ------------------------
@app.route('/run_scrapers', methods=['POST'])
def run_scrapers():
    try:
        logging.info("Running all news scrapers...")

        # Start scraping news concurrently
        threads = [
            threading.Thread(target=run_scraper, args=(BINANCE_SCRAPER,)),
            threading.Thread(target=run_scraper, args=(BIZTOC_SCRAPER,)),
            threading.Thread(target=run_reddit_scraper),
            threading.Thread(target=run_scraper, args=(YAHOO_SCRAPER, DATA_FOLDER))
        ]

        # Start all scraper threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Run FinBERT after scraping
        logging.info("Running FinBERT analysis...")
        run_finbert()  # Ensure FinBERT runs after scraping is completed.

        return jsonify({"status": "success", "message": "Scraping and FinBERT analysis completed!"})
    except Exception as e:
        logging.error(f"Error running scrapers: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})


@app.route('/run_finbert', methods=['POST'])
def run_finbert():
    try:
        logging.info("Running FinBERT analysis...")
        run_finbert_analysis(DATA_FOLDER, OUTPUT_FOLDER)
        return jsonify({"status": "success", "message": "FinBERT analysis completed successfully!"})
    except Exception as e:
        logging.error(f"Error running FinBERT: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('input')
    if user_input:
        financial_data = load_json(JSON_FILE_PATH)
        response = chat_with_gpt(user_input, json_data=financial_data)
    else:
        response = "No input received."
    return jsonify({"response": response})

# ------------------------
# New Route to Fetch Articles Scanned
# ------------------------
@app.route('/get_articles_scanned', methods=['GET'])
def get_articles_scanned():
    try:
        # Path to the JSON or CSV file
        file_path = "C:\\Users\\Danish Azizi\\Desktop\\financial-sentiment-analysis\\sentiment_analysis\\finbert_analyzed_news.json"
        
        # Check if the file is JSON or CSV and load accordingly
        if file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                data = json.load(f)
            article_count = len(data)  # Number of entries in the JSON file
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            article_count = len(df)  # Number of rows in the CSV file
        
        return jsonify({"status": "success", "articles_scanned": article_count})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ------------------------
# Get Pie Chart Sentiment Distribution
# ------------------------
@app.route('/get_sentiment_distribution', methods=['GET'])
def get_sentiment_distribution():
    try:
        # Load the sentiment data from your JSON file
        sentiment_data = load_json("C:/Users/Danish Azizi/Desktop/financial-sentiment-analysis/sentiment_analysis/finbert_analyzed_news.json")
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

        if sentiment_data:
            # Count sentiment occurrences
            for entry in sentiment_data:
                sentiment = entry.get('Sentiment', '')
                if sentiment in sentiment_counts:
                    sentiment_counts[sentiment] += 1

            # Calculate percentages
            total_articles = len(sentiment_data)
            sentiment_percentages = {k: (v / total_articles) * 100 for k, v in sentiment_counts.items()}

            return jsonify({
                "status": "success",
                "sentiment_percentages": sentiment_percentages
            })
        else:
            raise ValueError("Sentiment data is empty.")

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ------------------------
# Wordcloud
# ------------------------
@app.route('/get_word_cloud', methods=['GET'])
def get_word_cloud():
    try:
        # Load sentiment data
        sentiment_data = load_json("C:/Users/Danish Azizi/Desktop/financial-sentiment-analysis/sentiment_analysis/finbert_analyzed_news.json")

        # Create a list of headlines
        headlines = [entry['Headline'] for entry in sentiment_data]

        # Combine all headlines into a single string
        all_headlines = ' '.join(headlines)

        # Remove punctuation and make lowercase
        all_headlines = all_headlines.translate(str.maketrans('', '', string.punctuation)).lower()

        # Split into words and filter out common stop words
        stopwords = set(['the', 'a', 'an', 'of', 'to', 'and', 'in', 'on', 'for', 'is', 'it', 'this', 'that', 'with', 'as', 'by', 'as', 'now', 'strong', '2025', '2026', 'will', 'into', 'why', 'what', 'over', 'one', 'be', 'amid', 'are','earnings', 'from','more', 'at', 'its', 'after', 'market', 'says' ,'you', 'than',' options'])
        words = [word for word in all_headlines.split() if word not in stopwords]

        # Count the frequency of each word
        word_counts = Counter(words)

        # Create the word cloud
        wordcloud = WordCloud(width=400, height=400, background_color='black').generate_from_frequencies(word_counts)

        # Save the word cloud image to a static path
        wordcloud_image_path = 'static/images/wordcloud.png'
        wordcloud.to_file(wordcloud_image_path)

        return jsonify({"status": "success", "wordcloud_image_path": wordcloud_image_path})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# ------------------------
# Get Top 10 Most Frequent Words
# ------------------------
@app.route('/get_top_10_words', methods=['GET'])
def get_top_10_words():
    try:
        # Load sentiment data
        sentiment_data = load_json("C:/Users/Danish Azizi/Desktop/financial-sentiment-analysis/sentiment_analysis/finbert_analyzed_news.json")

        # Create a list of headlines
        headlines = [entry['Headline'] for entry in sentiment_data]

        # Combine all headlines into a single string
        all_headlines = ' '.join(headlines)

        # Remove punctuation and make lowercase
        all_headlines = all_headlines.translate(str.maketrans('', '', string.punctuation)).lower()

        # Split into words and filter out common stop words
        stopwords = set(['the', 'a', 'an', 'of', 'to', 'and', 'in', 'on', 'for', 'is', 'it', 'this', 'that', 'with', 'as', 'by', 'as', 'now', 'strong', '2025', '2026', 'will', 'into', 'why', 'what', 'over', 'one', 'be', 'amid', 'are','earnings', 'from','more', 'at', 'its', 'after'])
        words = [word for word in all_headlines.split() if word not in stopwords]

        # Count the frequency of each word
        word_counts = Counter(words)

        # Get the 10 most common words
        top_10_words = word_counts.most_common(10)

        return jsonify({
            "status": "success",
            "top_10_words": top_10_words
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# ------------------------
# UTILITY FUNCTIONS
# ------------------------

def run_scraper(script_path, *args):
    try:
        logging.info(f"Running scraper: {script_path}")
        subprocess.run([r'C:\Users\Danish Azizi\Desktop\financial-sentiment-analysis\venv\Scripts\python.exe', str(script_path)], check=True)
        logging.info(f"Scraper {script_path} completed successfully!")
    except Exception as e:
        logging.error(f"Error running {script_path}: {str(e)}")

def run_reddit_scraper():
    try:
        logging.info("Running Reddit scraper...")
        subprocess.run([r'C:\Users\Danish Azizi\Desktop\financial-sentiment-analysis\venv\Scripts\python.exe', str(REDDIT_SCRAPER)], check=True)
        logging.info("Reddit scraper completed successfully!")
    except Exception as e:
        logging.error(f"Reddit scraper failed: {str(e)}")

def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            json_data = json.load(f)
        logging.info(f"Successfully loaded JSON data from {filepath}")
        return json_data
    except Exception as e:
        logging.error(f"Error loading JSON data: {str(e)}")
        return None

# ------------------------
# MAIN ENTRY POINT
# ------------------------

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)