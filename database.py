# database.py
# -*- coding: utf-8 -*-
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker

# PostgreSQL连接配置（根据实际情况修改）
DATABASE_URL = "postgresql://postgres:985050@localhost:5432/postgres"

# 创建异步引擎（需安装 asyncpg 或 psycopg2-binary）
engine = create_engine(
    DATABASE_URL, pool_size=5, max_overflow=10, pool_timeout=30, pool_recycle=1800
)

# 创建本地会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 初始化数据库表（在main.py中调用）
def init_db():
    SQLModel.metadata.create_all(engine)
