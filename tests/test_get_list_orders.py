import allure
import requests
from data import MAIN_URL, GET_LIST_ORDERS_URL, generate_limit_orders

class TestListOrders:

    @allure.title('Получить заказы и проверить тело ответа возвращает список заказов')
    def test_get_orders_return_list_orders(self):
        limit = generate_limit_orders()
        params = {"limit": limit}
        response = requests.get(f'{MAIN_URL}{GET_LIST_ORDERS_URL}', params=params)

        assert len(response.json()['orders']) == limit
