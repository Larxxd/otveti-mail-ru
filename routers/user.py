from fastapi import APIRouter, HTTPException, Depends
from schemas.user import UserCreate, UserRead, UserUpdate
from schemas.token import TokenResponse
from crud.user import read_user, update_user
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from services.user_service import UserService

router = APIRouter(
    prefix = "/user",
    tags=["users"]
)

@router.post('/registration', response_model=TokenResponse)
async def registr_user(user: UserCreate, db: AsyncSession=Depends(get_db)):
    return await UserService(db).registration(user)

@router.get('/{user_id}', response_model=UserRead)
async def get_user (user_id: int, db: AsyncSession=Depends(get_db)):
    user = await read_user(db,user_id)
    if user is None:
        raise HTTPException(404, "User not found!!!")
    return user

@router.patch('/{user_id}', response_model=UserRead)
async def edit_user(user_update: UserUpdate, user_id: int, db: AsyncSession=Depends(get_db)):
    user = await update_user(db, user_id, user_update)
    if user is None:
        raise HTTPException(404, "User not found!!!")
    return user