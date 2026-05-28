from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserCreate
from utils.auth import verify_password, hash_password


#根据用户名获取用户信息
async def get_user(
        db:AsyncSession,
        username:str
):
    sttm = select(User).where(User.username == username)
    result = await db.execute(sttm)

    return result.scalar_one_or_none()

#用户注册
async def create_user(
        db: AsyncSession,
        data:UserCreate,
):
    existing = await get_user(db, data.username)

    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")

    hashed_password = hash_password(data.password)
    result = User(username=data.username, password=hashed_password)

    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result

#用户登录
async def login_user(
        db: AsyncSession,
        username: str,
        password: str
):
    sttm = await get_user(db,username)
    if not sttm:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    valid = verify_password(password, sttm.password)

    if not valid:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    return sttm

