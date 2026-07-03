from ..dependencies import get_db, get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.question import QuestionCreate, QuestionRead, QuestionUpdate
from ..schemas.answer import AnswerCreate, AnswerRead
from typing import Sequence
from ..services.question_service import QuestionService

router = APIRouter(
    prefix="/questions",
    tags=["questions"]
)


@router.post("/create", response_model=QuestionRead)
async def make_question(question: QuestionCreate, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await QuestionService(db).create_question(question, user_id)


@router.get("/{question_id}", response_model=QuestionRead)
async def get_question(question_id: int, db: AsyncSession = Depends(get_db)):
    return await QuestionService(db).read_question(question_id)


@router.patch("/{question_id}", response_model=QuestionRead)
async def update_question(question_id: int, question: QuestionUpdate, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await QuestionService(db).edit_question(question, user_id, question_id)


@router.post("/{question_id}", response_model=AnswerRead)
async def make_answer(question_id: int, answer_create: AnswerCreate, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await QuestionService(db).create_answer(question_id, answer_create, user_id)


@router.get("/", response_model=Sequence[QuestionRead])
async def get_questions(db: AsyncSession = Depends(get_db)):
    return await QuestionService(db).get_all_questions()
