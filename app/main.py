from fastapi import FastAPI
from .routers import user, question, answer

app = FastAPI()

app.include_router(user.router)
app.include_router(question.router)
app.include_router(answer.router)
