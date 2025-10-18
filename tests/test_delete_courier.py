import allure
import requests
from data import MAIN_URL, CREATE_COURIER_URL, LOGIN_COURIER_URL

class TestDeleteCourier:

    @allure.title('Удалить курьера с несуществующим id')
    def test_delete_courier_not_exist_id_return_message_error(self):
        courier_id = 999999
        response = requests.delete(f'{MAIN_URL}{CREATE_COURIER_URL}/{courier_id}')
        assert response.status_code == 404
        assert response.json().get('message') in ['Курьера с таким id нет.', 'Курьера с таким id не существует']

    @allure.title('Удалить существующего курьера — успешный сценарий')
    def test_delete_courier_return_ok_true(self, create_courier):
        payload = {"login": create_courier["login"], "password": create_courier["password"]}
        response = requests.post(f'{MAIN_URL}{LOGIN_COURIER_URL}', data=payload)
        id_courier = response.json().get('id')
        delete_response = requests.delete(f'{MAIN_URL}{CREATE_COURIER_URL}/{id_courier}')
        assert delete_response.status_code == 200
        assert delete_response.json() == {'ok': True}

    @allure.title('Удалить курьера без указания id')
    def test_delete_courier_without_id_return_message_not_found(self):
        response = requests.delete(f'{MAIN_URL}{CREATE_COURIER_URL}')
        assert response.status_code in [400, 404]
        assert response.json().get('message') in ['Not Found.', 'Недостаточно данных для поиска']

