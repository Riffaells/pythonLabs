# Лабораторная работа №4

## Создание простого приложения на customtkinter

**Цель работы**: Овладеть базовыми навыками работы с библиотекой customtkinter для создания графических интерфейсов на языке Python. Научиться создавать простые приложения, используя основные виджеты, такие как кнопки, текстовые поля, выпадающие списки и чекбоксы, а также обрабатывать события, связанные с взаимодействием пользователя.

## ТЕОРЕТИЧЕСКАЯ ЧАСТЬ

### Установка Библиотеки customtkinter

```shell
pip3 install customtkinter
```

### 1. Импорт библиотек:

`customtkinter` импортируется как `ctk`. Это упрощает использование библиотечных методов и виджетов в дальнейшем коде.

```python
# Импорт библиотек
import customtkinter as ctk
```

#### Инициализация библиотеки и настройка темы:

```python
set_appearance_xmode("Dark")  # Устанавливает темную тему для всего приложения.
set_default_color_theme("blue")  # Задает основную цветовую тему для виджетов.

```

#### Создание основного окна:

```python
root = ctk.CTk()  # Создает основное окно приложения с помощью customtkinter. Заменяет стандартный Tk в tkinter.
root.title("Лабораторная работа по customtkinter")  # Устанавливает заголовок окна.
root.geometry("500x400")  # Задает размер окна — 500 пикселей по ширине и 400 пикселей по высоте.
```

#### Добавление виджетов:

- Заголовок: `label` — виджет, отображающий текст. Создан с шрифтом `Arial` и размером 20. Располагается с помощью
  метода `pack` с отступом `pady=20`.

```python
label = ctk.CTkLabel(root, text="Добро пожаловать в customtkinter!", font=("Arial", 20))
label.pack(pady=20)  # Установка отступа сверху
```

- Кнопка: `button` — виджет кнопки. При нажатии выполняет функцию on_button_click, которая изменяет текст на label.

```python
Добавление
кнопки


def on_button_click():
    label.configure(text="Вы нажали на кнопку!")


button = ctk.CTkButton(root, text="Нажми меня", command=on_button_click)
button.pack(pady=10)  # Установка отступа между кнопкой и другими элементами
```

- Текстовое поле: `entry` — виджет для ввода текста с `placeholder` — подсказкой.

```python
Добавление
текстового
поля
entry = ctk.CTkEntry(root, placeholder_text="Введите что-то...")
entry.pack(pady=10)

```

- Чекбокс: checkbox — виджет для включения и выключения опции. Использует переменную `checkbox_var` для отслеживания
  состояния (включен/выключен). При изменении состояния запускается функция `on_checkbox_toggle`, изменяющая текст на
  `label`.

```python
# Добавление чекбокса
def on_checkbox_toggle():
    if checkbox_var.get() == 1:
        label.configure(text="Чекбокс включен")
    else:
        label.configure(text="Чекбокс выключен")


checkbox_var = ctk.IntVar()
checkbox = ctk.CTkCheckBox(root, text="Согласен с условиями", variable=checkbox_var, command=on_checkbox_toggle)
checkbox.pack(pady=10)

```

- Выпадающий список: `optionmenu` — виджет с несколькими вариантами выбора. При выборе нового значения запускается
  функция `on_optionmenu_change`, изменяющая текст на `label`.

```python
# Добавление выпадающего списка
def on_optionmenu_change(choice):
    label.configure(text=f"Вы выбрали: {choice}")


optionmenu = ctk.CTkOptionMenu(root, values=["Опция 1", "Опция 2", "Опция 3"], command=on_optionmenu_change)
optionmenu.pack(pady=10)

```

#### Запуск основного цикла приложения:

`root.mainloop()` - Основной цикл событий, который удерживает окно открытым и отслеживает действия пользователя.

```python

# Запуск основного цикла приложения
if __name__ == "__main__":
    root.mainloop()

```