import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode
from aiogram.filters import Command
from aiohttp import web

# Отримання токена
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("❌ API_TOKEN не знайдено! Додайте токен у змінні середовища.")

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Створюємо головне меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Послуги"), KeyboardButton(text="✍️ Заповнити заявку")],
        [KeyboardButton(text="📞 Контакти"), KeyboardButton(text="❓ Допомога")],
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message_handler(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "🚗 Привіт! Я бот сервісу <b>AutoScout Kyiv</b>. Я допоможу вам знайти ідеальне авто! \n\n"
        "Оберіть команду в меню або напишіть 'Допомога' для перегляду всіх можливостей.",
        reply_markup=main_menu,
        parse_mode=ParseMode.HTML
    )

# Послуги
@dp.message_handler(lambda message: message.text == "📋 Послуги")
async def show_services(message: types.Message):
    await message.answer(
        "🛠 <b>Наші послуги:</b>\n\n"
        "🔹 Разовий огляд авто\n"
        "🔹 Підбір авто 'під ключ'\n"
        "🔹 Експерт на день\n"
        "🔹 Супровід на авторинку\n"
        "🔹 Перевірка документів\n"
        "🔹 Перевірка на СТО\n"
        "🔹 Фото/відео звіт",
        parse_mode=ParseMode.HTML
    )

# Контакти
@dp.message_handler(lambda message: message.text == "📞 Контакти")
async def send_contacts(message: types.Message):
    await message.answer(
        "📞 <b>Контакти:</b>\n"
        "📲 Телефон: +380 (73) 933 77 97\n"
        "📍 Київ\n\n"
        "🔹 <a href='https://t.me/autoscout_kyiv'>Telegram</a>\n"
        "🔹 <a href='https://instagram.com/autoscout_kyiv'>Instagram</a>\n"
        "🔹 <a href='https://autoscout.neocities.org/'>Наш сайт</a>",
        parse_mode=ParseMode.HTML
    )

# Допомога
@dp.message_handler(lambda message: message.text == "❓ Допомога")
async def send_help(message: types.Message):
    await message.answer(
        "❓ <b>Доступні команди:</b>\n"
        "📋 Послуги — переглянути наші послуги\n"
        "✍️ Заповнити заявку — як зробити замовлення\n"
        "📞 Контакти — телефон, Telegram, Instagram, сайт\n"
        "Якщо у вас є питання, звертайтеся!",
        parse_mode=ParseMode.HTML
    )

# Обробка webhook
async def handle_webhook(request):
    update = await request.json()
    await dp.feed_update(bot, update)
    return web.Response(text="OK")

# Налаштування веб-сервера
async def on_startup(app):
    webhook_url = f"https://{os.getenv('HEROKU_APP_NAME')}.herokuapp.com/"
    await bot.set_webhook(webhook_url)

app = web.Application()
app.router.add_post("/", handle_webhook)
app.on_startup.append(on_startup)

# Запуск
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    web.run_app(app, host="0.0.0.0", port=port)
