import os

from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

PG_DB = os.getenv("PG_DB", "aiohttp_db")
PG_USER = os.getenv("PG_USER", "aiohttp")
PG_PASSWORD = os.getenv("PG_PASSWORD", "1234")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", "5431")

PG_DNS = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_async_engine(PG_DNS)    # Подключение к базе по заданному URL-базы (DNS)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class User(Base):

    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
