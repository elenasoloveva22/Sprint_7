import allure
import requests
from data import MAIN_URL, CREATE_COURIER_URL, LOGIN_COURIER_URL

class TestDeleteCourier:

    @allure.title('Удалить курьера с несуществующим id')
    def test_delete_courier_not_exist_id_return_message_error(self):
        courier_id = 999999
        with allure.step("Попытка удалить несуществующего курьера"):
            response = requests.delete(f'{MAIN_URL}{CREATE_COURIER_URL}/{courier_id}')

        with allure.step("Проверка ответа - курьер не найден"):
            assert response.status_code == 404
            assert response.json() == {"code": 404, "message": "Курьера с таким id нет."}

    @allure.title('Удалить существующего курьера — успешный сценарий')
    def test_delete_courier_return_ok_true(self, create_courier):
        with allure.step("Логин курьера для получения id"):
            payload = {"login": create_courier["login"], "password": create_courier["password"]}
            response = requests.post(f'{MAIN_URL}{LOGIN_COURIER_URL}', json=payload)
            assert response.status_code == 200
            id_courier = response.json().get('id')

        with allure.step("Удаление курьера"):
            delete_response = requests.delete(f'{MAIN_URL}{CREATE_COURIER_URL}/{id_courier}')

        with allure.step("Проверка ответа"):
            assert delete_response.status_code == 200
            body = delete_response.json()
            assert body == {'ok': True}

    @allure.title('Удалить курьера без указания id')
    def test_delete_courier_without_id_return_message_not_found(self):
        with allure.step("Попытка удалить курьера без указания id"):
            response = requests.delete(f'{MAIN_URL}{CREATE_COURIER_URL}')

        with allure.step("Проверка ответа - неверный endpoint"):
            assert response.status_code == 404
            assert response.json() == {"code": 404, "message": "Not Found."}