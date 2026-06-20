from .database import AsyncSessionLocal
from fastapi import Header
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from .settings import settings
from fastapi import HTTPException

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(authorization: str = Header(...)):
    try:
        return jwt.decode(authorization.split()[1],settings.secret_key, settings.algorithm)["user_id"]
    except(ExpiredSignatureError):
        raise HTTPException(401, "Invalid token!")