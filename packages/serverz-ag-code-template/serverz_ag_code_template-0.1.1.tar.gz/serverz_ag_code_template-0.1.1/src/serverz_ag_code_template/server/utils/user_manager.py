# user_manager.py
import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
# from fastapi_users_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users.db import SQLAlchemyUserDatabase
from .database import get_async_session

from fastapi import Depends, Request, HTTPException, status # <-- 确保 HTTPException 在这里
from sqlalchemy.exc import IntegrityError # <-- 确保这一行存在

from umanager.server.models.models import User, UserCreate # <--- 在这里添加 UserCreate 的导入

from passlib.context import CryptContext # 确保这里引入了 CryptContext

# ---------- 确保 pwd_context 在模块级别定义 ----------
# 它应该在任何使用它的类或函数之外
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 替换为您的安全密钥，最好从环境变量中获取
SECRET = "YOUR_SUPER_SECRET_KEY_REPLACE_ME" # !!! 重要：在生产环境中，请务必使用环境变量


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    # ... (reset_password_token_secret, verification_token_secret 保持不变)

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> User:
        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )

        hashed_password = pwd_context.hash(user_create.password)

        # 使用 model_dump 获取 Pydantic V2 的字典表示
        user_data = user_create.model_dump(exclude_unset=True)
        user_data["hashed_password"] = hashed_password
        user_data["id"] = uuid.uuid4()

        if "password" in user_data: # 确保移除明文密码
            del user_data["password"]

        # 创建 SQLAlchemy User 实例
        # 这里的 self.user_db.user_table 就是 models.User
        new_user = self.user_db.user_table(**user_data) 
        
        # 确保默认字段被设置
        new_user.is_active = True
        new_user.is_superuser = False
        new_user.is_verified = False

        # created_user = await self.user_db.create(new_user)
        try:
            self.user_db.session.add(new_user)
            await self.user_db.session.commit()
            await self.user_db.session.refresh(new_user) # 刷新以获取可能由数据库生成的字段（如默认值）
        except IntegrityError:
            await self.user_db.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A database integrity error occurred (e.g., duplicate email)."
            )
        # await self.on_after_register(created_user, request)
        # return created_user
        await self.on_after_register(new_user, request) # 这里也是 new_user
        return new_user

async def get_user_db(session = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)



async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


# uv venv .venv --python 3.11 
# python -c "import pydantic; print(pydantic.VERSION)"