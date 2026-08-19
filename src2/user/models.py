from sqlalchemy import Column, Integer,String, Float,Boolean

from src2.utils.db import Base

class UserModel(Base):
    __tablename__="user_table"

    id=Column(Integer,primary_key=True)
    name=Column(String)
    username=Column(String,nullable=False)
    password=Column(String,nullable=False)
    email=Column(String)
    mobile=Column(Integer)

