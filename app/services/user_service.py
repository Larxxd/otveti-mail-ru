from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserCreate, UserRead, UserUpdate
from ..models.user import User
from ..crud.user import create_user, read_user, update_user
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
        
    async def login(self, user: UserCreate ) -> TokenResponse:
        finded_user = await self.db.execute(select(User).where(User.name == user.name))
        result_user = finded_user.scalar_one_or_none()
        if result_user == None:
            raise HTTPException(404, "User not exists!")
        if not HashPassword().check_password(user.password, result_user.password):
            raise HTTPException(401, "Incorrect login or password!")
        
        token = self._create_token(result_user.id)
        return TokenResponse(access_token=token, token_type="Bearer", user=UserRead.model_validate(result_user))

    async def get_me(self, user_id: int ) -> UserRead | None:
        user = await read_user(self.db, user_id)
        if user:
            return UserRead.model_validate(user)
        raise HTTPException(400, "User is empty!")

    async def patch_user(self, user: UserUpdate, user_id: int) -> User| None:
        db_updated_user =  await self.db.execute(select(User).where(User.name == user.name))
        updated_user = db_updated_user.scalar_one_or_none()
        if updated_user == None or updated_user.id == user_id:
            return await update_user(self.db, user_id, user)
        raise HTTPException(409, "This name already exists!")
        
    async def get_user(self, user_id: int) -> User | None:
        user = await read_user(self.db,user_id)
        if user is None:
            raise HTTPException(404, "User not found!!!")
        return user
    
    # Че блять не помню такого
    def create_question(self):
        pass

    def create_answer(self):
        pass