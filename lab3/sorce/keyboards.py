from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Создаем инлайн-клавиатуру
inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Случайное число от 1 до 100", callback_data="random_1_100")],
        [InlineKeyboardButton(text="Случайное число в диапазоне (задать диапазон)", callback_data="set_range")],
        [InlineKeyboardButton(text="Генерировать 5 чисел", callback_data="generate_five")]
    ]
)
