from typing import Optional
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    date: Optional[str] = None
    time: Optional[str] = None
class TaskRead(BaseModel):
    id: str
    title: str
    date: Optional[str] = None
    time: Optional[str] = None
    is_done: bool