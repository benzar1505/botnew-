import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode
from aiogram.filters import Command
from aiohttp import web

# Логування
logging.basicConfig(level=logging.INFO)

# Отримання токена
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")

if not API_TOKEN:
    raise ValueError("❌ API_TOKEN не знайдено! Додайте токен у змінні середовища.")
if not HEROKU_APP_NAME:
    raise ValueError("❌ HEROKU_APP_NAME не знайдено! Додайте його у змінні середовища.")

# Ініціалізація бота та диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Головне меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Послуги"), KeyboardButton(text="✍️ Заповнити заявку")],
        [KeyboardButton(text="📞 Контакти"), KeyboardButton(text="❓ Допомога")],
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "🚗 Привіт! Я бот сервісу <b>AutoScout Kyiv</b>. Я допоможу вам знайти ідеальне авто! \n\n"
        "Оберіть команду в меню або напишіть 'Допомога' для перегляду всіх можливостей.",
        reply_markup=main_menu,
        parse_mode=ParseMode.HTML
    )

# Обробка Webhook
async def handle_webhook(request):
    update = await request.json()
    await dp.feed_update(bot, update)
    return web.Response(text="OK")

# Налаштування веб-сервера
async def on_startup(app):
    webhook_url = f"https://{HEROKU_APP_NAME}.herokuapp.com/"
    logging.info(f"Встановлення webhook: {webhook_url}")
    await bot.set_webhook(webhook_url)

app = web.Application()
app.router.add_post("/", handle_webhook)
app.on_startup.append(on_startup)

# Запуск веб-сервера
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Запуск веб-сервера на порті {port}")
    web.run_app(app, host="0.0.0.0", port=port)
