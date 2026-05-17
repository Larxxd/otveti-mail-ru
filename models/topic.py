from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database import Base

class Topic(Base):
    __tablename__ = "topics"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), nullable = False)