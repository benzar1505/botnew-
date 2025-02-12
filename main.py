import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Отримання токена
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("❌ API_TOKEN не знайдено! Додайте токен у змінні середовища.")

# ID адміна
ADMIN_ID = 7858563425  

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Створюємо меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Послуги"), KeyboardButton(text="📝 Заповнити заявку")],
        [KeyboardButton(text="📞 Контакти"), KeyboardButton(text="❓ Допомога")],
    ],
    resize_keyboard=True
)

# Стан для заявки
class RequestForm(StatesGroup):
    name = State()
    contact = State()
    service = State()
    question = State()

# Команда /start
@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "🚗 Привіт! Я бот сервісу <b>AutoScout Kyiv</b>. Я допоможу вам знайти ідеальне авто!\n\n"
        "Оберіть команду в меню або напишіть 'Допомога' для перегляду всіх можливостей.",
        reply_markup=main_menu,
        parse_mode=ParseMode.HTML
    )

# Послуги
@router.message(F.text == "📋 Послуги")
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
@router.message(F.text == "📞 Контакти")
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
@router.message(F.text == "❓ Допомога")
async def send_help(message: types.Message):
    await message.answer(
        "❓ <b>Доступні команди:</b>\n"
        "📋 Послуги — переглянути наші послуги\n"
        "📝 Заповнити заявку — відправити заявку на підбір авто\n"
        "📞 Контакти — телефон, Telegram, Instagram, сайт\n"
        "Якщо у вас є питання, звертайтеся!",
        parse_mode=ParseMode.HTML
    )

# --- Форма заявки ---
@router.message(F.text == "📝 Заповнити заявку")
async def request_start(message: types.Message, state: FSMContext):
    await state.set_state(RequestForm.name)
    await message.answer("📝 Введіть ваше ім'я:")

@router.message(RequestForm.name)
async def request_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RequestForm.contact)
    await message.answer("📞 Введіть ваш номер телефону або Telegram-нік:")

@router.message(RequestForm.contact)
async def request_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(RequestForm.service)
    await message.answer("🔹 Оберіть послугу:\n\n"
                         "1️⃣ Разовий огляд авто\n"
                         "2️⃣ Підбір авто 'під ключ'\n"
                         "3️⃣ Експерт на день\n"
                         "4️⃣ Супровід на авторинку\n"
                         "5️⃣ Перевірка документів\n"
                         "6️⃣ Перевірка на СТО\n"
                         "7️⃣ Фото/відео звіт\n\n"
                         "Напишіть номер або назву послуги.")

@router.message(RequestForm.service)
async def request_service(message: types.Message, state: FSMContext):
    await state.update_data(service=message.text)
    await state.set_state(RequestForm.question)
    await message.answer("❓ Введіть ваше питання або уточнення:")

@router.message(RequestForm.question)
async def request_question(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    
    # Формуємо текст заявки
    request_text = (
        f"📩 <b>Нова заявка:</b>\n\n"
        f"👤 Ім'я: {user_data['name']}\n"
        f"📞 Контакт: {user_data['contact']}\n"
        f"🔹 Послуга: {user_data['service']}\n"
        f"❓ Питання: {message.text}"
    )
    
    # Надсилаємо адміну
    await bot.send_message(ADMIN_ID, request_text, parse_mode=ParseMode.HTML)
    
    # Дякуємо користувачу
    await message.answer("✅ Дякуємо! Ваша заявка відправлена, ми зв'яжемося з вами найближчим часом.")
    
    await state.clear()

# Підключаємо Router до Dispatcher
dp.include_router(router)

# Функція запуску бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())