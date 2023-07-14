import pytest
from auth_service.adapters.otp_store import InMemoryOtpStore, InMemoryOtpStoreConf
from auth_service.entities.store import OtpStoreErrors
from tests import factories as fty

@pytest.fixture
def otp_file(tmp_path):
    otp_file = (tmp_path / "otps.jsonl")
    otp_file.touch(exist_ok= True)
    return otp_file

@pytest.fixture
def store(otp_file):
    conf = InMemoryOtpStoreConf(
        otp_file= otp_file
    )
    return InMemoryOtpStore(config=conf)

@pytest.mark.integration
class TestSaveOtp:

    @pytest.mark.asyncio
    async def test_save_otp(self, store, otp_file):
        #given
        otp = fty.OtpFactory()
        #when
        res = await store.save(otp=otp)
        #then
        assert res == otp
        assert otp_file.read_text() == otp.model_dump_json() + "\n"

    @pytest.mark.asyncio
    async def test_raise_error_if_otp_already_exists(self, store):
        #given
        otp = fty.OtpFactory()
        #when
        await store.save(otp=otp)
        with pytest.raises(OtpStoreErrors.AlreadyExists):
            await store.save(otp=otp)

@pytest.mark.integration
class TestGetOtp:

    @pytest.mark.asyncio
    async def test_get_otp(self, store):
        #given
        otp = fty.OtpFactory()
        await store.save(otp=otp)
        #when
        res = await store.get(session_id=otp.session_id)
        #then
        assert res == otp

    @pytest.mark.asyncio
    async def test_raise_error_if_otp_not_exits(self, store):
        #given
        otp = fty.OtpFactory()
        await store.save(otp=otp)
        #when
        with pytest.raises(OtpStoreErrors.NotFoundError):
            await store.get(session_id=fty.OtpFactory().session_id)

@pytest.mark.integration
class TestMarkChecked:

    @pytest.mark.asyncio
    async def test_mark_checked(self, store):
        #given
        otp = fty.OtpFactory()
        await store.save(otp=otp)
        #when
        await store.mark_checked(otp=otp)
        #then
        checked_otp = await store.get(otp.session_id)
        assert checked_otp.checked is True

