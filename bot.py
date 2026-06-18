import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import logging
from setting import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {user_id} нажал /start")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (telegram_id) VALUES (?)", (user_id,))
        conn.commit()
        await message.answer("Вы успешно подписаны на рассылку новостей!")
        logging.info(f"Пользователь {user_id} добавлен в базу данных.")
    except sqlite3.IntegrityError:
        await message.answer("Вы уже подписаны на рассылку!")
        logging.warning(f"Пользователь {user_id} попытался подписаться повторно.")
    finally:
        conn.close()


async def main():
    import database
    database.init_db()
    logging.info("Бот успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())