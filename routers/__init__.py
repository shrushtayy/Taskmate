from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from schemas import TaskCreate, TaskUpdate
from models import Task

router = APIRouter()

# Get ALL tasks
@router.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks

# Get ONE task
@router.get("/tasks/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    return task

# Create task
@router.post("/tasks")
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task(**task.dict())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

# Update task
@router.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        return {"message": "Task not found"}
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    session.commit()
    session.refresh(db_task)
    return db_task

# Delete task
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        return {"message": "Task not found"}
    session.delete(db_task)
    session.commit()
    return {"message": f"Task {task_id} deleted successfully"}