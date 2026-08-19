import jwt
from src2.user.schema import UserSchema,UserLogin
from sqlalchemy.orm import Session
from src2.user.models import UserModel
from fastapi import HTTPException,status,Request
from pwdlib import PasswordHash
import jwt
from src2.utils.config import config
from datetime import datetime,timedelta
from src2.utils.mail import simple_send
from fastapi import BackgroundTasks

password_hash=PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)


async def register(body:UserSchema,bg_task:BackgroundTasks,db:Session):
    print(body)
    #user_name validation
    is_user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if is_user:
        raise HTTPException(400,"user_name already exist")

    #email validation
    is_email=db.query(UserModel).filter(UserModel.email==body.email).first()
    if is_email:
        raise HTTPException(400,"email already exist")

    #password
    hash_password=get_password_hash(body.password)

    new_user=UserModel(
        name=body.name,
        username=body.username,
        password=hash_password,
        email=body.email,
        mobile=body.mobile
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    bg_task.add_task(simple_send,[new_user.email])

    return new_user


def login_user(body:UserLogin, db:Session):
    #check username 
    user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User Not found")

    #check password
    if not verify_password(body.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Password didnt matched")

    #return jwt
    exp_time=(datetime.now()+timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
    token=jwt.encode({"_id":user.id,"username":user.username,"exp":exp_time},config.SECRET_KEY,config.ALGORITHM)

    return {"token":token}


def is_authenticated(request:Request,db:Session):
    try:
        token=request.headers.get("authorization")
        if not token:
            raise HTTPException(401,"login required")
        
        token=token.split(" ")[-1]
        print(config.ACCESS_TOKEN_EXPIRE_MINUTES)
        print(datetime.now().timestamp())
        data=jwt.decode(token,config.SECRET_KEY,config.ALGORITHM)
        print(data)
        user_id=data.get("_id")

        user=db.query(UserModel).filter(UserModel.id==user_id).first()
        if not user:
            raise HTTPException(401,"User not found")
        return user
    except Exception:
        raise HTTPException(401,"You are unauthorized")
