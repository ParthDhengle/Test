from fastapi import Request, HTTPException,status,Depends
from sqlalchemy.orm import Session
from src2.utils.config import config
from src2.utils.db import get_db
import jwt
from src2.user.models import UserModel

def is_authenticated(request:Request,db:Session=Depends(get_db)):
    token=request.headers.get('authorization')
    if not token:
        raise HTTPException(status_code=401,detail="No token")

    token=token.split(" ")[-1]
    try:
        data=jwt.decode(token,config.SECRET_KEY,config.ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="session id expired login again")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid token")


    user_id=data.get("_id")
    username=data.get("username")

    #validate user
    user=db.query(UserModel).filter(UserModel.id==user_id and UserModel.username==username).first()
    if not user:
        raise HTTPException(401,detail="No User found")

    return user