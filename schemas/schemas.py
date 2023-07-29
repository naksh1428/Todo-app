from pydantic import BaseModel


class TaskCreate(BaseModel):
    id: int
    task_name: str
    task_type: str
    assignee: str
    task_status: str
    comments: str
    created_date: str

    class Config:
        orm_mode = True


class UpdateTask(BaseModel):
    id: int
    task_name: str
    task_type: str
    assignee: str
    task_status: str
    comments: str

    class Config:
        orm_mode = True


class Tasklist(BaseModel):
    task_name: str
    task_type: str
    assignee: str
    task_status: str
    comments: str
    created_date: str
    updated_date: str

    class Config:
        orm_mode = True

