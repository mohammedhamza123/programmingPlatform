from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime

from sqlalchemy import or_

from src.user.scemas import *
from src.user.services import *

from src.db import SessionDep
from src.auth.dependencies import GetCurrentUser, RoleChecker
from src.user.models import User
from src.user.scemas import LoginUserPhone, RegisterUserSchema, UpdateUserSchema


user_router = APIRouter()
user_service = UserService()



@user_router.post("/signup")
async def signup(data: RegisterUserSchema, session: AsyncSession = Depends(get_session)):
    return await user_service.create_user(data, session)





@user_router.post("/login")
async def login(u: LoginUserPhone, session: SessionDep):
    new_user = await user_service.login(u, session)

    return new_user


@user_router.get("/aa")
async def GetAllUsers(session: SessionDep):
    users = await user_service.get_all_users(session)

    if not users:
        raise HTTPException(status_code=404, detail="No Users")
    return users

@user_router.get("/user/{user_id}")
async def GetUser(user_id: str, session: SessionDep, current_user: User = Depends(GetCurrentUser)):
    user = await user_service.get_user(user_id, session)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@user_router.delete("/{user_id}")
async def DeleteUser(session: SessionDep, current_user: User = Depends(GetCurrentUser)):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = await user_service.daleteUser(current_user.id, session)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user

@user_router.put("/{user_id}")
async def UpdateUser(data_updated: UpdateUserSchema, session: SessionDep, current_user: User = Depends(GetCurrentUser)):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = await user_service.update_user(current_user.id, data_updated, session)
    if user is None:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        return user

from uuid import UUID

@user_router.get("/users/search")
async def search_users(q: str, session: AsyncSession = Depends(get_session)):
    filters = [
        User.username.contains(q),
        User.email.contains(q),
        User.phone_number.contains(q)
    ]
    # إذا كان q يمثل UUID صحيح أضف شرط البحث بالـ id
    try:
        uuid_q = UUID(q)
        filters.append(User.id == uuid_q)
    except Exception:
        pass

    statement = select(User).where(or_(*filters))
    result = await session.exec(statement)
    return result.all()