from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserRead
from models.user import User
from crud.user import create_user, read_user
from jose import jwt
from config import ALGORITHM, SECRET_KEY
from schemas.token import TokenResponse
from .hash_passwords import HashPassword

class UserService():
    def __init__(self, db: AsyncSession ):
        self.db = db
    
    async def registration(self, user_reg: UserCreate) -> TokenResponse:
        username = user_reg.name
        result = await self.db.execute(select(User).where(User.name == username))
        if result.scalar_one_or_none():
            raise HTTPException(409, "User already exists!")
        
        created_user =  await create_user(self.db, user_reg)
        dataload = {"user_id": created_user.id}
        token = jwt.encode(dataload, SECRET_KEY,ALGORITHM)

        return TokenResponse(access_token=token,token_type="Bearer",user=UserRead.model_validate(created_user))
        

    # Проверка наличия юзера в дб. Если он есть, то проверить пароль. Если всё норм то войти
    # Если пароль неправильынй сообщить об ошибке. Если пользователя такого нет
    # то тоже сообщи лол
    async def check_authorization(self, user: UserCreate, token: str = "") -> User | None:
        
        if token != "":
            token_decode = jwt.decode(token, SECRET_KEY,ALGORITHM)
            return await read_user(self.db,token_decode["user_id"])
        
        finded_user = await self.db.execute(select(User).where(User.name == user.name))        
        result_user = finded_user.scalar_one_or_none()
        if not result_user:
            raise HTTPException(404, "User is not exists!")
        if not HashPassword().check_password(user.password,UserCreate.model_validate(finded_user).password):
            raise HTTPException(401, "Incorrect login or password")
        dataload = {"user_id": result_user.id}
        token = jwt.encode(dataload,SECRET_KEY, ALGORITHM)
        
        
    
    # Че блять не помню такого
    def get_current_user(self):
        pass

    def create_question(self):
        pass

    def create_answer(self):
        pass