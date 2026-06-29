from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.question import QuestionCreate, QuestionRead
from ..schemas.answer import AnswerCreate
from ..models.question import Question
from ..models.answer import Answer
from typing import Sequence
from ..crud.question import read_question, read_questions, create_question
from ..crud.answer import create_answer 
class QuestionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_question(self, question: QuestionCreate, user_id: int) -> Question:
        return await create_question(self.db, user_id, question)
    
    async def read_question(self, question_id: int) -> Question | None:
        question =  await read_question(self.db, question_id)
        if question is None:
            raise HTTPException(404, "Question not found!!!")
        return question
    
    async def get_all_questions(self) -> Sequence[Question] | None:
        return await read_questions(self.db)
    
    async def create_answer(self, question_id: int, answer_create: AnswerCreate, user_id: int) -> Answer:
        return await create_answer(self.db, answer_create,question_id,user_id)