from auth_service.adapters.email.email_gateway import FakeEmailGateway


def get_email_gateway():
    return FakeEmailGateway()
