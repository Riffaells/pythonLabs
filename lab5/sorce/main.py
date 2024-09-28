# Импорт библиотек
import customtkinter as ctk

# Инициализация библиотеки и настройка темы
ctk.set_appearance_mode("Light")  # Установка светлой темы
ctk.set_default_color_theme("green")  # Установка цветовой схемы

# Создание основного окна приложения
root = ctk.CTk()  # Создание основного окна с использованием CTk вместо стандартного Tk
root.title("Простой калькулятор на customtkinter")  # Установка заголовка окна
root.geometry("400x300")  # Установка фиксированного размера окна

# Создание виджетов
# Поля для ввода чисел
entry1 = ctk.CTkEntry(root, placeholder_text="Введите первое число")
entry1.pack(pady=10)

entry2 = ctk.CTkEntry(root, placeholder_text="Введите второе число")
entry2.pack(pady=10)

# Выпадающий список для выбора операции
operation = ctk.StringVar(value="Сложение")  # Установка начального значения
operations_menu = ctk.CTkOptionMenu(root, values=["Сложение", "Вычитание", "Умножение", "Деление"], variable=operation)
operations_menu.pack(pady=10)

# Метка для отображения результата
result_label = ctk.CTkLabel(root, text="Результат появится здесь", font=("Arial", 16))
result_label.pack(pady=20)


# Функция для выполнения операции
def calculate():
    try:
        # Получение значений из полей ввода
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        op = operation.get()

        # Выполнение выбранной операции
        if op == "Сложение":
            result = num1 + num2
        elif op == "Вычитание":
            result = num1 - num2
        elif op == "Умножение":
            result = num1 * num2
        elif op == "Деление":
            if num2 != 0:  # Проверка деления на ноль
                result = num1 / num2
            else:
                result = "Ошибка: деление на ноль"

        # Обновление текста метки с результатом
        result_label.configure(text=f"Результат: {result}")
    except ValueError:
        result_label.configure(text="Ошибка: введите корректные числа")


# 4.5. Кнопка для выполнения операции
calculate_button = ctk.CTkButton(root, text="Выполнить операцию", command=calculate)
calculate_button.pack(pady=20)

# Запуск основного цикла приложения
if __name__ == "__main__":
    root.mainloop()
