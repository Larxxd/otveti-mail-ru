from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserCreate, UserRead
from ..models.user import User
from ..crud.user import create_user, read_user
from jose import jwt
from ..config import ALGORITHM, SECRET_KEY
from ..schemas.token import TokenResponse
from .hash_passwords import HashPassword
from datetime import datetime, timedelta

class UserService():
    def __init__(self, db: AsyncSession ):
        self.db = db
    
    async def registration(self, user_reg: UserCreate) -> TokenResponse:
        username = user_reg.name
        result = await self.db.execute(select(User).where(User.name == username))
        if result.scalar_one_or_none():
            raise HTTPException(409, "User already exists!")
        
        created_user =  await create_user(self.db, user_reg)

        expiration = datetime.now() + timedelta(minutes = 15)
        dataload = {"user_id": created_user.id, "exp": expiration}
        token = jwt.encode(dataload, SECRET_KEY,ALGORITHM)

        return TokenResponse(access_token=token,token_type="Bearer",user=UserRead.model_validate(created_user))
        
    # Логин без токена
    async def login(self, user: UserCreate ) -> TokenResponse:
        if user == None:
            raise HTTPException(400, "User is empty!")
        finded_user = await self.db.execute(select(User).where(User.name == user.name))
        result_user = finded_user.scalar_one_or_none()
        if result_user == None:
            raise HTTPException(404, "User not exists!")
        if not HashPassword().check_password(user.password, result_user.password):
            raise HTTPException(401, "Incorrect login or password!")
        
        expiration = datetime.now() + timedelta(minutes = 15)
        dataload = {"user_id": result_user.id, "exp": expiration}
        token = jwt.encode(dataload,SECRET_KEY,ALGORITHM)
        return TokenResponse(access_token=token, token_type="Bearer", user=UserRead.model_validate(result_user))

    # Если есть токен
    async def get_me(self, token: str ) -> UserRead | None:
       
        decoded_token = jwt.decode(token,SECRET_KEY,ALGORITHM)
        user = await read_user(self.db, decoded_token["user_id"])
        
        if user:
            return UserRead.model_validate(user)
        raise HTTPException(400, "User is empty!")

    # Че блять не помню такого

    def create_question(self):
        pass

    def create_answer(self):
        pass