# Лабораторная работа №1 

## Программа для управления базой данных 

 
**Цель работы:** Создать простого Telegram-бота с использованием библиотеки `aiogram`, который будет реагировать на входящие сообщения и команды, выполняя эхо-функцию. Это позволит изучить основы взаимодействия с Telegram API, научиться обрабатывать события и сообщения, а также работать с библиотекой `aiogram` для создания ботов.
 
## ТЕОРЕТИЧЕСКАЯ ЧАСТЬ

### Добавление файла `config.py`

Для того чтобы ваш бот работал, вам нужно создать отдельный файл, где будет храниться токен бота. Это удобно для того, чтобы держать конфиденциальные данные отдельно от основного кода.

#### Cоздания файла `config.py`:

1. Создайте файл с именем `config.py` в корне вашего проекта.
2. Внутри этого файла нужно записать ваш токен, который вы получили через [BotFather](https://t.me/BotFather).
	1. Создайте нового бота с помощью команды `/newbot`.
	2. После создания бота BotFather предоставит вам токен — строку вида: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.
	3. Скопируйте этот токен и вставьте его в файл `config.py`.

config.py
```python
# Токен бота, который вы получили через BotFather
API_TOKEN = 'ваш_токен_здесь'
```

### Установка необходимых библиотек

Для работы с `Telegram` и создания бота с помощью `aiogram`, вам нужно установить библиотеку `aiogram`. Откройте терминал или командную строку и выполните команду:

```bash
pip install aiogram
```


### Создание эхо-бота

Теперь перейдём к созданию эхо-бота, который будет повторять любое сообщение, отправленное ему.

Cоздайте файл с именем `bot.py` в вашем проекте. В этом файле будет написана основная логика работы бота.

### Импортируйте необходимые библиотеки

```python
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import API_TOKEN  # Импортируем токен из файла config.py

```

#### Вставьте основной код

```python


# Инициализация диспетчера для обработки событий
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Этот обработчик срабатывает на команду /start.
    """
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!")

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Этот обработчик отвечает на любое сообщение, копируя его.
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Хорошая попытка!")

async def main() -> None:
    # Инициализация бота с параметрами по умолчанию
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    # Запуск диспетчера для обработки сообщений
    await dp.start_polling(bot)

```

#### Вставьте код для запуска


```python
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
```


**ЗАПУСТИТЕ БОТА**

- Перейдите в `Telegram` и найдите вашего бота по его имени.
- Отправьте команду `/start`, чтобы увидеть приветственное сообщение.
- Отправьте любое другое сообщение, и бот отправит его копию обратно.