import pytest
import requests
from data import MAIN_URL, CREATE_COURIER_URL, LOGIN_COURIER_URL, get_login, get_password, get_first_name


@pytest.fixture()
def courier_data():
    """Фикстура для хранения данных курьера"""
    return {
        "login": get_login(),
        "password": get_password(),
        "first_name": get_first_name()
    }


@pytest.fixture()
def create_courier(courier_data):
    """Фикстура для создания курьера — гарантирует успешное создание"""
    payload = {
        "login": courier_data["login"],
        "password": courier_data["password"],
        "firstName": courier_data["first_name"]
    }
    response = requests.post(f'{MAIN_URL}{CREATE_COURIER_URL}', json=payload)

    # Если курьер уже существует, создаём с новыми данными
    if response.status_code == 409:
        new_data = {
            "login": get_login(),
            "password": get_password(),
            "first_name": get_first_name()
        }
        payload = {
            "login": new_data["login"],
            "password": new_data["password"],
            "firstName": new_data["first_name"]
        }
        response = requests.post(f'{MAIN_URL}{CREATE_COURIER_URL}', json=payload)
        courier_data.update(new_data)

    # Гарантируем что курьер создан
    assert response.status_code == 201, f"Не удалось создать курьера: {response.json()}"
    return courier_data


@pytest.fixture()
def delete_courier(courier_data):
    """Фикстура для удаления курьера после теста"""
    yield
    payload = {
        "login": courier_data["login"],
        "password": courier_data["password"]
    }
    response = requests.post(f'{MAIN_URL}{LOGIN_COURIER_URL}', json=payload)

    # Проверяем, что курьер существует перед удалением
    if response.status_code == 200 and 'id' in response.json():
        id_courier = response.json()['id']
        requests.delete(f'{MAIN_URL}{CREATE_COURIER_URL}/{id_courier}')