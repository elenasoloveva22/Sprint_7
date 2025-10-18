import random
from helpers import (
    generate_login,
    generate_password,
    generate_first_name,
    generate_limit_orders,
    generate_courier_id,
)

# ==================== Константы URL ====================
MAIN_URL = 'https://qa-scooter.praktikum-services.ru'

# Курьеры
CREATE_COURIER_URL = '/api/v1/courier/'
LOGIN_COURIER_URL = '/api/v1/courier/login'

# Заказы
CREATE_ORDER_URL = '/api/v1/orders/'
GET_LIST_ORDERS_URL = '/api/v1/orders/'
ACCEPT_ORDER_URL = '/api/v1/orders/accept'
GET_ORDER_BY_ID_URL = '/api/v1/orders/track'

# ==================== Функции для генерации данных ====================
def get_login():
    """Случайный логин"""
    return generate_login()

def get_unique_login():
    """Гарантированно уникальный логин, чтобы не было конфликта при создании"""
    return f"{generate_login()}{random.randint(1000, 9999)}"

def get_password():
    return generate_password()

def get_first_name():
    return generate_first_name()

def get_limit_orders():
    """Возвращает лимит заказов для теста списка заказов"""
    return generate_limit_orders()

def get_courier_id():
    """Возвращает случайный id курьера"""
    return generate_courier_id()

