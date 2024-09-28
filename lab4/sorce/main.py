# Импорт библиотек
import customtkinter as ctk

# Инициализация библиотеки и настройка темы
ctk.set_appearance_mode("Dark")  # Установка темной темы
ctk.set_default_color_theme("blue")  # Установка цветовой схемы

# Создание основного окна приложения
root = ctk.CTk()  # Создание основного окна с использованием CTk вместо стандартного Tk
root.title("Лабораторная работа по customtkinter")  # Установка заголовка окна
root.geometry("500x400")  # Установка фиксированного размера окна

# Добавление виджетов
# Добавление заголовка
label = ctk.CTkLabel(root, text="Добро пожаловать в customtkinter!", font=("Arial", 20))
label.pack(pady=20)  # Установка отступа сверху


# Добавление кнопки
def on_button_click():
    label.configure(text="Вы нажали на кнопку!")


button = ctk.CTkButton(root, text="Нажми меня", command=on_button_click)
button.pack(pady=10)  # Установка отступа между кнопкой и другими элементами

# Добавление текстового поля
entry = ctk.CTkEntry(root, placeholder_text="Введите что-то...")
entry.pack(pady=10)


# Добавление чекбокса
def on_checkbox_toggle():
    if checkbox_var.get() == 1:
        label.configure(text="Чекбокс включен")
    else:
        label.configure(text="Чекбокс выключен")


checkbox_var = ctk.IntVar()
checkbox = ctk.CTkCheckBox(root, text="Согласен с условиями", variable=checkbox_var, command=on_checkbox_toggle)
checkbox.pack(pady=10)


# Добавление выпадающего списка
def on_optionmenu_change(choice):
    label.configure(text=f"Вы выбрали: {choice}")


optionmenu = ctk.CTkOptionMenu(root, values=["Опция 1", "Опция 2", "Опция 3"], command=on_optionmenu_change)
optionmenu.pack(pady=10)

# Запуск основного цикла приложения
if __name__ == "__main__":
    root.mainloop()
