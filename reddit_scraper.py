import praw
import pandas as pd
from datetime import datetime, timedelta
import os
import json
from pathlib import Path
import sys
import logging

# Configure absolute paths
PROJECT_ROOT = Path(__file__).parent.parent  # Adjust based on your folder structure
DATA_FOLDER = PROJECT_ROOT / "nsource"
DEFAULT_OUTPUT_PATH = DATA_FOLDER / "redditnews.csv"
REDDIT_LINKS_PATH = PROJECT_ROOT / "sources" / "reddit_subreddits.json"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def verify_paths():
    """Ensure all required directories exist"""
    try:
        if not DATA_FOLDER.exists():
            logging.info(f"Creating data directory: {DATA_FOLDER}")
            DATA_FOLDER.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Path verification failed: {str(e)}")
        return False

def load_subreddits(json_path):
    """Load list of subreddits from JSON"""
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Failed to load subreddit list from {json_path}: {e}")
        return []

def calculate_time_difference(post_timestamp):
    """Calculate human-readable time difference"""
    now = datetime.utcnow()
    time_diff = now - post_timestamp

    if time_diff.days > 0:
        return f"{time_diff.days}d"
    elif time_diff.seconds // 3600 > 0:
        return f"{time_diff.seconds // 3600}h"
    elif time_diff.seconds // 60 > 0:
        return f"{time_diff.seconds // 60}m"
    else:
        return "Just now"

def initialize_reddit_client():
    """Initialize and return the Reddit API client"""
    return praw.Reddit(
        client_id='Uts0Cd-b7nms_IjwSpRGQA',
        client_secret='dx9CN_Isis2HZv_9LZQJo0bRswwdLA',
        user_agent='scraper by /u/Plane_Carry_9421'
    )

def scrape_subreddit(subreddit_name, reddit_client, limit=100, output_path=None):
    """
    Scrape posts from a subreddit and save to CSV
    """
    if output_path is None:
        output_path = DEFAULT_OUTPUT_PATH

    logging.info(f"Scraping r/{subreddit_name} (limit: {limit})")
    subreddit = reddit_client.subreddit(subreddit_name)
    posts = []

    try:
        for post in subreddit.new(limit=limit):
            post_timestamp = datetime.fromtimestamp(post.created_utc)
            time_diff = datetime.utcnow() - post_timestamp

            if time_diff <= timedelta(days=2):
                posts.append({
                    'Headline': post.title,
                    'Time': calculate_time_difference(post_timestamp),
                    'Created': post_timestamp,
                    'Upvote_Ratio': post.upvote_ratio,
                    'Subreddit': subreddit_name
                })

    except Exception as e:
        logging.error(f"Error scraping r/{subreddit_name}: {str(e)}")

    df = pd.DataFrame(posts)

    if not df.empty:
        try:
            df.to_csv(output_path, index=False)
            logging.info(f"Saved {len(df)} posts to {output_path}")
        except Exception as e:
            logging.error(f"Failed to save CSV: {str(e)}")

    return df

def run_scraper():
    """Main scraping function"""
    if not verify_paths():
        return

    subreddits = load_subreddits(REDDIT_LINKS_PATH)
    if not subreddits:
        logging.warning("No subreddits to scrape. Exiting.")
        return

    reddit = initialize_reddit_client()
    limit = 50
    all_posts = []

    for subreddit in subreddits:
        df = scrape_subreddit(subreddit, reddit, limit=limit)
        if not df.empty:
            all_posts.append(df)

    if all_posts:
        combined_df = pd.concat(all_posts, ignore_index=True)
        try:
            combined_df.to_csv(DEFAULT_OUTPUT_PATH, index=False)
            logging.info(f"Saved combined data ({len(combined_df)} posts) to {DEFAULT_OUTPUT_PATH}")

            if os.path.exists(DEFAULT_OUTPUT_PATH):
                logging.info("File verification successful")
            else:
                logging.error("File verification failed - output not found")
        except Exception as e:
            logging.error(f"Failed to save combined CSV: {str(e)}")

if __name__ == "__main__":
    logging.info("Starting Reddit scraper")
    run_scraper()
    logging.info("Scraping complete")
