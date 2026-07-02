from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Union


class AnswerCreate(BaseModel):
    answer_text: str


class AnswerRead(BaseModel):
    id: int
    user_id: int
    question_id: int
    answer_text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnswerUpdate(BaseModel):
    answer_text: Union[str, None] = None
