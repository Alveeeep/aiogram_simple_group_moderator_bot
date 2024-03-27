import asyncio
import contextlib
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

from middleware.db import DataBaseSession
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_get_messages, orm_add_message, orm_get_message_state, orm_update_message_state, \
    orm_delete_message

load_dotenv()

from database.engine import create_db, session_maker

bot = Bot(os.getenv("BOT_TOKEN"))  # make .env file with bot token
dp = Dispatcher()

logger = logging.getLogger(__name__)

ALLOWED_UPDATES = ['message, edited_message']


async def on_startup(bot):
    await create_db()


async def on_shutdown(bot):
    print('бот лег')


# When leaving this period of time, the bot will respond to messages
@dp.message((~(6 <= F.date.hour < 15) & F.text.contains("?")) & F.sender_chat.is_(None))
async def message_after_18(message: Message):
    await message.answer(
        "Здравствуйте! Спасибо за вопрос. Наши специалисты ответят на него в рабочее время: Пн - Пт с 9 до 18 по МСК.")


async def check_for_admin_reply(message: Message, session: AsyncSession):
    await asyncio.sleep(300)  # Wait for 5 minutes
    # Check if the message has been replied to by an admin
    if await orm_get_message_state(message.message_id, session) is False:
        # If not replied, send a template message
        await message.answer("Template message")
        await orm_delete_message(message.message_id, session)


@dp.message((6 <= F.date.hour < 15) & F.text.contains("?"))
async def wait_on_answer(message: Message, session: AsyncSession):
    if message.chat.type in ['group', 'supergroup']:
        # Check if the sender is an admin
        user_status = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if user_status.status not in ['creator', 'administrator']:
            # If the sender is not an admin, store the message and start the check
            await orm_add_message(message.message_id, False, session)
            asyncio.create_task(check_for_admin_reply(message.message_id, session))
        else:
            # If the sender is an admin, mark the previous message as replied
            replied_message_id = message.reply_to_message.message_id
            if replied_message_id in await orm_get_messages(session):
                await orm_update_message_state(replied_message_id, True, session)


async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s")
    logger.info("Starting bot...")
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
