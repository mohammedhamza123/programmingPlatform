from pydantic import BaseModel
from src.utils import BaseResponseSchema



class RegisterUserSchema(BaseModel):
      username: str
      email:str
      password_hash:str
      phone_number:str
      super_user: bool = False
       
      
class UpdateUserSchema(BaseModel):
      email:str
      password_hash:str
      phone_number:str
class ResponseRegister(BaseResponseSchema[RegisterUserSchema]):
    pass    
    
class LoginUserEmail(BaseModel):
    email:str
    password_hash:str
class ResponseLoginUserEmail(BaseResponseSchema[LoginUserEmail]):
    pass
class LoginUserPhone (BaseModel):
    phone_number:str
    password_hash:str

class ResponseLoginUserPhone(BaseResponseSchema[LoginUserPhone]):
    pass

