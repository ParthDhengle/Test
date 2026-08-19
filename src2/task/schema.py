from pydantic import BaseModel
from typing import Optional

class TaskSchema(BaseModel):
    title:str
    desc:str
    priority:int
    is_completed:bool
    
class TaskSchemaUpdate(BaseModel):
    title:Optional[str] =None
    desc:Optional[str]=None
    priority:Optional[int]=None
    is_completed:Optional[bool]=None


class TaskResponse(BaseModel):
    id:int
    title:str 
    user_id:int
