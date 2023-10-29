from uuid import uuid4

from sqlalchemy import BigInteger, String, UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class DBBaseModel(AsyncAttrs, DeclarativeBase):
    pass


class UserTask(DBBaseModel):
    __tablename__ = 'usertask'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    # id: Mapped[int] = mapped_column(primary_key=True)
    userid: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    firstticker: Mapped[str] = mapped_column(String(5), nullable=False)
    secondticker: Mapped[str] = mapped_column(String(5), nullable=False)
    percentofchange: Mapped[float]
    price: Mapped[float]

    def __repr__(self) -> str:
        return self.id
