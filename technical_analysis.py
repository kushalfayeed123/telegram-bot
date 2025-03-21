import yfinance as yf
import numpy as np
import pandas_ta as ta

def fetch_stock_data(symbol):
    """Fetch historical stock data from Yahoo Finance."""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="6mo")
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_technical_indicators(data):
    """Calculate key technical indicators."""
    if data is None or data.empty:
        return None

    data['SMA_50'] = ta.SMA(data['Close'], timeperiod=50)
    data['SMA_200'] = ta.SMA(data['Close'], timeperiod=200)
    data['RSI'] = ta.RSI(data['Close'], timeperiod=14)
    macd, signal, _ = ta.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    data['MACD'] = macd
    data['Signal_Line'] = signal

    return data.iloc[-1]  # Return the latest indicators

def analyze_stock_crypto(symbol, investment_style="moderate"):
    """Analyze stock or crypto based on technical indicators."""
    data = fetch_stock_data(symbol)
    indicators = calculate_technical_indicators(data)

    if indicators is None:
        return None, None

    message = f"Asset: {symbol}\nCurrent Price: ${data['Close'].iloc[-1]:.2f}\n"
    message += f"50-day SMA: ${indicators['SMA_50']:.2f}\n"
    message += f"200-day SMA: ${indicators['SMA_200']:.2f}\n"
    message += f"RSI: {indicators['RSI']:.2f}\n"
    message += f"MACD: {indicators['MACD']:.2f} vs Signal: {indicators['Signal_Line']:.2f}\n"
    
    # Determine trend and recommendation
    if indicators['SMA_50'] > indicators['SMA_200'] and indicators['RSI'] < 70:
        message += "Recommendation: Strong Buy - Uptrend confirmed.\n"
    elif indicators['SMA_50'] < indicators['SMA_200'] and indicators['RSI'] > 30:
        message += "Recommendation: Hold - Await better entry.\n"
    else:
        message += "Recommendation: Sell - Downtrend risk high.\n"

    return message, data['Close'].iloc[-1]

def analyze_option_detailed(option_data):
    """Placeholder function for option analysis."""
    return "Option analysis not implemented.", None
