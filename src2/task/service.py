from .schema import TaskSchema,TaskSchemaUpdate
from .model import TaskModel
from src2.user.models import UserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException,status


def create_task(data:TaskSchema, db:Session,user:UserModel):
    new_data=TaskModel(
        title=data.title,
        desc=data.desc,
        priority=data.priority,
        is_completed=data.is_completed,
        user_id=user.id
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return new_data


def get_tasks(db:Session,user:UserModel):
    tasks=db.query(TaskModel).filter(TaskModel.user_id==user.id).all()
    return tasks

def get_one_task(id:int,db:Session):
    one_task=db.query(TaskModel).get(id)
    if not one_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return{
        "status":"task found",
        "data":one_task
    }


def update_task(body:TaskSchemaUpdate,id:int,db:Session,user:UserModel):
    one_task=db.query(TaskModel).get(id)
    if not one_task:
        raise HTTPException(404,"task not found")

    if one_task.user_id!=user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="u are not allowed to update this task")

    body=body.model_dump()
    for field,value in body.items():
        setattr(one_task,field,value)

    db.add(one_task)
    db.commit()
    db.refresh(one_task)
    
    return{
        "status":"Task updated",
        "data":one_task
    }


def delete_task(id:int,db:Session):
    one_task=db.query(TaskModel).get(id)
    if not one_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(one_task)
    db.commit()

    return None