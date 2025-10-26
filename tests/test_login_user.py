import pytest
import allure
import requests
import data
from urls import UrlsApi
from helpers import UserData

@allure.epic("API: Авторизация пользователя")
class TestLoginUser:

    @allure.title('Успешный вход под ранее созданным пользователем')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_user(self):
        with allure.step("Создание нового пользователя через API"):
            user = UserData.create_user_data()
            create_response = requests.post(UrlsApi.CREATE_USER, json=user)
            assert create_response.status_code == data.StatusCode.OK, \
                f"Не удалось создать пользователя: {create_response.text}"

        with allure.step("Авторизация пользователя с корректными данными"):
            login_response = requests.post(UrlsApi.LOGIN_USER, json=user)

        with allure.step("Проверка успешного входа"):
            assert login_response.status_code == data.StatusCode.OK
            assert login_response.json()["success"] == data.TextResponse.TRUE

        # очистка данных
        with allure.step("Удаление созданного пользователя"):
            token = create_response.json().get("accessToken")
            if token:
                requests.delete(UrlsApi.DELETE_USER, headers={"Authorization": token})

    @allure.title('Попытка авторизации с некорректным логином или паролем')
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_no_user(self):
        with allure.step("Отправка запроса с некорректными данными пользователя"):
            user = UserData.create_user_no_name()
            response = requests.post(UrlsApi.LOGIN_USER, json=user)

        with allure.step("Проверка сообщения об ошибке"):
            assert response.status_code == data.StatusCode.UNAUTHORIZED
            assert response.json()["message"] == data.TextResponse.BAD_LOGIN_PASS
            assert response.json()["success"] == data.TextResponse.FALSE