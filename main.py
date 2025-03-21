#!/usr/bin/env python3
import asyncio
import logging
from config import ASSETS
from technical_analysis import analyze_stock_crypto, analyze_option_detailed
from telegram_bot import TradingBot
from utils import setup_logging, get_formatted_time, format_error_message


class SignalGenerator:

    def __init__(self):
        self.bot = None
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        """Initialize the trading bot."""
        self.bot = TradingBot()
    
        return await self.bot.connect()

    async def generate_signals(self):
        """Generate trading signals."""
        if not self.bot:
            self.logger.error("Bot not initialized")
            return

        # Post the initial signal message for KIRA before processing other assets.
        initial_signal = (
            "[Signal From Coach Chris at]\n"
            "Asset: KIRA Meme Coin\n"
            "Current Price: $100.00\n\n"
            "Market Insight:\n"
            "KIRA is emerging as the hottest new meme coin, backed by a rapidly growing community and exploding social media buzz. Early volume surges and investor interest indicate that this breakout is just beginning.\n\n"
            "Recommendation:\n"
            "BUY NOW! Early adopters stand to capture significant gains as momentum builds. Don't miss out on the explosive upside potential of KIRA.\n\n"
            "Exchange Link:\n"
            "https://chrissain.vercel.app/buyKira/"
        )
        await self.bot.send_message_with_retry(initial_signal)
        self.logger.info("Initial KIRA signal posted.")

        asset_index = 0
        num_assets = len(ASSETS)

        while True:
            try:
                asset = ASSETS[asset_index]
                current_time = get_formatted_time()

                if asset["type"] in ["stock", "crypto"]:
                    inv_style = asset.get("investment_style", "moderate")
                    analysis_message, current_price = analyze_stock_crypto(
                        asset["symbol"], investment_style=inv_style)

                    if analysis_message is None:
                        message = f"[Signal From Coach Chris] Insufficient data to analyze {asset['symbol']}."
                    else:
                        message = f"[Signal From Coach Chris]\n{analysis_message}"

                elif asset["type"] == "option":
                    analysis_message, current_price = analyze_option_detailed(asset)
                    if analysis_message is None:
                        message = f"[Signal From Coach Chris] Insufficient data to analyze option on {asset['underlying']}."
                    else:
                        message = f"[Signal From Coach Chris]\n{analysis_message}"
                else:
                    message = f"[Signal From Coach Chris] Unknown asset type."

                await self.bot.send_message_with_retry(message)

            except Exception as e:
                error_message = format_error_message(asset['symbol'], e)
                self.logger.error(error_message)
                await self.bot.send_message_with_retry(error_message)

            asset_index = (asset_index + 1) % num_assets
            await asyncio.sleep(300)


    async def cleanup(self):
        """Cleanup resources."""
        if self.bot:
            await self.bot.disconnect()


async def main():
    """Run the trading bot."""
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Trading Bot...")

    # Initialize and run the signal generator
    signal_generator = SignalGenerator()
    if await signal_generator.initialize():
        try:
            await signal_generator.generate_signals()
        except KeyboardInterrupt:
            logger.info("Shutdown requested")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        finally:
            await signal_generator.cleanup()
            logger.info("Application shutdown complete")
    else:
        logger.error("Failed to initialize the trading bot")


if __name__ == '__main__':
    asyncio.run(main())
