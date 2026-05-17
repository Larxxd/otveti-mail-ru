from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from schemas import UserCreate, UserUpdate
from services import HashPassword


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(**user.model_dump())
    db_user.password = HashPassword().hash_password(db_user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user

async def read_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
    
# Бляяя может похуй?
async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User | None:
    db_user: User | None = await read_user(db, user_id)
    if db_user == None:
        return None
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)
    db_user.password = HashPassword().hash_password(db_user.password)
    
    await db.commit()
    await db.refresh(db_user)

    return db_user