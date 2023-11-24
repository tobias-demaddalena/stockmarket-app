import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Alpha Vantage API key - replace with your own
api_key = 'VLLKN713GQBQYOUW'

def get_stock_data(ticker, start_date, end_date):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}&outputsize=full"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        time_series = data.get('Time Series (Daily)', {})
        # Filter data based on the specified date range
        filtered_data = {date: values for date, values in time_series.items() if start_date <= date <= end_date}
        return filtered_data
    else:
        st.error(f"Failed to retrieve data for {ticker}: {response.text}")
        return None

def calculate_volatility(closing_prices):
    # Calculate the daily returns
    returns = np.diff(closing_prices) / closing_prices[:-1]
    # Volatility is the standard deviation of daily returns
    return np.std(returns)

def plot_stock_data(stock_data, ticker):
    dates = []
    closing_prices = []

    for date, daily_data in sorted(stock_data.items()):
        dates.append(datetime.strptime(date, '%Y-%m-%d'))
        closing_prices.append(float(daily_data['4. close']))

    plt.figure(figsize=(10, 6))
    plt.plot(dates, closing_prices, marker='o', label=f'{ticker} Closing Price')
    plt.title(f'Stock Performance: {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    return plt, closing_prices

def calculate_performance(closing_prices):
    if closing_prices:
        performance = ((closing_prices[-1] - closing_prices[0]) / closing_prices[0]) * 100
        return round(performance, 2)
    return 0

st.title("Stock Performance Tracker")

ticker = st.text_input("Enter stock ticker symbol (e.g., AAPL)")
start_date = st.text_input("Enter start date (YYYY-MM-DD)")
end_date = st.text_input("Enter end date (YYYY-MM-DD)")

if st.button("Show Stock Data"):
    stock_data = get_stock_data(ticker, start_date, end_date)
    if stock_data:
        fig, closing_prices = plot_stock_data(stock_data, ticker)
        st.pyplot(fig)

        current_price = closing_prices[-1]
        volatility = calculate_volatility(closing_prices)
        performance = calculate_performance(closing_prices)

        st.write(f"**Current Price:** ${current_price}")
        st.write(f"**Volatility:** {volatility * 100:.2f}%")
        st.write(f"**Performance:** {performance}%")

