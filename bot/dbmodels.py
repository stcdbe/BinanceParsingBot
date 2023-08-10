from uuid import uuid4

from sqlalchemy import Column, BigInteger, String, Float, UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class DBBaseModel(AsyncAttrs, DeclarativeBase):
    pass


class UserTask(DBBaseModel):
    __tablename__ = 'usertask'
    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    userid = Column(BigInteger, nullable=False)
    firstticker = Column(String(5), nullable=False)
    secondticker = Column(String(5), nullable=False)
    percentofchange = Column(Float)
    price = Column(Float)
