import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import random
from config import API_TOKEN
from keyboards import inline_keyboard

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инлайн-кнопки для генерации случайных чисел

# Состояние для хранения диапазона
user_ranges = {}


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Выберите действие для генерации случайных чисел:",
        reply_markup=inline_keyboard
    )


# Обработчик нажатий на инлайн-кнопки
@dp.callback_query(lambda callback_query: True)
async def handle_callback_query(callback_query: CallbackQuery):
    # Генерация случайного числа от 1 до 100
    if callback_query.data == "random_1_100":
        random_number = random.randint(1, 100)
        await callback_query.message.answer(f"Случайное число от 1 до 100: {random_number}")
        await callback_query.answer()

    # Установка диапазона для генерации
    elif callback_query.data == "set_range":
        await callback_query.message.answer("Введите диапазон чисел в формате 'min-max' (например: 10-50):")
        await callback_query.answer()

    # Генерация 5 случайных чисел
    elif callback_query.data == "generate_five":
        random_numbers = [random.randint(1, 100) for _ in range(5)]
        random_numbers_str = ', '.join(map(str, random_numbers))
        await callback_query.message.answer(f"Сгенерированные числа: {random_numbers_str}")
        await callback_query.answer()


# Обработчик текстовых сообщений для установки диапазона
@dp.message()
async def handle_set_range(message: types.Message):
    if '-' in message.text:
        try:
            min_val, max_val = map(int, message.text.split('-'))
            if min_val >= max_val:
                await message.answer("Минимальное число должно быть меньше максимального.")
                return

            random_number = random.randint(min_val, max_val)
            await message.answer(f"Случайное число в диапазоне {min_val}–{max_val}: {random_number}")
        except ValueError:
            await message.answer("Пожалуйста, введите корректные числа в формате 'min-max'.")
    else:
        await message.answer("Введите диапазон в формате 'min-max'.")


if __name__ == '__main__':
    # Запуск бота
    asyncio.run(dp.start_polling(bot))
