from fastapi import APIRouter, Depends
from ..schemas.user import UserCreate, UserRead, UserUpdate
from ..schemas.token import TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_db, get_current_user
from ..services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.post('/registration', response_model=TokenResponse)
async def registr_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService(db).registration(user)


@router.get("/me", response_model=UserRead)
async def get_me(user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_me(user_id)


@router.patch('/me', response_model=UserRead)
async def edit_user(user_update: UserUpdate, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService(db).patch_user(user_update, user_id)


@router.post("/login", response_model=TokenResponse)
async def login_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService(db).login(user)


@router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_user(user_id)
