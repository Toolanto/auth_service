import pytest
from fastapi.testclient import TestClient

from auth_service.adapters.http.routers.schemas import Authentication, UserRes
from auth_service.controller import Controller
from auth_service.dependencies.controller import get_controller
from auth_service.repositories import UserStoreErrors
from auth_service.usecases.create_user import CreateUserData
from auth_service.usecases.login_user import (
    LoginUserData,
    LoginUserErrors,
    LoginUserRes,
)
from auth_service.usecases.otp_login import OtpLoginData, OtpLoginErrors
from main import app


@pytest.fixture()
def controller(mocker):
    return mocker.Mock(spec=Controller)


@pytest.fixture()
def client(controller):
    app.dependency_overrides[get_controller] = lambda: controller
    return TestClient(app)


class TestRegister:
    @pytest.mark.parametrize(
        "data,expected_user",
        [
            pytest.param(
                {"email": "email@test.test", "name": "test", "password": "pwd12300"},
                UserRes(email="email@test.test", name="test", two_factor_auth_enabled=False),
            ),
            pytest.param(
                {
                    "email": "email@test.test",
                    "name": "test",
                    "password": "pwd12300",
                    "name": "test",
                    "last_name": "testino",
                    "two_factor_auth_enabled": True,
                },
                UserRes(
                    email="email@test.test",
                    name="test",
                    last_name="testino",
                    two_factor_auth_enabled=True,
                ),
            ),
        ],
    )
    def test_register(self, client, controller, data, expected_user):
        # given

        controller.create_user.return_value = expected_user
        # when
        res = client.post("/users", json=data)
        # then
        assert res.status_code == 201
        assert res.json() == expected_user.model_dump()
        controller.create_user.assert_called_once_with(req=CreateUserData(**data))

    @pytest.mark.parametrize(
        "data",
        [
            pytest.param(
                {"email": "email@test.test", "name": "test", "password": "pw"},
                id="invalid password",
            ),
            pytest.param(
                {"email": "email", "name": "test", "password": "pwd12300"}, id="invalid email"
            ),
            pytest.param({"email": "email", "name": "test"}, id="missing password"),
        ],
    )
    def test_return_validation_error(self, client, controller, data):
        # given

        # when
        res = client.post("/users", json=data)
        # then
        assert res.status_code == 422
        controller.create_user.assert_not_called()

    def test_return_conflict_error(self, client, controller):
        # given
        data = {"email": "email@test.test", "name": "test", "password": "pwd12300"}
        controller.create_user.side_effect = UserStoreErrors.AlreadyExists("error")
        # when
        res = client.post("/users", json=data)
        # then
        assert res.status_code == 409
        controller.create_user.assert_called_once_with(req=CreateUserData(**data))


class TestLogin:
    @pytest.mark.parametrize(
        "controller_res,endpoint_res",
        [
            pytest.param(LoginUserRes(token="token"), Authentication(token="token")),
            pytest.param(LoginUserRes(otp_id="otp-id"), Authentication(otp_id="otp-id")),
        ],
    )
    def test_login_user(self, client, controller, controller_res, endpoint_res):
        # given
        controller.login_user.return_value = controller_res
        data = {"email": "email@email.it", "password": "password123"}
        # when
        res = client.post("/login", json=data)
        # then
        assert res.status_code == 200
        assert res.json() == endpoint_res.model_dump()
        controller.login_user.assert_called_once_with(req=LoginUserData(**data))

    @pytest.mark.parametrize(
        "exception,code",
        [
            pytest.param(LoginUserErrors.InvalidCredentials, 401),
            pytest.param(UserStoreErrors.NotFoundError, 422),
        ],
    )
    def test_errors(self, client, controller, exception, code):
        # given
        controller.login_user.side_effect = exception
        data = {"email": "email@email.it", "password": "password123"}
        # when
        res = client.post("/login", json=data)
        # then
        assert res.status_code == code
        controller.login_user.assert_called_once_with(req=LoginUserData(**data))


class TestOptLogin:
    def test_login_user(self, client, controller):
        # given
        token = "token"
        controller.otp_login.return_value = token
        data = {"otp_id": "otp-123", "otp_value": "12345"}
        # when
        res = client.post("/otp-login", json=data)
        # then
        assert res.status_code == 200
        assert res.json() == Authentication(token=token).model_dump()
        controller.otp_login.assert_called_once_with(req=OtpLoginData(**data))

    @pytest.mark.parametrize(
        "exception,code",
        [
            pytest.param(OtpLoginErrors.InvalidCredentials, 401),
            pytest.param(UserStoreErrors.NotFoundError, 422),
        ],
    )
    def test_errors(self, client, controller, exception, code):
        # given
        controller.otp_login.side_effect = exception
        data = {"otp_id": "otp-123", "otp_value": "12345"}
        # when
        res = client.post("/otp-login", json=data)
        # then
        assert res.status_code == code
        controller.otp_login.assert_called_once_with(req=OtpLoginData(**data))
