# Импорт библиотек
import customtkinter as ctk

# Инициализация библиотеки и настройка темы
ctk.set_appearance_mode("Dark")  # Установка темной темы для всего приложения
ctk.set_default_color_theme("blue")  # Задает основную цветовую тему для виджетов

# Создание основного окна приложения
root = ctk.CTk()  # Создание основного окна приложения с помощью customtkinter
root.title("Простое To-Do приложение на customtkinter")  # Установка заголовка окна
root.geometry("500x600")  # Задает размер окна — 500 пикселей по ширине и 600 пикселей по высоте

# Список для хранения виджетов задач
task_widgets = []

# Поле для ввода новой задачи
entry = ctk.CTkEntry(root, placeholder_text="Введите новую задачу")
entry.pack(pady=10)  # Установка отступа сверху

# Создание прокручиваемого фрейма для задач
scrollable_frame = ctk.CTkScrollableFrame(root, width=450, height=400)
scrollable_frame.pack(pady=20, padx=10, fill="both", expand=True)  # Размещение фрейма с возможностью скроллинга


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


# Функция для удаления задачи
def remove_task(task_frame):
    task_frame.pack_forget()  # Скрытие фрейма с задачей
    task_widgets[:] = [task for task in task_widgets if task[0] != task_frame]  # Удаление задачи из списка виджетов


# Кнопка добавления новой задачи
add_button = ctk.CTkButton(root, text="Добавить задачу", command=add_task)
add_button.pack(pady=10)  # Установка отступа


# Функция для удаления выполненных задач
def remove_completed_tasks():
    for task_frame, task_checkbox, task_var in task_widgets[:]:
        if task_var.get() == "checked":  # Проверка, если задача отмечена как выполненная
            remove_task(task_frame)


# Кнопка удаления выполненных задач
remove_completed_button = ctk.CTkButton(root, text="Удалить выполненные задачи", command=remove_completed_tasks)
remove_completed_button.pack(pady=10)  # Установка отступа


# Запуск основного цикла приложения
if __name__ == "__main__":
    root.mainloop()
