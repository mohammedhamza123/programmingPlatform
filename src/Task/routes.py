from fastapi import APIRouter, Depends
from src.Task.services import TaskService
from src.Task.scemas import TaskCreate
from src.db import get_session
from src.auth.dependencies import GetCurrentUser

router = APIRouter()

@router.get("/api/tasks")
async def get_tasks(user=Depends(GetCurrentUser), session=Depends(get_session)):
    service = TaskService()
    return await service.get_tasks(user.id, session)

@router.post("/api/tasks")
async def add_task(data: TaskCreate, user=Depends(GetCurrentUser), session=Depends(get_session)):
    service = TaskService()
    return await service.add_task(user.id, data.title, session, data.date, data.time)

@router.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str, user=Depends(GetCurrentUser), session=Depends(get_session)):
    service = TaskService()
    return await service.delete_task(user.id, task_id, session)