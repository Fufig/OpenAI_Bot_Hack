from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy import BigInteger, String, Integer, ForeignKey, Text, TIMESTAMP, func
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, unique=True, nullable=False)

class Counter(Base):
    __tablename__ = "counter"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    message_count = mapped_column(Integer, default=0, nullable=False)

class History(Base):
    __tablename__ = 'history'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    message = mapped_column(Text, nullable=False)
    response = mapped_column(Text, nullable=True)
    timestamp = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())

async def async_main():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Error occurred during table creation or connection: {e}")