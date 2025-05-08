from datetime import timedelta
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.user.models import  User
from sqlmodel import select
from src.user.scemas import *
from src.utils import *
from src.user.scemas import RegisterUserSchema, UpdateUserSchema
from src.auth.dependencies import *
from datetime import datetime
class UserService:

   async def get_all_users(self, session: AsyncSession):
      statement = select(User)
      result = await session.exec(statement)
      return result.all()
   
   async def create_user(self, user_data: RegisterUserSchema, session: AsyncSession):
   
      user_data.password_hash = passwordHash(user_data.password_hash)
      user_data.super_user = False
      userD = user_data.model_dump()
      nuser = User(**userD)
      session.add(nuser)
      await session.commit()
      await session.refresh(nuser)
      return nuser
      
   async def login(self, u: LoginUserPhone, session: AsyncSession):
    try:
        # البحث عن المستخدم باستخدام رقم الهاتف
        statement = select(User).where(User.phone_number == u.phone_number)
        res = await session.exec(statement)
        user = res.first()

        # التحقق من وجود المستخدم وصحة كلمة المرور
        if not user or not verifyPassword(u.password_hash, user.password_hash):
            raise HTTPException(status_code=403, detail="رقم الهاتف أو كلمة المرور غير صحيحة")

        # إنشاء التوكنات
        access_token = createAccessToken(
            user_data={
                'id': str(user.id),
                'email': user.email,
                'phone_number': user.phone_number
            }
        )
        refresh_token = createAccessToken(
            user_data={
                'id': str(user.id),
                'email': user.email,
                'phone_number': user.phone_number
            },
            expiry=timedelta(2),
            refresh=True
        )

        # تسجيل البيانات التي يتم إرجاعها
        print(f"Access Token: {access_token}")
        print(f"Refresh Token: {refresh_token}")

        return {"access_token": access_token, "refresh_token": refresh_token}

    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء تسجيل الدخول") 
         
         
   async def daleteUser(self, user_uid: str, session:AsyncSession):
      statement = select(User).where(User.id == user_uid)
      results = await session.exec(statement)
      user = results.one_or_none()
      if user!=None:
         await session.delete(user)
         await session.commit()
         return "Done"
      else:
         return None
     
   async def updateUser(self, user_uid: str, updated_data: UpdateUserSchema, session: AsyncSession):
      statement = select(User).where(User.id == user_uid)
      results = await session.exec(statement)
      user = results.first()
      data=updated_data.model_dump()
      if user is not None:
            for key, value in data.items():
               setattr(user, key, value)
            user.password_hash = passwordHash(updated_data.password_hash)
            await session.commit()
            
            return user 
      else:
         return None 
      
   async def get_user(self,user_id:int, session:AsyncSession):
      if isinstance(user_id, str):
         user_id = uuid.UUID(user_id)
      statement = select(User).where(User.id == user_id)
      res = await session.exec(statement=statement)
      return res.first()
  
   async def change_password(s: AsyncSession, email: str, old_password: str, new_password: str):

      statement = select(User).where(User.email == email)
      result = await s.exec(statement)
      user = result.one_or_none() 

      if not user or not verifyPassword(old_password, user.password_hash):
         raise HTTPException(status_code=400, detail="كلمة المرور القديمة غير صحيحة")
      
      user.password_hash = passwordHash(new_password)
      
      s.add(user)     
      await s.commit()  
      
      return {"message": "تم تغيير كلمة المرور بنجاح"}
   
   
   