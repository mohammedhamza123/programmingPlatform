from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
import uuid as uuid_pkg


class Task(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True)
    user_id: uuid_pkg.UUID = Field(foreign_key="user.id")
    title: str
    date: Optional[str] = None   
    time: Optional[str] = None
    is_done: bool = False
    user: Optional["User"] = Relationship(back_populates="tasks")
    