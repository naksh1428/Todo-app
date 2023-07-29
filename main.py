from fastapi import FastAPI, Request, Depends, HTTPException, Query,status
from typing import Optional
from config.dbconnection import engine, sessionLocal, Base
from sqlalchemy.orm import Session
from models import models
from datetime import datetime
import uvicorn
from pydantic import BaseModel
import crud
from schemas.schemas import TaskCreate, UpdateTask, Tasklist
from fastapi.middleware.cors import CORSMiddleware
#from tokenizers import Tokenizer

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="To-Do management API",
    redoc_url=None,
    version="0.0.1",
)
origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


status_dropdown = Query("started", enum=["To-Do", "In-Progress", "Cancelled", "Completed"])
task_type_dropdown = Query("Refinement", enum=["Development", "Testing", "Deployment"])


@app.get("/api/healthchecker")
async def root():
    return {"API": "To do management is LIVE.. "}


@app.post("/api/create-todo", response_model=TaskCreate, status_code=status.HTTP_201_CREATED)
async def create_todo(task_name: str, task_type: str = task_type_dropdown, task_status: str = status_dropdown,
                      assignee: str | None = None, comments: str | None = None, db: Session = Depends(get_db)):
    try:
        created_date = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        return crud.create_task(db, task_name, task_type, task_status, assignee, comments, created_date)

    except Exception as e:
        print(f"Exception Occurred while entering data in to database {e}")


@app.get("/api/get-todo-list")
async def get_todo_list(task_status: str = status_dropdown, db: Session = Depends(get_db)):
    try:
        data = crud.get_task_list(task_status, db)
        return data
    except Exception as e:
        print(f"Exception occurred while extracting task: {e}")


@app.get("/api/all-todo")
async def get_all_todo(db: Session = Depends(get_db)):
    try:
        data = crud.get_all_task_list(db)
        return data
    except Exception as e:
        print(f"Exception Occurred while extracting Completed task list: {e}")


@app.patch("/api/update-todo", status_code=status.HTTP_200_OK)
async def update_todo(new_task: UpdateTask, db: Session = Depends(get_db)):
    try:
        new_date = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        return crud.update_task(db, new_task, new_date)
    except Exception as e:
        print(f"Exception Occurred while extracting Completed task list: {e}")

@app.delete("/api/delete-todo", status_code=status.HTTP_200_OK)
async def delete_todo(task_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_task(task_id, db)
    except Exception as e:
        print(f"Exception Occurred while deleting task: {e}")



@app.get("/api/deleted-do-list", status_code=status.HTTP_200_OK)
async def Archive_task_list(db: Session = Depends(get_db)):
    try:
        return crud.get_archive_task(db)
    except Exception as e:
        print(f"Exception Occurred while deleting task: {e}")

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
    )
