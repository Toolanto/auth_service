from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    two_factor_auth_enabled = Column(Boolean, nullable=False)


class OtpModel(Base):
    __tablename__ = "otp"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    value = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), nullable=False)
    expired = Column(DateTime(timezone=True), nullable=False)
    checked = Column(Boolean, nullable=False, default=False)
