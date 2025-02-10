import logging
import asyncio
import os
import signal
from aiogram import Bot, Dispatcher, types, Router, F
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

# Підменю послуг
services_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚗 Разовий огляд авто")],
        [KeyboardButton(text="🎯 Експерт на день")],
        [KeyboardButton(text="🏪 Супровід на авторинку")],
        [KeyboardButton(text="🔑 Підбір авто 'Під ключ'")],
        [KeyboardButton(text="🔙 Назад")],
    ],
    resize_keyboard=True
)

# **Привітання перед натисканням /start**
@router.message(F.text)
async def welcome_message(message: types.Message):
    if message.text.lower() not in ["/start", "старт"]:
        await message.answer(
            "🚗 Вітаємо у <b>AutoScout Kyiv</b>!\n\n"
            "Я допоможу вам знайти ідеальне авто! Натисніть /start для початку роботи."
        )

# Команда /start
@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "🚗 Привіт! Я бот сервісу <b>AutoScout Kyiv</b>. Я допоможу вам знайти ідеальне авто! \n\n"
        "Оберіть команду в меню або напишіть 'Допомога' для перегляду всіх можливостей.",
        reply_markup=main_menu
    )

# Відкриття підменю послуг
@router.message(F.text == "📋 Послуги")
async def show_services_menu(message: types.Message):
    await message.answer("🛠 Оберіть послугу:", reply_markup=services_menu)

# Назад до головного меню
@router.message(F.text == "🔙 Назад")
async def go_back(message: types.Message):
    await message.answer("🔙 Ви повернулись у головне меню.", reply_markup=main_menu)

# **Разовий огляд авто**
@router.message(F.text == "🚗 Разовий огляд авто")
async def service_one_time_check(message: types.Message):
    await message.answer(
        "🚗 <b>РАЗОВИЙ ОГЛЯД АВТО – 1500₴</b>\n\n"
        "🔹 Перевірка кузова та ЛФП\n"
        "🔹 Первинна перевірка технічного стану\n"
        "🔹 Загальна оцінка стану авто\n"
        "🔹 Комп’ютерна діагностика\n"
        "🔹 Тест-драйв\n"
        "🔹 Перевірка документів\n"
        "🔹 Фото/відео звіт"
    )

# **Експерт на день**
@router.message(F.text == "🎯 Експерт на день")
async def service_expert_day(message: types.Message):
    await message.answer(
        "🎯 <b>ЕКСПЕРТ НА ДЕНЬ – 4000₴</b>\n\n"
        "🔍 Перевіряємо до 5 авто за день\n"
        "🔹 Перевірка кузова та ЛФП\n"
        "🔹 Первинна перевірка технічного стану\n"
        "🔹 Загальна оцінка стану\n"
        "🔹 Комп’ютерна діагностика\n"
        "🔹 Перевірка документів\n"
        "🔹 Тест-драйв"
    )

# **Супровід на авторинку**
@router.message(F.text == "🏪 Супровід на авторинку")
async def service_market_assistance(message: types.Message):
    await message.answer(
        "🏪 <b>СУПРОВІД НА АВТОРИНКУ – 3000₴</b>\n\n"
        "📍 Разом з вами оглядаємо авто на авторинку\n"
        "🔹 Перевірка кузова та ЛФП\n"
        "🔹 Первинна перевірка технічного стану\n"
        "🔹 Загальна оцінка стану\n"
        "🔹 Комп’ютерна діагностика\n"
        "🔹 Перевірка за базами (1 авто)\n"
        "🔹 Перевірка на СТО (1 авто)\n"
        "🔹 Тест-драйв"
    )

# **Підбір авто "Під ключ"**
@router.message(F.text == "🔑 Підбір авто 'Під ключ'")
async def service_full_selection(message: types.Message):
    await message.answer(
        "🔑 <b>ПІДБІР АВТО “ПІД КЛЮЧ”</b>\n\n"
        "✅ Пошук авто під ваш бюджет та вимоги\n"
        "✅ Перевірка кузова та ЛФП\n"
        "✅ Первинна перевірка технічного стану\n"
        "✅ Загальна оцінка стану\n"
        "✅ Комп’ютерна діагностика\n"
        "✅ Перевірка документів\n"
        "✅ Перевірка за базами + перевірка на СТО\n"
        "✅ Тест-драйв\n"
        "✅ Фото/відео звіт\n\n"
        "💰 Вартість підбору обговорюється індивідуально."
    )

# Підключаємо Router до Dispatcher
dp.include_router(router)

# Функція для обробки сигналу завершення
def handle_exit(*args):
    logging.warning("Бот вимикається...")
    asyncio.create_task(bot.session.close())
    asyncio.sleep(5)
    logging.warning("Бот вимкнено.")

# Функція запуску бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    keep_alive()  # Підтримка роботи Heroku
    signal.signal(signal.SIGTERM, handle_exit)  # Додано для обробки завершення
    asyncio.run(main())