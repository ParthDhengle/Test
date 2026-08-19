from src2.user import service
from fastapi import APIRouter,Depends,status,Request,BackgroundTasks
from sqlalchemy.orm import Session
from src2.utils.db import get_db
from src2.user.schema import UserSchema,UserResponse,UserLogin
from src2.utils.helper import is_authenticated


user_routes=APIRouter(prefix="/user")

@user_routes.post("/register",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def register_route(body:UserSchema,bg_task:BackgroundTasks,db:Session=Depends(get_db)):
    return await service.register(body,bg_task,db)

@user_routes.post("/login",status_code=status.HTTP_200_OK)
def user_login_route(body:UserLogin,db:Session=Depends(get_db)):
    return service.login_user(body,db)

@user_routes.get("/is_auth",status_code=status.HTTP_200_OK,response_model=UserResponse)
def is_auth(request:Request,db:Session=Depends(get_db)):
    return is_authenticated(request,db)