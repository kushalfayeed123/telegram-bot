import logging
import datetime

def setup_logging():
    """Configures logging settings."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

def get_formatted_time():
    """Returns the current time as a formatted string."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_error_message(asset_symbol, error):
    """Formats error messages for logging and notifications."""
    return f"[ERROR] {get_formatted_time()} - {asset_symbol}: {str(error)}"
