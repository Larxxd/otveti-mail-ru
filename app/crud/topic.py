from ..models import Topic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence


async def read_topic(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Topic]:
    result = await db.execute(select(Topic).offset(skip).limit(limit))
    return result.scalars().all()
