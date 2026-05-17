from schemas import AnswerCreate
from models import Answer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

async def create_answer(db: AsyncSession, answer: AnswerCreate, question_id: int) -> Answer:
    db_answer = Answer(**answer.model_dump())
    db_answer.question_id = question_id
    db.add(db_answer)
    await db.commit()
    await db.refresh(db_answer)

    return db_answer

async def read_answers(db: AsyncSession, question_id: int, skip: int = 0, limit: int = 100) -> Sequence[Answer]:
    result = await db.execute(select(Answer).where(Answer.question_id == question_id).offset(skip).limit(limit))
    return result.scalars().all()