import pytest

from auth_service.adapters.user_store import InMemoryUserStore, InMemoryUserStoreConf
from auth_service.entities.store import UserStoreErrors
from tests import factories as fty


@pytest.fixture
def user_file(tmp_path):
    user_file = tmp_path / "users.jsonl"
    user_file.touch(exist_ok=True)
    return user_file


@pytest.fixture
def store(user_file):
    conf = InMemoryUserStoreConf(user_file=user_file)
    return InMemoryUserStore(config=conf)


@pytest.mark.integration
class TestSaveUser:
    @pytest.mark.asyncio
    async def test_save_user(self, store, user_file):
        # given
        user = fty.UserFactory()
        # when
        res = await store.save(user=user)
        # then
        assert res == user
        assert user_file.read_text() == user.model_dump_json() + "\n"

    @pytest.mark.asyncio
    async def test_raise_error_if_user_already_exists(self, store, user_file):
        # given
        user = fty.UserFactory()
        # when
        await store.save(user=user)
        with pytest.raises(UserStoreErrors.AlreadyExists):
            await store.save(user=user)


@pytest.mark.integration
class TestGetUser:
    @pytest.mark.asyncio
    async def test_get_user(self, store):
        # given
        user = fty.UserFactory()
        await store.save(user=user)
        # when
        res = await store.get(email=user.email)
        # then
        assert res == user

    @pytest.mark.asyncio
    async def test_raise_error_if_user_not_exits(self, store):
        # given
        user = fty.UserFactory()
        await store.save(user=user)
        # when
        with pytest.raises(UserStoreErrors.NotFoundError):
            await store.get(email=fty.UserFactory().email)
