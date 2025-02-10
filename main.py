import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from keep_alive import keep_alive  # Запуск Flask-сервера для Heroku

# Отримання токена
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("❌ API_TOKEN не знайдено! Додайте токен у змінні середовища.")

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Створюємо Router
router = Router()

# Головне меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Послуги"), KeyboardButton(text="✍️ Залишити заявку")],
        [KeyboardButton(text="📞 Контакти"), KeyboardButton(text="❓ Допомога")],
    ],
    resize_keyboard=True
)

# Команда /start
@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "🚗 Привіт! Я бот сервісу <b>AutoScout Kyiv</b>. Я допоможу вам знайти ідеальне авто! \n\n"
        "Оберіть команду в меню або напишіть 'Допомога' для перегляду всіх можливостей.",
        reply_markup=main_menu
    )

# Послуги
@router.message(lambda message: message.text == "📋 Послуги")
async def show_services(message: types.Message):
    await message.answer(
        "🛠 <b>Наші послуги:</b>\n\n"
        "🔹 Разовий огляд авто\n"
        "🔹 Підбір авто 'під ключ'\n"
        "🔹 Експерт на день\n"
        "🔹 Супровід на авторинку\n"
        "🔹 Перевірка документів\n"
        "🔹 Перевірка на СТО\n"
        "🔹 Фото/відео звіт"
    )

# Заявка
@router.message(lambda message: message.text == "✍️ Залишити заявку")
async def send_request_info(message: types.Message):
    await message.answer(
        "📩 Для оформлення заявки напишіть нам у <a href='https://t.me/autoscout_kyiv'>Telegram</a> або зателефонуйте."
    )

# Контакти
@router.message(lambda message: message.text == "📞 Контакти")
async def send_contacts(message: types.Message):
    await message.answer(
        "📞 <b>Контакти:</b>\n"
        "📲 Телефон: +380 (73) 933 77 97\n"
        "📍 Київ\n\n"
        "🔹 <a href='https://t.me/autoscout_kyiv'>Telegram</a>\n"
        "🔹 <a href='https://instagram.com/autoscout_kyiv'>Instagram</a>\n"
        "🔹 <a href='https://autoscout.neocities.org/'>Наш сайт</a>"
    )

# Допомога
@router.message(lambda message: message.text == "❓ Допомога")
async def send_help(message: types.Message):
    await message.answer(
        "❓ <b>Доступні команди:</b>\n"
        "📋 Послуги — переглянути наші послуги\n"
        "✍️ Залишити заявку — як зробити замовлення\n"
        "📞 Контакти — телефон, Telegram, Instagram, сайт\n"
        "Якщо у вас є питання, звертайтеся!"
    )

# Підключаємо Router до Dispatcher
dp.include_router(router)

# Функція запуску бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    keep_alive()  # Підтримка роботи Heroku
    asyncio.run(main())