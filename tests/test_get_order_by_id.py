import allure
import requests
from helpers import (
    generate_first_name,
    generate_password,
    generate_address,
    generate_metro_station,
    generate_phone,
    generate_rent_time,
    generate_delivery_date,
    generate_comment,
    generate_color
)
from data import MAIN_URL, CREATE_ORDER_URL, GET_ORDER_BY_ID_URL

class TestGetOrderById:

    @allure.title('Получить заказ по его номеру - успешный запрос возвращает объект с заказом')
    def test_get_order_by_id_success_return_order_object(self):
        payload_order = {
            "firstName": generate_first_name(),
            "lastName": generate_password(),
            "address": generate_address(),
            "metroStation": generate_metro_station(),
            "phone": generate_phone(),
            "rentTime": generate_rent_time(),
            "deliveryDate": generate_delivery_date(),
            "comment": generate_comment(),
            "color": generate_color()
        }

        with allure.step("Создание заказа"):
            response = requests.post(f'{MAIN_URL}{CREATE_ORDER_URL}', json=payload_order)
            assert response.status_code == 201
            order_id = response.json()['track']

        with allure.step("Получение заказа по номеру"):
            params = {"t": order_id}
            response = requests.get(f'{MAIN_URL}{GET_ORDER_BY_ID_URL}', params=params)
            assert response.status_code == 200
            assert 'order' in response.json()

    @allure.title('Получить заказ без номера заказа - возвращает ошибку')
    def test_get_order_without_id_return_error(self):
        params = {"t": ""}
        with allure.step("Попытка получить заказ без номера"):
            response = requests.get(f'{MAIN_URL}{GET_ORDER_BY_ID_URL}', params=params)
            assert response.status_code == 400
            assert response.json() == {'code': 400, 'message': 'Недостаточно данных для поиска'}

    @allure.title('Получить заказ с несуществующим номером - возвращает ошибку')
    def test_get_order_by_not_exist_id_return_error(self):
        params = {"t": 999999}
        with allure.step("Попытка получить заказ с несуществующим номером"):
            response = requests.get(f'{MAIN_URL}{GET_ORDER_BY_ID_URL}', params=params)
            assert response.status_code == 404
            assert response.json() == {'code': 404, 'message': 'Заказ не найден'}