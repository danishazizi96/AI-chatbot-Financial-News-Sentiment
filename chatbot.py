import os
from dotenv import load_dotenv
from openai import OpenAI
import sys

# Load environment variables
load_dotenv()

def initialize_client():
    """Initialize and return the OpenAI client with API key validation"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("\033[91mError: OPENAI_API_KEY not found in .env file\033[0m")
        print("Please create a .env file with your API key like this:")
        print("OPENAI_API_KEY=your-api-key-here")
        sys.exit(1)
    
    if not api_key.startswith('sk-'):
        print("\033[91mError: Invalid API key format\033[0m")
        print("API keys should start with 'sk-'")
        sys.exit(1)
    
    return OpenAI(api_key=api_key)

client = initialize_client()

def chat_with_gpt(prompt, model="gpt-4-turbo"):
    """Send prompt to OpenAI and return response"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"\033[91mError: {str(e)}\033[0m"

def main():
    print("\033[94mWelcome to the ChatGPT Assistant!\033[0m")
    print("Type 'quit', 'exit', or 'bye' to end the chat\n")
    
    while True:
        try:
            user_input = input("\033[92mYou: \033[0m")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\033[94mGoodbye!\033[0m")
                break
                
            response = chat_with_gpt(user_input)
            print("\033[96mAssistant:\033[0m", response)
            
        except KeyboardInterrupt:
            print("\n\033[94mGoodbye!\033[0m")
            break

if __name__ == "__main__":
    main()