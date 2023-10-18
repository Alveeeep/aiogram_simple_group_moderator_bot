import asyncio
import contextlib
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

load_dotenv()

bot = Bot(os.getenv("BOT_TOKEN")) # make .env file with bot token
dp = Dispatcher()

logger = logging.getLogger(__name__)


# When leaving this period of time, the bot will respond to messages
@dp.message(~(6 <= F.date.hour <= 15))
async def message_after_18(message: Message):
    await message.answer("Hello")


async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s")
    logger.info("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
