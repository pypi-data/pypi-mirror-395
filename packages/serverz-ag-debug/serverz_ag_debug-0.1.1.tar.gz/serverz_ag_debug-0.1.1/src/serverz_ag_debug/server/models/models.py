
import uuid
from typing import Optional

from sqlalchemy import String, Boolean, Column
from sqlalchemy.dialects.mysql import CHAR # Use CHAR for UUID to store as fixed length string
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from pydantic import BaseModel, Field

from umanager.server.utils import Base # 引入Base

# SQLAlchemy 用户模型
# 使用 SQLAlchemyBaseUserTableUUID 来自动处理 UUID 主键
class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users" # 表名
    
    # 可以在这里添加额外的用户属性
    first_name: str = Column(String(255), nullable=True)
    last_name: str = Column(String(255), nullable=True)
    is_admin: bool = Column(Boolean, default=False)

# Pydantic 模型 (用于请求和响应)
class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_admin: bool = False

    class Config:
        from_attributes = True # updated from orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserUpdate(UserCreate):
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_admin: Optional[bool] = None
