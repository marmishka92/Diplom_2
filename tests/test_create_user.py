import pytest
import allure
import requests
import data
from urls import UrlsApi
from helpers import UserData

@allure.epic("API: Регистрация пользователя")
class TestCreateUser:

    @allure.title('Проверка успешного создания нового уникального пользователя')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_ok(self):
        with allure.step("Формирование данных для нового пользователя"):
            user = UserData.create_user_data()

        with allure.step("Отправка запроса на регистрацию нового пользователя"):
            response = requests.post(UrlsApi.CREATE_USER, json=user)

        with allure.step("Проверка успешного ответа сервера"):
            assert response.status_code == data.StatusCode.OK
            assert response.json()["success"] == data.TextResponse.TRUE

        with allure.step("Удаление созданного пользователя через API"):
            token = response.json().get("accessToken")
            if token:
                requests.delete(UrlsApi.DELETE_USER, headers={"Authorization": token})

    @allure.title('Попытка зарегистрировать пользователя, который уже существует в системе')
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_two_registered(self):
        with allure.step("Создание пользователя"):
            user = UserData.create_user_data()
            requests.post(UrlsApi.CREATE_USER, json=user)

        with allure.step("Повторная попытка регистрации того же пользователя"):
            response = requests.post(UrlsApi.CREATE_USER, json=user)

        with allure.step("Проверка ошибки о существующем пользователе"):
            assert response.status_code == data.StatusCode.FORBIDDEN
            assert response.json()["message"] == data.TextResponse.CREATE_DOUBLE_USER

    @allure.title('Попытка создать пользователя без заполнения одного из обязательных полей')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('payload', (
        UserData.create_user_no_name(),
        UserData.create_user_no_password(),
        UserData.create_user_no_email()
    ))
    def test_create_no_data(self, payload):
        with allure.step("Отправка запроса на создание пользователя с неполными данными"):
            response = requests.post(UrlsApi.CREATE_USER, json=payload)

        with allure.step("Проверка ошибки и кода ответа"):
            assert response.status_code == data.StatusCode.FORBIDDEN
            assert response.json()["success"] == data.TextResponse.FALSE
            assert response.json()["message"] == data.TextResponse.NOT_FIELD