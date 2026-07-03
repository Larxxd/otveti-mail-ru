from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..models import Question
from ..schemas import QuestionCreate, QuestionUpdate, QuestionRead
from typing import Sequence
from datetime import datetime


async def create_question(db: AsyncSession, user_id: int, question: QuestionCreate) -> Question:
    db_question = Question(**question.model_dump())
    db_question.user_id = user_id
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


async def update_question(db: AsyncSession, question: QuestionUpdate, user_id: int, question_id: int) -> Question | None:
    if question == None:
        return None

    db_question = await read_question(db, question_id)
    if QuestionRead.model_validate(db_question).user_id != user_id:
        return db_question

    for field, value in question.model_dump(exclude_unset=True).items():
        if value is None:
            continue
        setattr(db_question, field, value)
    setattr(db_question, "updated_at", datetime.now())

    await db.commit()
    await db.refresh(db_question)
    return db_question
