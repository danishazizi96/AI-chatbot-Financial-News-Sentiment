import os
from dotenv import load_dotenv
from openai import OpenAI
import sys
import pandas as pd
import json
import re  # Import regex for formatting the response

# Load environment variables
load_dotenv()

def initialize_client():
    """Initialize and return the OpenAI client with API key validation"""
    # HARDCODE the correct API key here
    api_key = "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"

    print(f"Loaded API Key: {api_key}")
    
    if not api_key:
        print("\033[91mError: OPENAI_API_KEY not found in .env file\033[0m")
        print("Please create a .env file with your API key like this: ")
        print("OPENAI_API_KEY=your-api-key-here")
        sys.exit(1)
    
    if not api_key.startswith('sk-'):
        print("\033[91mError: Invalid API key format\033[0m")
        print("API keys should start with 'sk-'")
        sys.exit(1)
    
    return OpenAI(api_key=api_key)

def load_json(filepath):
    """Load and return the JSON file with financial sentiment data"""
    try:
        with open(filepath, 'r') as f:
            json_data = json.load(f)
        print("\033[92mSuccessfully loaded JSON file\033[0m")
        return json_data
    except Exception as e:
        print(f"\033[91mError loading JSON file: {str(e)}\033[0m")
        return None

def analyze_financial_data(df):
    """Generate trading insights from the financial sentiment data"""
    if df is None or df.empty:
        return "No data available for analysis."
    
    try:
        # Prepare summary of the data for GPT
        summary = "Financial Sentiment Data Summary:\n"
        summary += f"- Total records: {len(df)}\n"
        summary += f"- Columns available: {', '.join(df.columns)}\n"
        
        if 'sentiment_score' in df.columns:
            summary += f"- Average sentiment score: {df['sentiment_score'].mean():.2f}\n"
            summary += f"- Positive sentiment ratio: {(df['sentiment_score'] > 0).mean():.2%}\n"
        
        if 'stock' in df.columns:
            top_stocks = df['stock'].value_counts().head(5)
            summary += "- Most mentioned stocks:\n"
            for stock, count in top_stocks.items():
                summary += f"  {stock}: {count} mentions\n"
        
        return summary
    
    except Exception as e:
        return f"Error analyzing data: {str(e)}"

client = initialize_client()

def chat_with_gpt(prompt, model="gpt-4o-mini-2024-07-18", json_data=None):
    """Send prompt to OpenAI with optional JSON data context and print the model used"""
    try:
        messages = [
    {
        "role": "system",
        "content": """
You are "Bill", an AI financial analyst and trading advisor. I want you to talk non-chalantly and more human. 
You are highly experienced in stocks, forex, and cryptocurrency markets, speaking with the tone of a friendly but no-nonsense advisor in his 40s-50s. Your tone is uplifting, confident, and firm, like a Wall Street veteran who’s seen every market cycle. You’re here to guide users through smart trading decisions based on sentiment and headline data provided in a JSON file.

You always analyze the market with a professional edge, drawing on sentiment trends, news headlines, and overall market conditions. Then, you provide clear and specific recommendations:

For stocks, use ticker symbols like AAPL (Apple), NVDA (Nvidia), TSLA (Tesla), etc.
For forex, use currency pairs like USD/JPY, EUR/USD, GBP/USD, etc.
For crypto, use symbols like BTC (Bitcoin), ETH (Ethereum), SOL (Solana), etc.

🔍 Your job includes:
- Reading and interpreting the sentiment and headline data from the JSON file
- Providing a brief market summary (e.g., “The market shows bullish momentum today based on tech news.”)
- Recommending specific assets to buy, sell, or hold
- Explaining why each recommendation matters using sentiment-backed reasoning

Keep responses clear, decisive, and no fluff. Never say “maybe” or “possibly”—you give actionable advice.
"""
    },
    {"role": "user", "content": prompt}
]
        
        if json_data is not None:
            # Use the JSON data directly instead of converting from CSV
            messages.insert(1, {
                "role": "system", 
                "content": f"Here's financial sentiment data to analyze:\n{json_data}"
            })

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500  # Increased for more detailed analysis
        )
        
        # Print the model being used
        print(f"\033[94mUsing model: {model}\033[0m")

        assistant_reply = response.choices[0].message.content

        # Format the response to include bold and line breaks
        formatted_reply = format_response(assistant_reply)

        return formatted_reply
    
    except Exception as e:
        return f"\033[91mError: {str(e)}\033[0m"

def format_response(text):
    """Format the assistant's response to include bold and line breaks"""
    # Replace `**` with `<strong>` for bold text
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Replace `###` with a new line (or paragraph)
    text = text.replace('###', '<br><br>')

    return text

def main():
    # Load the financial data (JSON format from FinBERT analysis)
    json_path = r"C:\Users\Danish Azizi\Desktop\financial-sentiment-analysis\sentiment_analysis\finbert_analyzed_news.json"
    financial_data = load_json(json_path)
    
    print("\033[94mWelcome to the Financial Trading Assistant!\033[0m")
    print("Type 'insights' to get trading recommendations from the data")
    print("Type 'quit', 'exit', or 'bye' to end the chat\n")
    
    while True:
        try:
            user_input = input("\033[92mYou: \033[0m").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\033[94mGoodbye!\033[0m")
                break
            elif user_input.lower() == 'Lets go':
                if financial_data is not None:
                    prompt = """
                    Analyze this financial sentiment data from finbert_analyzed_news.json. It should be sent to you. I want you to provide specific trading recommendations.
                    Consider:
                    1. Overall sentiment trends (keep in concise, only one sentence summary)
                    2. Most mentioned stocks (keep in concise, only one sentence summary
                    3. Provide:
                    - Specific stock recommendations (buy/sell/hold) with reasoning according to the JSON file given. Use specific ticker symbols from NASDAQ, BURSA, FOREX, CRYPTO, etc.
                    
                    """
                    print("\033[96mAnalyzing data...\033[0m")
                    response = chat_with_gpt(prompt, json_data=financial_data)
                    print("\033[96mAssistant:\033[0m", response)
                else:
                    print("\033[91mNo valid financial data available for analysis\033[0m")
            else:
                response = chat_with_gpt(user_input, json_data=financial_data)
                print("\033[96mAssistant:\033[0m", response)
            
        except KeyboardInterrupt:
            print("\n\033[94mGoodbye!\033[0m")
            break



if __name__ == "__main__":
    main()
