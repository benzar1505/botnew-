import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Токен бота
API_TOKEN = os.getenv('BOT_API_TOKEN')

# Ініціалізація бота та диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Обробник стартової команди
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Це бот, створений за допомогою aiogram.")

# Обробник текстових повідомлень
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

# Функція для запуску бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
