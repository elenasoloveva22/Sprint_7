import random
import allure
import pytest
import requests
from helpers import generate_login, generate_password, generate_first_name
from data import MAIN_URL

class TestLoginCourier:

    @allure.title('Выполнить логин с логином и паролем')
    def test_login_courier_with_login_password_true(self, create_courier):
        payload = {"login": create_courier["login"], "password": create_courier["password"]}
        response = requests.post(f'{MAIN_URL}/api/v1/courier/login', json=payload)

        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title('Выполнить логин с несуществующим логином и паролем')
    def test_login_courier_with_bad_login_password_return_message_error(self):
        payload = {"login": generate_login(), "password": generate_password()}
        response = requests.post(f'{MAIN_URL}/api/v1/courier/login', json=payload)

        assert response.status_code == 404
        assert response.json() == {'code': 404, 'message': 'Учетная запись не найдена'}

    @allure.title('Выполнить логин без логина или пароля')
    @pytest.mark.parametrize('login_courier, password_courier', [
        [generate_login(), ''],
        ['', generate_password()]
    ])
    def test_login_courier_without_login_or_password_return_message_error(self, login_courier, password_courier):
        payload = {"login": login_courier, "password": password_courier}
        response = requests.post(f'{MAIN_URL}/api/v1/courier/login', json=payload)

        assert response.status_code == 400
        assert response.json() == {'code': 400, 'message': 'Недостаточно данных для входа'}

    @allure.title('Логин возвращает идентификатор курьера')
    def test_login_courier_return_id_courier(self):
        login = f"{generate_login()}{random.randint(1000,9999)}"
        password = generate_password()
        first_name = generate_first_name()

        create_payload = {"login": login, "password": password, "firstName": first_name}
        create_response = requests.post(f'{MAIN_URL}/api/v1/courier', json=create_payload)
        assert create_response.status_code == 201

        login_payload = {"login": login, "password": password}
        login_response = requests.post(f'{MAIN_URL}/api/v1/courier/login', json=login_payload)
        assert login_response.status_code == 200
        assert 'id' in login_response.json()


