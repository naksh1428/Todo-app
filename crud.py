from sqlalchemy.orm import Session
from models.models import Task, ArchiveTask
from fastapi import HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
from http import HTTPStatus


def create_task(db: Session, task_name: str, task_type: str, task_status: str, assignee: str,
                comments: str, created_date: str):
    t1 = Task(task_name=task_name, task_type=task_type, assignee=assignee, task_status=task_status,
              comments=comments, created_date=created_date, updated_date=created_date)
    db.add(t1)
    db.commit()
    db.refresh(t1)
    return t1


def update_task(db:Session, new_task, new_date):
    new_task = new_task.dict(exclude_unset=True)
    db_task = db.query(Task).filter(Task.id == new_task["id"]).first()
    if not db_task:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"Message": "Record Not Found"})
    new_task["updated_date"] = new_date
    for key, value in new_task.items():
        setattr(db_task, key, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_list(task_status: str, db: Session):
    data = db.query(Task).filter(Task.task_status == task_status).all()
    if not data:
        raise HTTPException(status_code=404, detail="No Task..")
    return data


def get_all_task_list(db: Session):
    data = db.query(Task).all()
    if not data:
        raise HTTPException(status_code=404, detail="No Task..")
    return data


def delete_task(task_id: int, db: Session):
    try:
        data = db.query(Task).filter(Task.id == task_id).first()
        if not data:
            return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"Message": "Record Not Found"})

        # insert record to archive table then delete it
        insert_archive_data(data, db)
        db.delete(data)
        db.commit()
    except Exception as e:
        return {
            "error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"
        }
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Message": f"ID: {task_id}, Record Deleted successfully"})


def insert_archive_data(data, db: Session):
    # insert data into archive table
    t1 = ArchiveTask(id=data.id, task_name=data.task_name, task_type=data.task_type, assignee=data.assignee,
                     task_status=data.task_status, comments=data.comments, created_date=data.created_date,
                     updated_date=data.updated_date)
    db.add(t1)
    db.commit()
    db.refresh(t1)


def get_archive_task(db: Session):
    data = db.query(ArchiveTask).all()
    if not data:
        raise HTTPException(status_code=404, detail="No Archive Task..")
    return data
