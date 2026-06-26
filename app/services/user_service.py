from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserCreate, UserRead
from ..models.user import User
from ..crud.user import create_user, read_user
from jose import jwt
from ..settings import settings
from ..schemas.token import TokenResponse
from .hash_passwords import HashPassword
from datetime import datetime, timedelta

class UserService():
    def __init__(self, db: AsyncSession ):
        self.db = db
    
    def _create_token(self, user_id: int) -> str:
        expiration = datetime.now() + timedelta(minutes = 15)
        dataload = {"user_id": user_id, "exp": expiration}
        token = jwt.encode(dataload, settings.secret_key,settings.algorithm)

        return token

    async def registration(self, user_reg: UserCreate) -> TokenResponse:
        username = user_reg.name
        result = await self.db.execute(select(User).where(User.name == username))
        if result.scalar_one_or_none():
            raise HTTPException(409, "User already exists!")
        
        created_user =  await create_user(self.db, user_reg)
        token = self._create_token(created_user.id)
        

        return TokenResponse(access_token=token,token_type="Bearer",user=UserRead.model_validate(created_user))
        
    # Логин без токена
    async def login(self, user: UserCreate ) -> TokenResponse:
        finded_user = await self.db.execute(select(User).where(User.name == user.name))
        result_user = finded_user.scalar_one_or_none()
        if result_user == None:
            raise HTTPException(404, "User not exists!")
        if not HashPassword().check_password(user.password, result_user.password):
            raise HTTPException(401, "Incorrect login or password!")
        
        token = self._create_token(result_user.id)

        return TokenResponse(access_token=token, token_type="Bearer", user=UserRead.model_validate(result_user))

    # Выбрать себя с токеном
    async def get_me(self, user_id: int ) -> UserRead | None:
       
        user = await read_user(self.db, user_id)
        
        if user:
            return UserRead.model_validate(user)
        raise HTTPException(400, "User is empty!")

    # Че блять не помню такого

    def create_question(self):
        pass

    def create_answer(self):
        pass