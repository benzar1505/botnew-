import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode
from aiogram.filters import Command
from aiohttp import web
from keep_alive import keep_alive  # Запуск Flask-сервера для Heroku

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

# Заявка
@dp.message_handler(lambda message: message.text == "✍️ Заповнити заявку")
async def fill_request(message: types.Message):
    await message.answer(
        "📩 Заповніть форму заявки, і ми з вами зв'яжемося найближчим часом!\n\n"
        "❓ Ваше ім'я:\n"
        "📞 Ваш номер телефону або Telegram акаунт:\n"
        "🔹 Бажана послуга:\n"
        "💬 Ваше питання:\n"
        "Напишіть ці деталі, і ми обов'язково вам допоможемо.",
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

# Функція для налаштування webhook
async def set_webhook():
    url = "https://your-heroku-app-name.herokuapp.com/"  # Замість цього вставте ваш URL
    await bot.set_webhook(url)

# Обробка запитів по webhook
async def on_start(request):
    return web.Response(text="Bot is running")

# Налаштовуємо веб-сервер
app = web.Application()
app.router.add_get("/", on_start)

# Запуск webhook і веб-сервера
async def on_start():
    await bot.set_webhook("https://your-heroku-app-name.herokuapp.com/")  # Замість цього вставте ваш URL
    return web.Response(text="Bot is running")

# Запуск веб-сервера
if __name__ == "__main__":
    keep_alive()  # Підтримка роботи Heroku
    web.run_app(app, port=os.getenv('PORT'))