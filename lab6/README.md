# Лабораторная работа №3

## Создание простого To-Do приложения на `customtkinter` с возможностью прокрутки

**Цель работы**: Овладеть базовыми навыками работы с библиотекой `customtkinter` для создания графических интерфейсов на языке Python. Научиться создавать простое приложение для управления списком задач с возможностью прокрутки, используя такие виджеты, как кнопки, текстовые поля, прокручиваемые фреймы и чекбоксы. А также реализовать функционал для отметки выполнения задач и их удаления.

## ТЕОРЕТИЧЕСКАЯ ЧАСТЬ

### Установка библиотеки `customtkinter`

Для работы с библиотекой `customtkinter` необходимо установить её командой:

```shell
pip3 install customtkinter
```

### 1. Импорт библиотек

Импорт библиотеки `customtkinter` выполняется под сокращением `ctk`, что упрощает использование методов и виджетов.

```python
# Импорт библиотек
import customtkinter as ctk
```

#### Инициализация библиотеки и настройка темы

Перед созданием интерфейса настраивается тема и цветовая схема приложения:

```python
ctk.set_appearance_mode("Dark")  # Установка темной темы для всего приложения.
ctk.set_default_color_theme("blue")  # Задает основную цветовую тему для виджетов.
```

#### Создание основного окна приложения

```python
root = ctk.CTk()  # Создание основного окна приложения с помощью customtkinter.
root.title("Простое To-Do приложение на customtkinter")  # Установка заголовка окна.
root.geometry("500x600")  # Задает размер окна — 500 пикселей по ширине и 600 пикселей по высоте.
```

#### Добавление виджетов

- **Поле для ввода новой задачи**: используется виджет `entry` для ввода текста задачи. В него пользователь будет вводить название новой задачи.

```python
entry = ctk.CTkEntry(root, placeholder_text="Введите новую задачу")
entry.pack(pady=10)  # Установка отступа сверху
```

- **Создание прокручиваемого фрейма для задач**: используется виджет `CTkScrollableFrame`, который позволяет добавлять задачи с возможностью прокрутки.

```python
scrollable_frame = ctk.CTkScrollableFrame(root, width=450, height=400)
scrollable_frame.pack(pady=20, padx=10, fill="both", expand=True)  # Размещение фрейма с возможностью скроллинга
```

- **Кнопка для добавления новой задачи**: `add_button` — виджет кнопки, при нажатии которой вызывается функция `add_task`, добавляющая новую задачу в список задач.

```python
add_button = ctk.CTkButton(root, text="Добавить задачу", command=add_task)
add_button.pack(pady=10)  # Установка отступа
```

- **Кнопка для удаления выполненных задач**: `remove_completed_button` — виджет кнопки, вызывающей функцию `remove_completed_tasks` для удаления всех задач, которые были отмечены как выполненные.

```python
remove_completed_button = ctk.CTkButton(root, text="Удалить выполненные задачи", command=remove_completed_tasks)
remove_completed_button.pack(pady=10)  # Установка отступа
```

#### Добавление функционала в приложение

Функция `add_task()` добавляет новую задачу в прокручиваемый фрейм с возможностью отмечать выполнение с помощью чекбокса и удалять каждую задачу по отдельности.

```python
# Функция добавления новой задачи
def add_task():
    task_text = entry.get()  # Считывание текста из текстового поля
    if task_text:  # Проверка, что текст не пустой
        # Создание фрейма для задачи внутри прокручиваемого фрейма
        task_frame = ctk.CTkFrame(scrollable_frame)
        task_frame.pack(pady=5, padx=10, fill="x")  # Размещение фрейма

        # Создание чекбокса для отметки выполнения задачи
        task_var = ctk.StringVar(value="unchecked")  # Переменная для хранения состояния чекбокса
        task_checkbox = ctk.CTkCheckBox(task_frame, text=task_text, variable=task_var, onvalue="checked", offvalue="unchecked")
        task_checkbox.pack(side="left", padx=5)  # Размещение чекбокса в фрейме

        # Кнопка для удаления задачи
        remove_task_button = ctk.CTkButton(task_frame, text="Удалить", width=80, command=lambda: remove_task(task_frame))
        remove_task_button.pack(side="right", padx=5)  # Размещение кнопки в фрейме

        # Сохранение виджетов задачи
        task_widgets.append((task_frame, task_checkbox, task_var))
        entry.delete(0, "end")  # Очистка текстового поля после добавления задачи
```

Функция `remove_task()` удаляет отдельную задачу из списка и удаляет её фрейм из видимого интерфейса.

```python
# Функция для удаления задачи
def remove_task(task_frame):
    task_frame.pack_forget()  # Скрытие фрейма с задачей
    task_widgets[:] = [task for task in task_widgets if task[0] != task_frame]  # Удаление задачи из списка виджетов
```

Функция `remove_completed_tasks()` удаляет все задачи, отмеченные как выполненные.

```python
# Функция для удаления выполненных задач
def remove_completed_tasks():
    for task_frame, task_checkbox, task_var in task_widgets[:]:
        if task_var.get() == "checked":  # Проверка, если задача отмечена как выполненная
            remove_task(task_frame)
```

#### Запуск основного цикла приложения

`root.mainloop()` — основной цикл событий, который удерживает окно открытым и отслеживает действия пользователя. Это позволяет приложению оставаться активным и принимать ввод от пользователя.

```python
# Запуск основного цикла приложения
if __name__ == "__main__":
    root.mainloop()
```
