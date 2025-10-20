import allure
import requests
from helpers import generate_password, generate_first_name, generate_login
from data import MAIN_URL, CREATE_COURIER_URL

class TestCreateCourier:

    @allure.title('Создать двух одинаковых курьеров')
    def test_create_two_same_courier_show_message_conflict(self, create_courier):
        with allure.step("Попытка создать курьера с уже существующим логином"):
            payload = {"login": create_courier["login"], "password": create_courier["password"], "firstName": create_courier["first_name"]}
            response = requests.post(f'{MAIN_URL}{CREATE_COURIER_URL}', json=payload)
            assert response.status_code == 409
            assert response.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}

    @allure.title('Создать курьера и получить статус код 201')
    def test_create_courier_return_status_code_201(self):
        login = generate_login()
        password = generate_password()
        first_name = generate_first_name()
        payload = {"login": login, "password": password, "firstName": first_name}
        with allure.step("Создание нового курьера"):
            response = requests.post(f'{MAIN_URL}{CREATE_COURIER_URL}', json=payload)
            assert response.status_code == 201
            assert 'ok' in response.json() or response.json() == {"ok": True}

    @allure.title('Создать курьера без логина или пароля')
    def test_create_courier_without_required_field_show_message_bad_request(self):
        login = generate_login()
        first_name = generate_first_name()
        payload = {"login": login, "firstName": first_name}
        with allure.step("Создание курьера без обязательных полей"):
            response = requests.post(f'{MAIN_URL}{CREATE_COURIER_URL}', json=payload)
            assert response.status_code == 400
            assert response.json() == {'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}

    @allure.title('Создать курьера c логином, который уже существует в системе')
    def test_create_courier_with_login_already_exists_show_message_conflict(self, create_courier):
        with allure.step("Попытка создать курьера с логином, который уже существует"):
            payload = {"login": create_courier["login"], "password": generate_password(), "firstName": generate_first_name()}
            response = requests.post(f'{MAIN_URL}{CREATE_COURIER_URL}', json=payload)
            assert response.status_code == 409
            assert response.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}
