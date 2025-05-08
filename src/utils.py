from datetime import datetime, timedelta
import uuid
from src.config import Config
import jwt
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from enum import Enum
from passlib.context import CryptContext
T = TypeVar("T")

class BaseResponseSchema(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None

#BaseResponse Schema Example
"""
class DataSchema(BaseModel):
    id:uuid.UUID
    name:str
    
class ResponseDataSchema(BaseResponseSchema[DataSchema]):
    pass
    
استعمل الكلاس الاخير في الاستجابة متع ال
views او ما تسمي ب routes
"""

ACCESS_TOKEN_EXPIRY = 5000

passwd_context = CryptContext(
    schemes=['bcrypt']
)

def passwordHash(password: str):
    hash = passwd_context.hash(password)
    return hash

def verifyPassword(password: str, hash: str):
    return passwd_context.verify(password, hash)
def createAccessToken(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    paylode = {    "user_id": 1,
    "exp": datetime.utcnow() + timedelta(seconds=60)}

    paylode['user'] = user_data
    paylode['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    paylode['jti'] = str(uuid.uuid4())
    paylode['refresh'] = refresh

    token = jwt.encode(
        payload=paylode,
        key = Config.JWT_SECRET,
        algorithm= Config.JWT_ALGORITHM,
    )

    return token

def decodeToken(token: str):
    try:
        tokenData = jwt.decode(
            jwt = token,
            key= Config.JWT_SECRET,
            algorithms= [Config.JWT_ALGORITHM]
        )
        return tokenData
    except jwt.PyJWTError as e:
        return None