# 📈 AI-Powered Financial Analysis & Sentiment Intelligence

An AI-powered financial analysis platform that combines **financial news scraping, NLP sentiment analysis, market data, and generative AI** to help users make more informed stock trading decisions.
The system automatically collects financial news from multiple sources, analyzes sentiment using **FinBERT**, and provides AI-powered insights through an interactive web application.
---

## 🚀 Project Overview

Financial markets are heavily influenced by news, market sentiment, and rapidly changing events. Manually monitoring large volumes of financial news can be time-consuming and inefficient.

This project addresses that challenge by building an automated pipeline that:

1. 📰 Collects financial news from multiple sources
2. 🧹 Processes and cleans the collected data
3. 🤖 Performs financial sentiment analysis using **FinBERT**
4. 📊 Analyzes financial-market information
5. 🧠 Uses AI APIs to generate contextual insights
6. 💬 Provides an interactive chatbot for financial analysis
7. 📈 Allows users to explore stock-market information through the web interface

The goal is to transform large amounts of unstructured financial information into **actionable and understandable insights**.

---

## 🎯 Objectives

* Automate the collection of financial news.
* Analyze financial news sentiment using NLP.
* Reduce the time required for manual financial research.
* Combine sentiment data with market information.
* Provide AI-generated insights to support investment decisions.
* Develop an intuitive web-based financial analysis platform.
* Demonstrate the practical application of **Data Science, NLP, AI, and financial analytics**.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   Financial News    │
                    │      Sources        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Web Scrapers      │
                    │                     │
                    │ Binance             │
                    │ Yahoo Finance       │
                    │ Reddit              │
                    │ Biztoc              │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Data Processing &   │
                    │      Cleaning       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FinBERT        │
                    │ Sentiment Analysis  │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │ Financial Data  │        │ Sentiment Data  │
        │    Analysis     │        │   & Insights    │
        └────────┬────────┘        └────────┬────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌─────────────────────┐
                    │      AI Engine      │
                    │                     │
                    │ ChatGPT API         │
                    │ Gemini API          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Web Application   │
                    │                     │
                    │ Analysis Dashboard  │
                    │ AI Chatbot          │
                    │ Stock Information   │
                    └─────────────────────┘
```

---

## 🧠 Key Features

### 📰 Automated Financial News Scraping

The system gathers financial information from multiple sources, including:

* Binance
* Yahoo Finance
* Reddit
* Biztoc

This allows the platform to collect diverse perspectives from traditional financial media and online communities.

---

### 🤖 FinBERT Sentiment Analysis

Financial news headlines are analyzed using **FinBERT**, a BERT-based NLP model specifically designed for financial text.

Each headline is classified into sentiment categories such as:

* 🟢 Positive
* 🔴 Negative
* ⚪ Neutral

The resulting sentiment information is stored and used for downstream financial analysis.

---

### 📊 Financial Market Analysis

The platform combines sentiment information with financial-market data to identify potential relationships between:

**News → Sentiment → Market Conditions → Trading Insights**

Users can search for stocks and examine relevant market information through the web interface.

---

### 💬 AI Financial Chatbot

The project includes an AI-powered chatbot designed to help users interpret financial information.

The chatbot can use analyzed financial news and sentiment information to provide contextual responses and assist users in understanding market conditions.

AI APIs used in the project include:

* OpenAI GPT API
* Google Gemini API

> **Disclaimer:** The chatbot is an analytical and educational tool and does not constitute professional financial advice.

---

### 🖥️ Interactive Web Interface

The web application provides several core functions:

#### Analyze

Runs the financial-data collection and sentiment-analysis pipeline.

#### Chat

Opens the AI-powered financial chatbot.

#### Pending / Stock Search

Provides access to stock-market information and visualization functionality.

The interface was designed to make complex financial information easier to explore.

---

## 🛠️ Technology Stack

| Category                | Technologies                  |
| ----------------------- | ----------------------------- |
| Programming             | Python                        |
| Data Analysis           | Pandas, NumPy                 |
| Machine Learning        | FinBERT, Transformers         |
| NLP                     | Hugging Face Transformers     |
| Web Scraping            | Python-based scraping tools   |
| Database / Data Storage | CSV, SQL                      |
| AI                      | OpenAI API, Google Gemini API |
| Frontend                | HTML, CSS, JavaScript         |
| Backend                 | Python                        |
| Visualization           | Financial/stock charts        |
| Development             | VS Code                       |

---

## 🔄 Data Pipeline

```text
1. Collect Financial News
          ↓
2. Clean & Process Data
          ↓
3. Extract Headlines & Metadata
          ↓
4. FinBERT Sentiment Analysis
          ↓
5. Store Analyzed Results
          ↓
6. Combine With Market Data
          ↓
7. AI-Powered Interpretation
          ↓
8. Display Results Through Web App
```

---

## 📂 Project Structure

```text
financial-sentiment-analysis/
│
├── sources/
│   └── binance_links.json
│
├── static/
│   └── images/
│       ├── analyze.png
│       ├── chat.png
│       └── pending.png
│
├── templates/
│   ├── index.html
│   └── chatbot.html
│
├── scrapers/
│   ├── binance/
│   ├── yahoo/
│   ├── reddit/
│   └── biztoc/
│
├── sentiment/
│   └── finbert_analysis.py
│
├── data/
│   └── finbert_analyzed_news.csv
│
├── app.py
├── requirements.txt
└── README.md
```

> The exact structure may vary depending on the latest version of the project.

---

## 📈 Project Impact

The project was designed to improve the efficiency of financial research by automating several traditionally manual processes.

### Reported Results

| Metric          |          Improvement |
| --------------- | -------------------: |
| Research Time   |   **~80% reduction** |
| Portfolio Gains | **~15% improvement** |

These results demonstrate the potential of combining **NLP-based sentiment analysis with AI-powered financial insights** to support investment research.

> Results depend on the underlying dataset, market conditions, strategy, and evaluation methodology. They should not be interpreted as a guarantee of future investment performance.

---

## 🔐 API Configuration

API keys should **never be hardcoded** into the source code.

Create environment variables for your API credentials:

```env
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Then access them securely within Python:

```python
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
```

Make sure `.env` files are included in `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/financial-sentiment-analysis.git

cd financial-sentiment-analysis
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file and add the required API credentials.

### 5. Run the Application

```bash
python app.py
```

Then open the local web application in your browser.

---

## 🧪 Example Workflow

A typical analysis follows this process:

```text
Financial News
      ↓
"Company reports stronger-than-expected earnings"
      ↓
FinBERT
      ↓
Positive Sentiment
      ↓
Market Data
      ↓
AI Analysis
      ↓
Potential Market Insight
```

This approach allows the system to move beyond simply classifying news and instead provide **contextual financial analysis**.

---

## 🔮 Future Improvements

Potential improvements include:

* Real-time market monitoring
* Automated portfolio tracking
* More advanced stock prediction models
* Time-series forecasting
* Technical indicator integration
* Automated trading strategy backtesting
* Sentiment trend dashboards
* More financial news sources
* Real-time alerts
* User authentication
* Portfolio risk analysis
* Cloud deployment
* Database migration from CSV to PostgreSQL
* Improved model evaluation and benchmarking

---

## ⚠️ Disclaimer

This project is intended for **educational, research, and analytical purposes only**.

The information generated by the system should **not be considered professional financial or investment advice**. Financial markets are inherently unpredictable, and past performance does not guarantee future results.

Users should conduct their own research and consult qualified financial professionals before making investment decisions.

---

## 👨‍💻 Author

**Danish Azizi**

Computer Science Graduate — Data Science

Interested in:

* Data Science
* Artificial Intelligence
* Financial Technology
* Machine Learning
* NLP
* Automation
* Financial Analytics

---

## ⭐ If You Find This Project Interesting

Feel free to ⭐ star the repository, explore the code, or use the project as inspiration for your own **AI + Finance** applications.
