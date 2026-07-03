from ..dependencies import get_db, get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.answer import AnswerRead, AnswerUpdate
from ..services.question_service import QuestionService

router = APIRouter(
    prefix="/answers",
    tags=["answers"]
)


@router.patch("/{answer_id}", response_model=AnswerRead)
async def update_answer(answer_id: int, answer: AnswerUpdate, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await QuestionService(db).edit_answer(answer_id, answer, user_id)


@router.delete("/{answer_id}", response_model=AnswerRead)
async def delete_answer(answer_id: int, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await QuestionService(db).del_answer(answer_id, user_id)
