import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Логування
logging.basicConfig(level=logging.INFO)

# Отримання змінних середовища
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
PORT = int(os.getenv("PORT", 5000))  # Heroku передає PORT як змінну середовища

if not API_TOKEN or not HEROKU_APP_NAME:
    raise ValueError("❌ Помилка: TELEGRAM_BOT_TOKEN або HEROKU_APP_NAME не задано!")

# Ініціалізація бота та диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Клавіатура
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Послуги"), KeyboardButton(text="✍️ Заявка")],
        [KeyboardButton(text="📞 Контакти"), KeyboardButton(text="❓ Допомога")],
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "🚗 Привіт! Я бот сервісу <b>AutoScout Kyiv</b>. Я допоможу вам знайти авто! \n\n"
        "Оберіть команду в меню або напишіть 'Допомога' для перегляду всіх можливостей.",
        reply_markup=main_menu,
        parse_mode=types.ParseMode.HTML
    )

# Обробник для всіх повідомлень (наприклад, для кнопок)
@dp.message()
async def handle_message(message: types.Message):
    if message.text == "❓ Допомога":
        await message.answer(
            "📝 Ось всі можливості, які я можу виконати:\n\n"
            "1. 📋 Послуги - Перегляд наших послуг.\n"
            "2. ✍️ Заявка - Заповнення заявки на підбір авто.\n"
            "3. 📞 Контакти - Контакти нашого сервісу.\n"
            "4. ❓ Допомога - Перегляд цього списку."
        )
    elif message.text == "📋 Послуги":
        await message.answer("🚗 Наші послуги: \n- Підбір авто по вашим вимогам\n- Тест-драйв\n- Допомога з документами")
    elif message.text == "✍️ Заявка":
        await message.answer("📝 Заповніть заявку на підбір авто або залиште контактні дані.")
    elif message.text == "📞 Контакти":
        await message.answer("📞 Контакти сервісу: \nТелефон: +380123456789\nEmail: autoscoutkyiv@service.com")
    else:
        await message.answer("❓ Виберіть одну з кнопок в меню.")

# Webhook обробник
async def handle_webhook(request):
    update = await request.json()
    await dp.feed_update(bot, update)
    return web.Response(text="OK")

# Webhook підключення
async def on_startup(app):
    webhook_url = f"https://{HEROKU_APP_NAME}.herokuapp.com/"
    logging.info(f"🔗 Встановлення webhook: {webhook_url}")
    await bot.set_webhook(webhook_url)

# Очищення сесій при завершенні
async def on_cleanup(app):
    logging.info("Закриття сесії та з'єднання...")
    await bot.session.close()

# Запуск веб-сервера
app = web.Application()
app.router.add_post("/", handle_webhook)
app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

if __name__ == "__main__":
    logging.info(f"🚀 Запуск сервера на порту {PORT}")
    web.run_app(app, host="0.0.0.0", port=PORT)
