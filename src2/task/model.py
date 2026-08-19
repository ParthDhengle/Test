from sqlalchemy import Column,Integer,String,Float,Boolean, ForeignKey
from src2.utils.db import Base

class TaskModel(Base):
    __tablename__="Task_table"

    id=Column(Integer,primary_key=True)
    title=Column(String)
    desc=Column(String)
    priority=Column(Integer,default="3")
    is_completed=Column(Boolean,default=False)

    user_id=Column(Integer,ForeignKey("user_table.id",ondelete="CASCADE"))


    