# database.py
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 您的 MySQL 连接字符串
# 格式：mysql+aiomysql://user:password@host:port/database
# 注意：fastapi_users 的 sqlalchemy 适配器通常需要异步驱动，
# 所以我们使用 `aiomysql` (虽然你安装的是 mysql-connector-python，
# 但为了异步，我们实际会用 aiomysql，请确保安装它：pip install aiomysql)
DATABASE_URL = "mysql+aiomysql://root:1234@localhost:3306/prompts"

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# 创建所有定义的表（在应用启动时调用）
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
