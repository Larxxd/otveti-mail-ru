from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.question import QuestionCreate, QuestionUpdate, QuestionRead
from ..schemas.answer import AnswerCreate, AnswerUpdate, AnswerRead
from ..models.question import Question
from ..models.answer import Answer
from typing import Sequence
from ..crud.question import read_question, read_questions, create_question, update_question, delete_question
from ..crud.answer import create_answer, update_answer, delete_answer, read_answer


class QuestionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_question(self, question: QuestionCreate, user_id: int) -> Question:
        return await create_question(self.db, user_id, question)

    async def read_question(self, question_id: int) -> Question | None:
        question = await read_question(self.db, question_id)
        if question is None:
            raise HTTPException(404, "Question not found!!!")
        return question

    async def get_all_questions(self) -> Sequence[Question] | None:
        return await read_questions(self.db)

    async def create_answer(self, question_id: int, answer_create: AnswerCreate, user_id: int) -> Answer:
        return await create_answer(self.db, answer_create, question_id, user_id)

    async def del_question(self, question_id: int, user_id: int):
        deleted_question = await read_question(self.db, question_id)
        if QuestionRead.model_validate(deleted_question).user_id != user_id:
            raise HTTPException(403, "Access is denied")
        return await delete_question(self.db, question_id)

    async def edit_question(self, question: QuestionUpdate, user_id: int, question_id: int):
        edited_question = await update_question(self.db, question, user_id, question_id)
        if QuestionRead.model_validate(edited_question).user_id != user_id:
            raise HTTPException(403, "Access is denied!")
        return edited_question

    async def edit_answer(self, answer_id: int, answer: AnswerUpdate, user_id: int):
        edited_answer = await update_answer(self.db, answer, user_id, answer_id)
        if AnswerRead.model_validate(edited_answer).user_id != user_id:
            raise HTTPException(403, "Access is denied!")
        return edited_answer

    async def del_answer(self, answer_id: int, user_id: int):
        deleted_answer = await read_answer(self.db, answer_id)
        if AnswerRead.model_validate(deleted_answer).user_id != user_id:
            raise HTTPException(403, "Access is denied")
        return await delete_answer(self.db, answer_id)
