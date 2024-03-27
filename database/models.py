from sqlalchemy import BIGINT, BOOLEAN
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class UserMessages(Base):
    __tablename__ = 'user_messages'

    message_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    state: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=False)
