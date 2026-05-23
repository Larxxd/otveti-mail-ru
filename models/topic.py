from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from ..database import Base

class Topic(Base):
    name: Mapped[str] = mapped_column(String(20), nullable = False)