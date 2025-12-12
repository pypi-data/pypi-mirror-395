
# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import FastAPI, Header


# 模拟获取当前用户的依赖项
async def get_current_user(x_token: str = Header(...)):
    if x_token not in ["1234",
                       "5678"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid X-Token header")
    return {"username": "admin", "roles": ["user", "admin"]}


router = APIRouter(
    tags=["users"],
    dependencies=[Depends(get_current_user)] # 统一的依赖项列表
)


@router.get("/dashboard")
async def get_user(user_info :dict =  Depends(get_current_user)):
    pass
    return {"message": "Welcome to the admin dashboard!"}
