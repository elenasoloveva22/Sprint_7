import datetime
import random
from faker import Faker

fake = Faker()


def generate_first_name():
    return fake.first_name()


def generate_password():
    # Минимальная длина 8, обязательно включаем разные символы
    return fake.password(length=8, special_chars=True, digits=True, upper_case=True, lower_case=True)


def generate_login():
    return fake.user_name()


def generate_last_name():
    return fake.last_name()


def generate_address():
    return fake.street_address()


def generate_metro_station():
    # Предположим, что у нас 1-5 станций, можно расширить при необходимости
    return random.randint(1, 5)


def generate_phone():
    return fake.phone_number()


def generate_rent_time():
    return random.randint(1, 5)


def generate_delivery_date():
    # Текущая дата в формате YYYY-MM-DD
    return str(datetime.date.today())


def generate_comment():
    return fake.text(max_nb_chars=100)


def generate_color():
    # Возвращаем список цветов для заказа, может быть пустым или с одним цветом
    return random.choice([[], ['BLACK'], ['GREY'], ['BLACK', 'GREY']])


def generate_limit_orders():
    # Лимит заказов для теста списка заказов
    return random.randint(2, 11)


def generate_courier_id():
    """
    Возвращает гарантированно несуществующий id курьера.
    Используется в негативных тестах.
    """
    return 999999999  # заведомо несуществующий id