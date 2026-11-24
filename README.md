# QuantumPulse – High-Frequency Financial Data Density Engine

## Project Overview
QuantumPulse is a financial analytics dashboard developed using Python. It helps users explore stock market data, compare stock prices, analyze financial statistics, and store financial records using SQLite.

## Features
- Stock data selection
- Financial data visualization
- Stock price comparison
- Advanced financial analytics
- SQLite database integration
- CSV data download
- Interactive dashboard using Streamlit

## Technologies Used
- Python
- Streamlit
- Polars
- Plotly
- SQLite
- Yahoo Finance (yfinance)

## Project Structure
```text
QuantumPulse/
├── app.py
├── processor.py
├── data_generator.py
├── database.py
├── live_stock.py
├── save_live_data.py
├── check_database.py
├── requirements.txt
├── README.md
└── data/
    ├── financial_data.csv
    └── quantumpulse.db
```

## How to Run
1. Install the required packages:
   `pip install -r requirements.txt`
2. Run the dashboard:
   `python -m streamlit run app.py`
3. Open the local dashboard in your browser.

## Project Outcome
QuantumPulse provides an interactive platform for stock data visualization, financial analysis, comparison, and database management.
