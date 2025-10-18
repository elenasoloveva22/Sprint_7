import allure
import pytest
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
from data import MAIN_URL, CREATE_ORDER_URL

class TestCreateOrder:

    @allure.title('Создать заказ с разными вариантами цвета')
    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GREY'],
        []
    ])
    def test_create_order_with_different_colors(self, color):
        payload_order = {
            "firstName": generate_first_name(),
            "lastName": generate_password(),
            "address": generate_address(),
            "metroStation": generate_metro_station(),
            "phone": generate_phone(),
            "rentTime": generate_rent_time(),
            "deliveryDate": generate_delivery_date(),
            "comment": generate_comment(),
            "color": color
        }
        response = requests.post(f'{MAIN_URL}{CREATE_ORDER_URL}', json=payload_order)
        assert response.status_code == 201
        assert 'track' in response.json()
