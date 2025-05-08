from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from typing import List, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db import get_session
from src.redis_utils import TokenInBlackList
from src.user.models import User
from src.utils import decodeToken

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error= True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        creds = await super().__call__(request)

        token = creds.credentials
        token_data = decodeToken(token)

        if not self.tokenValid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Token is InVaild or Expired")
            
        if await TokenInBlackList(token_data['jti']):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="token is InValid or has been Revoked")
            
        self.verify_token_data(token_data)

        return token_data

    def tokenValid(self, token) -> bool:
        isValid = decodeToken(token)
        return isValid is not None

    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="please provide an access token")

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="please provide an refresh token")

async def GetCurrentUser(token_details: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    from src.user.services import UserService 
    user_service = UserService()
    user_service = UserService()
    user_id = token_details['user']['id']
    user = await user_service.get_user(user_id, session)
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(GetCurrentUser)) -> Any:
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action."
        )