import uuid
from src.Task.models import Task
from sqlmodel import select

class TaskService:
    async def add_task(self, user_id: str, title: str, session, date=None, time=None):
        task = Task(user_id=user_id, title=title, date=date, time=time)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    async def delete_task(self, user_id: str, task_id: str, session):
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        if isinstance(task_id, str):
            task_id = uuid.UUID(task_id)
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.exec(statement)
        task = result.first()
        if task:
            await session.delete(task)
            await session.commit()
            return True
        return False

    async def get_tasks(self, user_id: str, session):
        statement = select(Task).where(Task.user_id == user_id)
        result = await session.exec(statement)
        return result.all()