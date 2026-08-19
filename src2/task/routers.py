from fastapi import APIRouter,Depends,status
from .service import create_task,get_tasks,get_one_task,update_task,delete_task
from .schema import TaskSchema,TaskSchemaUpdate, TaskResponse
from src2.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session
from src2.utils.helper import is_authenticated
from src2.user.models import UserModel

task=APIRouter(prefix="/task")


@task.post("/create_task2",status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def createTask(data:TaskSchema,db:Session=Depends(get_db) , user:UserModel=Depends(is_authenticated)):
    return create_task(data,db,user)

@task.get('/get_tasks',status_code=status.HTTP_200_OK, response_model=List[TaskResponse])
def get_tasks_route(db:Session=Depends(get_db), user:UserModel=Depends(is_authenticated)):
    return get_tasks(db,user)

@task.get("/get_one_task/{task_id}",status_code=status.HTTP_200_OK)
def get_one_task_route(task_id:int,db:Session=Depends(get_db), user:UserModel=Depends(is_authenticated)):
    return get_one_task(task_id,db)

@task.put("/update_task/{id}",status_code=status.HTTP_201_CREATED)
def update_task_route(body:TaskSchemaUpdate,id,db:Session=Depends(get_db), user:UserModel=Depends(is_authenticated)):
    return update_task(body,id,db,user)

@task.delete("/delete_task/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task_route(id:int,db:Session=Depends(get_db), user:UserModel=Depends(is_authenticated)):
    return delete_task(id,db)