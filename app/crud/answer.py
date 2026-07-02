from ..schemas import AnswerCreate, AnswerUpdate, AnswerRead
from ..models import Answer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence


async def create_answer(db: AsyncSession, answer: AnswerCreate, question_id: int, user_id: int) -> Answer:
    db_answer = Answer(**answer.model_dump())
    db_answer.question_id = question_id
    db_answer.user_id = user_id
    db.add(db_answer)
    await db.commit()
    await db.refresh(db_answer)

    return db_answer


async def read_answers(db: AsyncSession, question_id: int, skip: int = 0, limit: int = 100) -> Sequence[Answer]:
    result = await db.execute(select(Answer).where(Answer.question_id == question_id).offset(skip).limit(limit))
    return result.scalars().all()


async def update_answer(db: AsyncSession, answer: AnswerUpdate, user_id: int, answer_id: int) -> Answer | None:
    if answer == None:
        return None

    db_answer = await db.execute(select(Answer).where(Answer.id == answer_id))
    db_answer = db_answer.scalar_one_or_none()

    if AnswerRead.model_validate(db_answer).user_id != user_id:
        return db_answer

    for field, value in answer.model_dump(exclude_unset=True).items():
        if not value:
            continue
        setattr(db_answer, field, value)

    await db.commit()
    await db.refresh(db_answer)
    return db_answer
