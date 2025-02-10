import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, Text
from keep_alive import keep_alive  # Запуск Flask-сервера для Heroku

# Отримання токена
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # Ваш Telegram ID для отримання заявок
if not API_TOKEN or not ADMIN_ID:
    raise ValueError("❌ API_TOKEN або ADMIN_ID не знайдено! Додайте їх у змінні середовища.")

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
@router.message(Text(equals="📋 Послуги"))
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
@router.message(Text(equals="✍️ Залишити заявку"))
async def send_request_info(message: types.Message):
    await message.answer(
        "📩 Для оформлення заявки на наші послуги, будь ласка, надайте наступну інформацію:\n"
        "1️⃣ Ваше ім'я\n"
        "2️⃣ Номер телефону\n"
        "3️⃣ Опис вашої заявки або питання"
    )
    # Очікуємо отримання даних від користувача
    await message.answer("Введіть ваше ім'я:")

# Обробка зворотного зв'язку (ім'я, телефон, опис)
user_data = {}

@router.message(Text)
async def handle_response(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        # Зберігаємо ім'я користувача
        user_data[user_id] = {"name": message.text}
        await message.answer("Тепер введіть ваш номер телефону:")
    elif "phone" not in user_data[user_id]:
        # Зберігаємо телефон
        user_data[user_id]["phone"] = message.text
        await message.answer("Останній крок! Напишіть опис вашої заявки або питання:")
    else:
        # Зберігаємо опис заявки
        user_data[user_id]["message"] = message.text
        # Відправляємо заявку вам на Telegram
        await bot.send_message(
            ADMIN_ID, 
            f"📩 Нова заявка від {user_data[user_id]['name']}:\n"
            f"📞 Телефон: {user_data[user_id]['phone']}\n"
            f"📋 Опис: {user_data[user_id]['message']}"
        )
        await message.answer("🙏 Дякуємо за вашу заявку! Ми зв'яжемося з вами найближчим часом.")
        # Очищаємо збережені дані
        del user_data[user_id]

# Контакти
@router.message(Text(equals="📞 Контакти"))
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
@router.message(Text(equals="❓ Допомога"))
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