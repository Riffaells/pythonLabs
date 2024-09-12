# Лабораторная работа №1 

## Программа для управления базой данных 

 
**Цель работы**: Разработать Telegram-бота на базе библиотеки **aiogram**, который позволит пользователям добавлять, просматривать и отслеживать задачи. В процессе выполнения работы пользователь освоит взаимодействие с базой данных SQLite для хранения данных, научится обрабатывать команды и сообщения от пользователей, а также реализует функционал по управлению данными (добавление, обновление, удаление, выборка).
 
## ТЕОРЕТИЧЕСКАЯ ЧАСТЬ
### Установка необходимых библиотек  
  
Для работы с `Telegram` и создания бота с помощью `aiogram`, вам нужно установить библиотеку `aiogram`. Откройте терминал или командную строку и выполните команду:  
  
```bash  
pip install aiogram
```

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
  

### Создание базы данных в виде класса
Создадим файл `database.py`, который будет содержать логику для работы с базой данных SQLite. Мы создадим таблицы для задач и привычек.

#### 1. Инициализация базы данных и создание таблиц
```python
class Database:
    def __init__(self, db_path='tracker.db'):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                description TEXT NOT NULL,
                due_date TEXT,
                is_completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                description TEXT NOT NULL,
                frequency TEXT,
                last_completed_date TEXT
            )
        ''')
        conn.commit()
        conn.close()
```
- **`__init__`**: Инициализирует базу данных и создает таблицы для задач и привычек, если их нет.
- **Таблицы**: 
  - `tasks` для хранения информации о задачах (ID пользователя, описание, дата выполнения).
  - `habits` для хранения привычек (ID пользователя, описание, частота).

---

#### 2. Добавление и получение задач
```python
    def add_task(self, user_id, description, due_date):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (user_id, description, due_date) VALUES (?, ?, ?)',
                       (user_id, description, due_date))
        conn.commit()
        conn.close()

    def get_tasks(self, user_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE user_id=? AND is_completed=0', (user_id,))
        tasks = cursor.fetchall()
        conn.close()
        return tasks

    def complete_task(self, task_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET is_completed=1 WHERE id=?', (task_id,))
        conn.commit()
        conn.close()
```
- **`add_task`**: Добавляет новую задачу в таблицу с ID пользователя, описанием задачи и сроком выполнения.
- **`get_tasks`**: Извлекает все незавершенные задачи для данного пользователя.
- **`complete_task`**: Отмечает задачу как завершенную по её ID.

---

#### 3. Добавление и получение привычек
```python
    def add_habit(self, user_id, description, frequency):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO habits (user_id, description, frequency) VALUES (?, ?, ?)',
                       (user_id, description, frequency))
        conn.commit()
        conn.close()

    def get_habits(self, user_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habits WHERE user_id=?', (user_id,))
        habits = cursor.fetchall()
        conn.close()
        return habits
```
- **`add_habit`**: Добавляет новую привычку для пользователя с описанием и частотой выполнения.
- **`get_habits`**: Возвращает список всех привычек для пользователя.


### Создание `bot.py`

#### 1. **Импорт библиотек и инициализация бота**

```python
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from config import API_TOKEN
from database import Database

```

- **Импорт библиотек**:

    - **`aiogram`**: Основная библиотека для работы с Telegram API.
    - **`asyncio`**: Асинхронная библиотека для запуска бота.
    - **`logging` и `sys`**: Для настройки логирования.
    - **`config`**: Здесь хранится токен API.
    - **`database`**: Импорт класса для работы с базой данных.
      
- **Инициализация бота и диспетчера**:
    
    - **`Bot`**: Инициализация бота с токеном, полученным из `config.py`.
    - **`Dispatcher`**: Объект, который обрабатывает события (команды и сообщения).
    - **`Database`**: Инициализация объекта базы данных.

----
#### 2. **Обработчики команд: `/start` и `/addtask`**

```python
@dp.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я помогу тебе управлять задачами и привычками. Используй команды /addtask и /viewtasks, а также /addhabit и /viewhabits.")

```

**Обработчик команды `/start`**:

- При вводе пользователем команды `/start`, бот отправляет приветственное сообщение с информацией о доступных командах.

```python
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

```

**Обработчик команды `/addtask`**:

- Пользователь вводит команду `/addtask`, за которой следуют описание задачи и дата выполнения.
- Если пользователь не указал все данные, бот отправляет сообщение с правильным форматом команды.
- Добавляет задачу в базу данных с помощью метода `add_task`.

----
#### 3. **Обработчики команд: `/viewtasks` и `/addhabit`**


```python
@dp.message(Command(commands=["viewtasks"]))
async def view_tasks(message: types.Message):
    tasks = db.get_tasks(message.from_user.id)
    if tasks:
        response = "\n".join([f"{task[0]}. {task[2]} (до {task[3]})" for task in tasks])
    else:
        response = "Нет активных задач."
    await message.reply(response)

```

- **Обработчик команды `/viewtasks`**:
    - Этот обработчик выводит все активные задачи для пользователя, хранящиеся в базе данных.
    - Если задач нет, выводится сообщение: "Нет активных задач."

```python
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

```

**Обработчик команды `/addhabit`**:

- Пользователь добавляет привычку с командой `/addhabit`, описанием и частотой выполнения.
- Если параметры команды указаны неверно, бот напоминает пользователю формат ввода.

----

#### 4. **Обработчик команды `/viewhabits`**

```python
@dp.message(Command(commands=["viewhabits"]))
async def view_habits(message: types.Message):
    habits = db.get_habits(message.from_user.id)
    if habits:
        response = "\n".join([f"{habit[0]}. {habit[2]} (частота: {habit[3]})" for habit in habits])
    else:
        response = "Нет активных привычек."
    await message.reply(response)

```

**Обработчик команды `/viewhabits`**:

- Выводит список привычек пользователя, хранящихся в базе данных.
- Если привычек нет, бот отправляет сообщение: "Нет активных привычек."

----

5. **Основная функция и запуск бота**


```python
async def main() -> None:
    # Инициализация бота с параметрами по умолчанию
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Запуск диспетчера для обработки сообщений
    await dp.start_polling(bot)

```

**`main()`**:

- Инициализирует бота с параметрами по умолчанию, включая HTML как форматирование для сообщений.
- **`dp.start_polling(bot)`**: Начинает опрос событий (получение и обработка новых сообщений).

```python
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
```

## Запуск бота

- Настройка логирования для отслеживания событий.
- **`asyncio.run(main())`**: Запускает асинхронную функцию `main()` для запуска бота.
