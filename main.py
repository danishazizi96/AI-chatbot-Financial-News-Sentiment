import os
import sys
import time
from pathlib import Path
import logging
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Define absolute paths
PROJECT_ROOT = Path(__file__).parent
SCRAPERS = {
    "Binance": PROJECT_ROOT / "news_scrapper" / "binance_scraper.py",
    "Biztoc": PROJECT_ROOT / "news_scrapper" / "biztoc_scraper.py",
    "Yahoo": PROJECT_ROOT / "news_scrapper" / "yahoo_scraper.py"
}
REDDIT_SCRAPER = PROJECT_ROOT / "news_scrapper" / "reddit_scraper.py"
FINBERT_SCRIPT = PROJECT_ROOT / "sentiment_analysis" / "finbert_analysis.py"
CHATBOT_SCRIPT = PROJECT_ROOT / "chatbot" / "chatgpt_handler.py"
DATA_FOLDER = PROJECT_ROOT / "nsource"

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu"""
    clear_screen()
    print("\n" + "="*50)
    print("FINANCIAL SENTIMENT ANALYSIS SYSTEM".center(50))
    print("="*50)
    print("\nMAIN MENU:")
    print("1. Run Program (Scrape All News Sources)")
    print("2. Run FinBERT Analysis")
    print("3. Chatbot")
    print("4. Quit")
    print("\n" + "="*50)

def run_scraper_script(script_path):
    """Run a Python scraper script with proper path handling"""
    try:
        os.chdir(str(script_path.parent))
        result = os.system(f'python "{script_path.name}"')
        os.chdir(str(PROJECT_ROOT))  # Return to project root
        return result == 0
    except Exception as e:
        logging.error(f"Error running {script_path.name}: {str(e)}")
        return False

def run_reddit_scraper():
    """Special handling for Reddit scraper"""
    try:
        # Add to Python path for module import
        sys.path.insert(0, str(REDDIT_SCRAPER.parent))
        
        from news_scrapper.reddit_scraper import main as reddit_main
        reddit_main()
        return True
    except Exception as e:
        logging.error(f"Reddit scraper failed: {str(e)}")
        return False

def run_scrapers():
    """Run all news scraper scripts"""
    clear_screen()
    logging.info("RUNNING ALL NEWS SCRAPERS...")
    print("="*50 + "\n")
    
    # Run standard scrapers
    for name, path in SCRAPERS.items():
        if not path.exists():
            logging.error(f"{name} scraper not found at {path}")
            continue
            
        logging.info(f"Running {name} scraper...")
        if run_scraper_script(path):
            logging.info(f"{name} scraper completed successfully!")
        else:
            logging.error(f"{name} scraper failed!")
        print("-"*50)
        time.sleep(1)
    
    # Run Reddit scraper with special handling
    logging.info("Running Reddit scraper...")
    if run_reddit_scraper():
        logging.info("Reddit scraper completed successfully!")
    else:
        logging.error("Reddit scraper failed!")
    print("-"*50)
    
    # Verify all output files
    verify_output_files()
    
    input("\nPress Enter to return to main menu...")

def verify_output_files():
    """Verify all expected output files exist"""
    expected_files = {
        "Binance": "binancenews.csv",
        "Biztoc": "biztocnews.csv",
        "Yahoo": "yahoonews.csv",
        "Reddit": "redditnews.csv"
    }
    
    print("\nVERIFYING OUTPUT FILES:")
    all_success = True
    for source, filename in expected_files.items():
        filepath = DATA_FOLDER / filename
        if filepath.exists():
            try:
                # Quick check if file is readable
                pd.read_csv(filepath, nrows=1)
                print(f"✓ {source:8} -> {filepath} (Valid)")
            except:
                print(f"✗ {source:8} -> {filepath} (Corrupted)")
                all_success = False
        else:
            print(f"✗ {source:8} -> {filepath} (Missing)")
            all_success = False
    
    return all_success

def run_finbert():
    """Run FinBERT analysis script"""
    clear_screen()
    logging.info("RUNNING FINBERT ANALYSIS...")
    print("="*50 + "\n")
    
    if not FINBERT_SCRIPT.exists():
        logging.error(f"FinBERT script not found at {FINBERT_SCRIPT}")
        input("\nPress Enter to return to main menu...")
        return
    
    try:
        result = run_scraper_script(FINBERT_SCRIPT)
        if result:
            logging.info("FinBERT analysis completed successfully!")
            
            # Verify output
            output_path = PROJECT_ROOT / "sentiment_analysis" / "finbert_analyzed_news.csv"
            if output_path.exists():
                try:
                    pd.read_csv(output_path)
                    logging.info(f"Output verified at {output_path}")
                except:
                    logging.error("Output file exists but is corrupted")
        else:
            logging.error("FinBERT analysis failed!")
    except Exception as e:
        logging.error(f"Error running FinBERT: {str(e)}")
    
    input("\nPress Enter to return to main menu...")

def run_chatbot():
    """Run the ChatGPT handler"""
    clear_screen()
    logging.info("STARTING FINANCIAL CHATBOT...")
    print("="*50 + "\n")
    
    if not CHATBOT_SCRIPT.exists():
        logging.error(f"Chatbot script not found at {CHATBOT_SCRIPT}")
        input("\nPress Enter to return to main menu...")
        return
    
    try:
        # Add to Python path for module import
        sys.path.insert(0, str(CHATBOT_SCRIPT.parent))
        
        from chatbot.chatgpt_handler import main as chatbot_main
        chatbot_main()
    except Exception as e:
        logging.error(f"Chatbot failed: {str(e)}")
    
    input("\nPress Enter to return to main menu...")

def main():
    """Main program loop"""
    # Verify paths
    if not DATA_FOLDER.exists():
        logging.info(f"Creating data directory: {DATA_FOLDER}")
        DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_scrapers()
        elif choice == "2":
            run_finbert()
        elif choice == "3":
            run_chatbot()
        elif choice == "4":
            print("\nThank you for using the Financial Sentiment Analysis System. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)