from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:////root/py_proj/cat_bot/db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    user_status: Mapped[str] = mapped_column(String(25))
    user_photo: Mapped[int] = mapped_column(primary_key=False)
    user_video: Mapped[int] = mapped_column(primary_key=False)

class Photo(Base):
    __tablename__ = 'photos'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(255))

class Video(Base):
    __tablename__ = 'videos'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(255))

class Photo_approve(Base):
    __tablename__ = 'photos_approve'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(255))

class Video_approve(Base):
    __tablename__ = 'videos_approve'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(255))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)