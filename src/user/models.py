from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
import uuid as uuid_pkg



class User(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    phone_number: str = Field(unique=True, index=True)
    password_hash: str
    tasks: List["Task"] = Relationship(back_populates="user")
    
