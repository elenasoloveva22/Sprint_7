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
    generate_color,
    generate_courier_id
)
from data import MAIN_URL, CREATE_ORDER_URL, ACCEPT_ORDER_URL

class TestAcceptOrder:

    @allure.title('Принять заказ без id курьера')
    def test_accept_order_without_courier_id_return_error(self):
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
            response_order = requests.post(f'{MAIN_URL}{CREATE_ORDER_URL}', json=payload_order)
            assert response_order.status_code == 201, "Не удалось создать заказ"
            order_id = response_order.json().get('track')

        with allure.step("Попытка принять заказ без id курьера"):
            response = requests.put(f'{MAIN_URL}{ACCEPT_ORDER_URL}/{order_id}', json={})
            
        with allure.step("Проверка ответа - недостаточно данных"):
            assert response.status_code == 400
            assert response.json() == {"code": 400, "message": "Недостаточно данных для поиска"}

    @allure.title('Принять заказ с некорректным id курьера')
    def test_accept_order_with_incorrect_courier_id_return_error(self):
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
            response_order = requests.post(f'{MAIN_URL}{CREATE_ORDER_URL}', json=payload_order)
            assert response_order.status_code == 201
            order_id = response_order.json().get('track')

        with allure.step("Попытка принять заказ с некорректным id курьера"):
            response = requests.put(f'{MAIN_URL}{ACCEPT_ORDER_URL}/{order_id}', json={'courierId': generate_courier_id()})

        with allure.step("Проверка ответа - недостаточно данных"):
            assert response.status_code == 400
            assert response.json() == {"code": 400, "message": "Недостаточно данных для поиска"}

    @allure.title('Принять заказ с некорректным id заказа')
    def test_accept_order_with_incorrect_order_id_return_error(self):
        with allure.step("Попытка принять заказ с несуществующим id заказа"):
            response = requests.put(f'{MAIN_URL}{ACCEPT_ORDER_URL}/999999', json={'courierId': generate_courier_id()})

        with allure.step("Проверка ответа - недостаточно данных"):
            assert response.status_code == 400
            assert response.json() == {"code": 400, "message": "Недостаточно данных для поиска"}

    @allure.title('Принять заказ без id заказа')
    def test_accept_order_without_order_id_return_error(self):
        with allure.step("Попытка принять заказ без id"):
            response = requests.put(f'{MAIN_URL}{ACCEPT_ORDER_URL}/', json={'courierId': generate_courier_id()})

        with allure.step("Проверка ответа - неверный endpoint"):
            assert response.status_code == 404
            assert response.json() == {"code": 404, "message": "Not Found."}

