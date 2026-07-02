from pydantic import BaseModel, ConfigDict, Field
from typing import List, Union
from .answer import AnswerRead
from datetime import datetime


class QuestionCreate(BaseModel):
    topic_id: int
    question_text: str
    question_header: str


class QuestionRead(BaseModel):
    id: int
    topic_id: int
    question_text: str
    question_header: str
    user_id: int
    created_at: datetime
    answers: List[AnswerRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class QuestionUpdate(BaseModel):
    question_text: Union[str, None] = Field(default=None, min_length=1)
    question_header: Union[str, None] = Field(default=None, min_length=1)
