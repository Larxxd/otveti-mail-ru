from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..models import Question
from ..schemas import QuestionCreate
from typing import Sequence


async def create_question(db: AsyncSession, question: QuestionCreate) -> Question:
    db_question = Question(**question.model_dump())
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)

    result = await db.execute(
        select(Question)
        .where(Question.id == db_question.id)
        .options(selectinload(Question.answers))
    )

    return result.scalar_one()

async def read_questions(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Question] | None:
    result = await db.execute(select(Question).offset(skip).limit(limit).options(selectinload(Question.answers)))
    return result.scalars().all()

async def read_question(db: AsyncSession, question_id: int):
    db_question = await db.execute(select(Question).where(Question.id == question_id).options(selectinload(Question.answers)))
    return db_question.scalar_one_or_none()