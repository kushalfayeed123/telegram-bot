import os


# Telegram API Configuration
API_ID = 20013934
API_HASH = 'b1709a3a9e8303f5a29ccefd896d883b'

PHONE = '+2348032542506'
TARGET_GROUP = -4628265139

# Technical Analysis Parameters
SHORT_PERIOD = 50
LONG_PERIOD = 200

# Assets Configuration
ASSETS = [
    {"type": "stock", "symbol": "AAPL"},
    {"type": "stock", "symbol": "MSFT"},
    {"type": "stock", "symbol": "GOOGL"},
    {"type": "stock", "symbol": "AMZN"},
    {"type": "stock", "symbol": "TSLA"},
    {"type": "crypto", "symbol": "BTC-USD", "investment_style": "aggressive"},
    {"type": "crypto", "symbol": "ETH-USD", "investment_style": "aggressive"},
    {"type": "crypto", "symbol": "BNB-USD", "investment_style": "aggressive"},
    {"type": "crypto", "symbol": "XRP-USD", "investment_style": "aggressive"},
    {"type": "crypto", "symbol": "ADA-USD", "investment_style": "aggressive"},
    {"type": "crypto", "symbol": "DOGE-USD", "investment_style": "aggressive"},
    {"type": "crypto", "symbol": "SOL-USD", "investment_style": "aggressive"},
    {"type": "option", "underlying": "AAPL", "option_type": "call", "strike": 150, "expiry": "2025-06-20"},
    {"type": "option", "underlying": "MSFT", "option_type": "put", "strike": 280, "expiry": "2025-09-20"},
    {"type": "option", "underlying": "TSLA", "option_type": "call", "strike": 700, "expiry": "2025-03-15"}
]

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds