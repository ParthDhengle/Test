from fastapi import FastAPI
from src2.task.routers import task
from src2.utils.db import Base,engine
from src2.user.routers import user_routes


Base.metadata.create_all(engine)

app=FastAPI()

app.include_router(task)
app.include_router(user_routes)

@app.get('/')
def home():
    return{
        "status":"this is home!! welcome"
    }

