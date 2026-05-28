from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import user
from db.database import get_db
from schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["用户"])


#用户注册
@router.post("/register")
async def create_user(
        user_data:UserCreate,
        db:AsyncSession = Depends(get_db)
):

    try:
        new_user = await user.create_user(db,user_data)

        return {
            "code": 200,
            "message": "注册成功",
            "data": {
                "user_id": new_user.id,
                "username": new_user.username,
            }
        }

    except Exception as e:
        return {
            "code": 500,
            "message": f"注册失败: {str(e)}",
            "data": None
        }


#用户登录
@router.post("/login")
async def user_login(
        user_data:UserCreate,
        db:AsyncSession = Depends(get_db)
):
    user_login = await user.login_user(db,user_data.username,user_data.password)

    if not user_login:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "user_id": user_login.id,
            "username": user_login.username,
        }
    }