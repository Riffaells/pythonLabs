import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from config import API_TOKEN
from database import Database

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

db = Database()  # Инициализация базы данных


# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я помогу тебе управлять задачами и привычками. Используй команды /addtask и /viewtasks, а также /addhabit и /viewhabits.")


# Обработчик команды /addtask
@dp.message(Command(commands=["addtask"]))
async def add_task(message: types.Message):
    args = message.text.split(' ', 2)
    if len(args) < 3:
        await message.reply("Используй: /addtask [описание] [дата выполнения]")
        return

    description = args[1]
    due_date = args[2]

    db.add_task(message.from_user.id, description, due_date)
    await message.reply(f"Задача '{description}' добавлена на {due_date}!")


# Обработчик команды /viewtasks
@dp.message(Command(commands=["viewtasks"]))
async def view_tasks(message: types.Message):
    tasks = db.get_tasks(message.from_user.id)
    if tasks:
        response = "\n".join([f"{task[0]}. {task[2]} (до {task[3]})" for task in tasks])
    else:
        response = "Нет активных задач."
    await message.reply(response)


# Обработчик команды /addhabit
@dp.message(Command(commands=["addhabit"]))
async def add_habit(message: types.Message):
    args = message.text.split(' ', 2)
    if len(args) < 3:
        await message.reply("Используй: /addhabit [описание] [частота]")
        return

    description = args[1]
    frequency = args[2]

    db.add_habit(message.from_user.id, description, frequency)
    await message.reply(f"Привычка '{description}' добавлена с частотой '{frequency}'!")


# Обработчик команды /viewhabits
@dp.message(Command(commands=["viewhabits"]))
async def view_habits(message: types.Message):
    habits = db.get_habits(message.from_user.id)
    if habits:
        response = "\n".join([f"{habit[0]}. {habit[2]} (частота: {habit[3]})" for habit in habits])
    else:
        response = "Нет активных привычек."
    await message.reply(response)


async def main() -> None:
    # Инициализация бота с параметрами по умолчанию
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Запуск диспетчера для обработки сообщений
    await dp.start_polling(bot)


# Запуск бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
