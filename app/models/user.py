from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ..database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Answer
    from models import RefreshToken


class User(Base):
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    answers: Mapped[list["Answer"]] = relationship(back_populates="user")
    refreshtoken: Mapped["RefreshToken"] = relationship(back_populates="user")
