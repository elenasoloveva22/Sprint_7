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
            order_id = response_order.json().get('track') or response_order.json().get('id')

        with allure.step("Попытка принять заказ без id курьера"):
            response = requests.put(f'{MAIN_URL}{ACCEPT_ORDER_URL}/{order_id}', json={})

        with allure.step("Проверка ответа"):
            # Атомарные проверки для разных кодов
            if response.status_code == 400:
                assert response.json()['message'] == 'Недостаточно данных для поиска'
            elif response.status_code == 404:
                assert 'message' in response.json()
            else:
                assert False, f"Unexpected status code: {response.status_code}"

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
            order_id = response_order.json().get('track') or response_order.json().get('id')

        with allure.step("Попытка принять заказ с некорректным id курьера"):
            response = requests.put(f'{MAIN_URL}{ACCEPT_ORDER_URL}/{order_id}', json={'courierId': generate_courier_id()})

        with allure.step("Проверка ответа"):
            if response.status_code == 400:
                assert response.json()['message'] == 'Недостаточно данных для поиска'
            elif response.status_code == 404:
                assert 'message' in response.json()
            else:
                assert False, f"Unexpected status code: {response.status_code}"

    @allure.title('Принять заказ с некорректным id заказа')
    def test_accept_order_with_incorrect_order_id_return_error(self):
        with allure.step("Попытка создать пустой заказ для подготовки"):
            _ = requests.post(f'{MAIN_URL}{CREATE_ORDER_URL}', json={})

        with allure.step("Попытка принять заказ с несуществующим id заказа"):
            response = requests.put(f'{MAIN_URL}{ACCEPT_ORDER_URL}/999999', json={'courierId': generate_courier_id()})

        with allure.step("Проверка ответа"):
            if response.status_code == 400:
                assert response.json()['message'] == 'Недостаточно данных для поиска'
            elif response.status_code == 404:
                assert 'message' in response.json()
            else:
                assert False, f"Unexpected status code: {response.status_code}"

    @allure.title('Принять заказ без id заказа')
    def test_accept_order_without_order_id_return_error(self):
        with allure.step("Попытка принять заказ без id"):
            response = requests.put(f'{MAIN_URL}{ACCEPT_ORDER_URL}/', json={'courierId': generate_courier_id()})

        with allure.step("Проверка ответа"):
            if response.status_code == 400:
                assert response.json()['message'] == 'Недостаточно данных для поиска'
            elif response.status_code == 404:
                assert 'message' in response.json()
            else:
                assert False, f"Unexpected status code: {response.status_code}"

