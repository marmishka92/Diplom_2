import pytest
import allure
import requests
import data
from data import Ingredient
from urls import UrlsApi

@allure.epic("API: Создание заказов")
class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией пользователя')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_login(self, create_new_user):
        with allure.step("Авторизация пользователя"):
            token = create_new_user[1].json()["accessToken"]
            headers = {'Authorization': token}

        with allure.step("Создание заказа через API"):
            response = requests.post(UrlsApi.CREATE_ORDER, headers=headers, json=Ingredient.data)

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == data.StatusCode.OK
            assert response.json()["success"] == data.TextResponse.TRUE

    @allure.title('Создание заказа без авторизации')
    def test_create_order_not_login(self):
        with allure.step("Отправка запроса без авторизации"):
            response = requests.post(UrlsApi.CREATE_ORDER, json=Ingredient.data)

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == data.StatusCode.OK
            assert response.json()["success"] == data.TextResponse.TRUE

    @allure.title('Попытка создания заказа без ингредиентов')
    def test_create_order_not_ingredient(self):
        with allure.step("Отправка запроса без ингредиентов"):
            response = requests.post(UrlsApi.CREATE_ORDER, json=Ingredient.not_ingredient)

        with allure.step("Проверка ошибки на отсутствие ингредиентов"):
            assert response.status_code == data.StatusCode.BAD_REQUEST
            assert response.json()["success"] == data.TextResponse.FALSE
            assert response.json()["message"] == data.TextResponse.NOT_INGREDIENTS

    @allure.title('Создание заказа с некорректным хэшем ингредиентов')
    def test_create_order_bad_hash(self):
        with allure.step("Отправка запроса с некорректным хэшем ингредиентов"):
            response = requests.post(UrlsApi.CREATE_ORDER, json=Ingredient.hash_bad)

        with allure.step("Проверка ошибки сервера"):
            assert response.status_code == data.StatusCode.INTERNAL_SERVER_ERROR
            assert data.TextResponse.SERVER_ERROR in response.text