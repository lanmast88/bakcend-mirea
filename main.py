from datetime import date

username = "ivan_petrov"
password = "qwerty123"
entered_password = "qwerty123"
is_logged_in = (entered_password == password)


def get_login_status(is_logged_in):
    if is_logged_in:
        return f"Пользователь '{username}' успешно авторизован"
    return "Неверный пароль, авторизация не выполнена"


item_name = "Молоко"
category = "Продукты"
unit = "л"
quantity_input = "5"            
quantity = int(quantity_input)  
min_threshold = 2
date_added = date(2026, 9, 8)


def get_add_confirmation(item_name, category, quantity):
    if quantity > 0:
        return f"Товар '{item_name}' добавлен в категорию '{category}' в количестве {quantity} {unit}"
    return f"Товар '{item_name}' не добавлен: количество должно быть больше нуля"


used_amount = 3
quantity = quantity - used_amount


def get_stock_status(quantity, min_threshold):
    if quantity <= 0:
        return "Товар закончился, необходимо купить"
    elif quantity < min_threshold:
        return "Внимание: остаток товара ниже порога, пора пополнить запас"
    else:
        return "Запас товара в норме"


print(f"Пользователь: {username}")
print(get_login_status(is_logged_in))
print(f"Дата добавления товара: {date_added}")
print(get_add_confirmation(item_name, category, quantity))
print(get_stock_status(quantity, min_threshold))
