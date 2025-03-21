import asyncio
import logging
from telethon import TelegramClient
from datetime import datetime
from config import API_ID, API_HASH, PHONE, TARGET_GROUP, MAX_RETRIES, RETRY_DELAY

class TradingBot:
    def __init__(self):
        self.client = None
        self.logger = logging.getLogger(__name__)

    async def handle_code_callback(self):
        """Prompt the user to enter the Telegram verification code."""
        loop = asyncio.get_running_loop()
        code = await loop.run_in_executor(None, input, "Enter the Telegram verification code: ")
        return code.strip()

    async def connect(self):
        """Initialize and connect the Telegram client."""
        try:
            self.client = TelegramClient('user_message_bot.session', API_ID, API_HASH)
            await self.client.start(phone=PHONE, code_callback=self.handle_code_callback)
            async for dialog in self.client.iter_dialogs():
                print(f"Name: {dialog.name}, ID: {dialog.id}")

            # Get user information with proper error handling
            try:
                me = await self.client.get_me()
                if me:
                    username_str = f" (@{me.username})" if me.username else ""
                    self.logger.info(f"Logged in as: {me.first_name}{username_str}")
                else:
                    self.logger.warning("Connected but couldn't get user information")
            except Exception as e:
                self.logger.error(f"Error getting user information: {str(e)}")
                return False

            return bool(self.client and self.client.is_connected())
        except Exception as e:
            self.logger.error(f"Failed to connect to Telegram: {str(e)}")
            return False

    async def send_message_with_retry(self, message):
        """Send a message to the target group with retry logic."""
        for attempt in range(MAX_RETRIES):
            try:
                if not self.client or not self.client.is_connected():
                    if not await self.connect():
                        self.logger.error("Failed to establish connection")
                        continue
         
                await self.client.send_message(TARGET_GROUP, message)
                self.logger.info("Message sent successfully")
                print("Sent message:\n", message)
                return True
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    self.logger.error("Max retries reached. Message not sent.")
                    return False

    async def disconnect(self):
        """Disconnect the Telegram client."""
        if self.client:
            await self.client.disconnect()
            self.logger.info("Disconnected from Telegram")