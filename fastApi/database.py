import os
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from fastApi.services.appeal_operations.models import Base

load_dotenv()  # Load environment variables from.env file

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base.metadata = MetaData(bind=engine)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
