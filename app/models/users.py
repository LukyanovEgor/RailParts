from sqlalchemy import INTEGER, VARCHAR, BOOLEAN, TIMESTAMP, Column, func
from app.db import Base


class Users(Base):
    __tablename__ = 'user'

    user_id = Column(INTEGER(), primary_key=True)
    user_password = Column(VARCHAR(length=256))
    email = Column(VARCHAR(length=255))
    phone = Column(VARCHAR(length=20))
    age = Column(INTEGER())
    firstname = Column(VARCHAR(length=20))
    lastname = Column(VARCHAR(length=20))
    patronymic = Column(VARCHAR(length=20))
    is_admin = Column(BOOLEAN(), default=False)
    icon = Column(VARCHAR(length=255))
    reg_date = Column(TIMESTAMP(), server_default=func.now())