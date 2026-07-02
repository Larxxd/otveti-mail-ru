from sqlalchemy import Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import User


class RefreshToken(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), index=True, nullable=False)
    token: Mapped[str] = mapped_column(
        Text, nullable=False, index=True, unique=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now() + timedelta(days=30))
    user: Mapped["User"] = relationship(back_populates="refreshtoken")
