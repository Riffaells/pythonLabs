# Лабораторные работы по созданию ботов на aiogram

Этот репозиторий содержит простые лабораторные работы по созданию Telegram-ботов с использованием библиотеки **aiogram** и баз данных SQLite.

## Список лабораторных работ

### Lab 1 - Создание эхо-бота

В первой лабораторной работе вам нужно создать простого эхо-бота, который будет повторять отправленные пользователем сообщения.

**Цель работы**: Изучить основы взаимодействия с Telegram API и научиться обрабатывать входящие сообщения с помощью **aiogram**.

**Основные задачи**:
1. Инициализация бота через токен, полученный у BotFather.
2. Создание обработчика команды `/start`, который отправляет приветственное сообщение пользователю.
3. Создание обработчика для любых входящих сообщений, который будет пересылать их обратно отправителю (эхо-функция).

### Lab 2 - Создание бота учета задач и трекера привычек

Вторая лабораторная работа направлена на создание более сложного бота, который позволит пользователям управлять задачами и отслеживать свои привычки.

**Цель работы**: Создать Telegram-бота, который взаимодействует с базой данных для управления задачами и привычками.

**Основные задачи**:
1. Реализовать базу данных SQLite для хранения задач и привычек пользователей.
2. Реализовать команды:
   - `/addtask [описание] [дата выполнения]`: добавляет новую задачу.
   - `/viewtasks`: показывает активные задачи.
   - `/addhabit [описание] [частота]`: добавляет новую привычку.
   - `/viewhabits`: показывает привычки пользователя.
3. Использовать **aiogram** для обработки команд и взаимодействия с базой данных.
