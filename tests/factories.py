from datetime import datetime, timedelta, timezone

import factory

from auth_service.entities.otp import Otp
from auth_service.entities.user import User
from auth_service.usecases.create_user import CreateUserData
from auth_service.usecases.login_user import LoginUserData
from auth_service.usecases.otp_login import OtpLoginData


class UserFactory(factory.Factory):
    id = factory.Sequence(lambda n: f"id-{n}")
    email = factory.Faker("email")
    password = factory.Faker("password")
    name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    two_factor_auth_enabled = False

    class Meta:
        model = User


class OtpFactory(factory.Factory):
    id = factory.Sequence(lambda n: f"id-{n}")
    value = factory.Sequence(lambda n: f"1234{n}")
    created = factory.LazyFunction(lambda: datetime.now(tz=timezone.utc))
    expired = factory.LazyFunction(lambda: datetime.now(tz=timezone.utc) + timedelta(minutes=5))
    user_id = factory.Sequence(lambda n: f"user-id-{n}")

    class Meta:
        model = Otp


class CreateUserDataFactory(factory.Factory):
    email = factory.Faker("email")
    password = factory.Faker("password")
    name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    two_factor_auth_enabled = False

    class Meta:
        model = CreateUserData


class LoginUserDataFactory(factory.Factory):
    email = factory.Faker("email")
    password = factory.Faker("password")

    class Meta:
        model = LoginUserData


class OtpLoginDataFactory(factory.Factory):
    otp_id = factory.Sequence(lambda n: f"otp-id-{n}")
    otp_value = factory.Sequence(lambda n: f"1234{n}")

    class Meta:
        model = OtpLoginData
