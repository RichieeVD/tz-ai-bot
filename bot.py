import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import db
from gpt_service import get_chatgpt_response

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_KEY")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Новый запрос")
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    db.reset_context(message.from_user.id)
    await message.answer(
        "Привет! Контекст диалога сброшен. Напиши свой вопрос, и я отвечу с помощью ChatGPT.",
        reply_markup=get_main_keyboard()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Бот использует API ChatGPT для генерации ответов.\n\n"
        "1. Просто пиши сообщения, чтобы общаться.\n"
        "2. Бот помнит историю сообщений внутри текущего диалога.\n"
        "3. Нажми 'Новый запрос' или введи /start, чтобы бот всё забыл."
    )

@dp.message(F.text == "Новый запрос")
async def handle_reset_button(message: types.Message):
    db.reset_context(message.from_user.id)
    await message.answer("История очищена. О чем хочешь поговорить?")

@dp.message()
async def handle_user_message(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text

    # Сохраняем сообщение пользователя в базу
    db.add_message(user_id, "user", user_text)

    # Получаем всю историю переписки (контекст)
    context = db.get_context(user_id)

    # Отправляем статус "печатает"
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # Получаем ответ от ИИ (передаем весь контекст)
    response_text = await get_chatgpt_response(context)

    # Сохраняем ответ бота в базу
    db.add_message(user_id, "assistant", response_text)

    await message.answer(response_text)

async def main():
    # Запуск бота
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")