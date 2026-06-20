import asyncio
from ..database import AsyncSessionLocal, engine, Base
from ..models.topic import Topic

TOPICS = ["Политика", "Наука", "Спорт", "Технологии"]


async def seed():
    async with AsyncSessionLocal() as db:
        for name in TOPICS:
            db.add(Topic(name=name))
        await db.commit()
        
        print("Топики добавлены")

asyncio.run(seed())