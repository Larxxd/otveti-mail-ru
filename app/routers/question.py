from ..dependencies import get_db, get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.question import QuestionCreate, QuestionRead
from ..schemas.answer import AnswerCreate, AnswerRead
from ..crud.question import create_question, read_questions, read_question
from ..crud.answer import create_answer
from typing import Sequence

router = APIRouter(
    prefix = "/questions",
    tags=["questions"]
)

@router.post("/create", response_model=QuestionRead)
async def make_question( question: QuestionCreate,user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await create_question(db,user_id, question)

@router.get("/{question_id}", response_model=QuestionRead)
async def get_question(question_id: int, db: AsyncSession = Depends(get_db)):
    question =  await read_question(db, question_id)
    if question is None:
        raise HTTPException(404, "Question not found!!!")
    return question

@router.post("/{question_id}", response_model=AnswerRead)
async def make_answer(question_id: int, answer_create: AnswerCreate, db: AsyncSession = Depends(get_db)):
    return await create_answer(db,answer_create, question_id)

@router.get("/", response_model=Sequence[QuestionRead])
async def get_questions(db: AsyncSession = Depends(get_db)):
    return await read_questions(db)
