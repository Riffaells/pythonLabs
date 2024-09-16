# Лабораторная работа №3

## Telegram-бота с генерацией случайных чисел

 
**Цель работы**: Этот проект представляет собой простого Telegram-бота, который генерирует случайные числа с помощью инлайн-кнопок. Бот разработан с использованием библиотеки aiogram и позволяет пользователям:

- Сгенерировать случайное число в диапазоне от 1 до 100.
- Указать свой диапазон чисел для генерации.
- Сгенерировать 5 случайных чисел одновременно.
 
## ТЕОРЕТИЧЕСКАЯ ЧАСТЬ
### Настройка бота

Создайте файл `config.py` в корневой директории проекта и добавьте туда токен вашего бота, который вы получите у BotFather:

---
## Основной код бота разделен на два файла:

    bot.py — основной файл с логикой работы бота.
    keyboards.py — файл с конфигурацией инлайн-клавиатур.

```python
# config.py
API_TOKEN = 'ваш_токен_здесь'
```

## keyboard.py

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Создаем инлайн-клавиатуру
inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Случайное число от 1 до 100", callback_data="random_1_100")],
        [InlineKeyboardButton(text="Случайное число в диапазоне (задать диапазон)", callback_data="set_range")],
        [InlineKeyboardButton(text="Генерировать 5 чисел", callback_data="generate_five")]
    ]
)
```

Описание:

- Инлайн-клавиатура: Создаётся с тремя кнопками:
  - "Случайное число от 1 до 100": Генерирует случайное число в этом диапазоне.
  - "Случайное число в диапазоне (задать диапазон)": Позволяет пользователю задать свой диапазон.
  - "Генерировать 5 чисел": Генерирует сразу 5 случайных чисел.

## bot.py

```python
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

# Состояние для хранения диапазона
user_ranges = {}

```

Описание:

- Логирование: Устанавливается базовый уровень логирования для отображения информации.
- Инициализация бота: Бот и диспетчер инициализируются с использованием токена, который хранится в файле config.py.
- Переменная user_ranges: Словарь для хранения диапазонов чисел, введённых пользователями (если необходимо добавить функционал для каждого пользователя).



## Обработчики команд и инлайн-кнопок
Команда `/start`

```python

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Выберите действие для генерации случайных чисел:",
        reply_markup=inline_keyboard
    )
```

Описание:

- Этот обработчик реагирует на команду `/start`.
- После получения команды бот отправляет сообщение с предложением выбрать действие для генерации чисел. Сообщение сопровождается инлайн-клавиатурой, которая импортируется из файла `keyboards.py`.


## Обработка инлайн-кнопок

```python
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

```

Описание:

 - Обработчик нажатий на инлайн-кнопки:
    -  Этот обработчик обрабатывает все нажатия на инлайн-кнопки.
    -  Генерация случайного числа от 1 до 100: Если пользователь нажимает на кнопку с callback_data="random_1_100", бот генерирует и отправляет случайное число от 1 до 100.
    -  Задание диапазона: Если пользователь выбирает кнопку set_range, бот просит пользователя ввести диапазон чисел в формате min-max.
    -  Генерация 5 случайных чисел: При выборе кнопки generate_five, бот генерирует 5 случайных чисел от 1 до 100 и отправляет их пользователю.

## Обработка текстовых сообщений для диапазона

```python
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

```


Описание:

 - Когда пользователь вводит текстовый диапазон чисел (например, 10-50), бот проверяет правильность формата:
    - Если формат правильный, бот генерирует случайное число в указанном диапазоне.
    - Если диапазон некорректен (например, минимальное число больше максимального), бот отправляет ошибку.
    - Если ввод неверный, бот просит ввести корректные данные.








