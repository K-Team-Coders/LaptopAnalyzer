import os
from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from fastApi.services.appeal_operations.models import Base

load_dotenv()  # Load environment variables from .env file

# Fetching environment variables
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")

# Database URL in synchronous mode
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

# Create a synchronous SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a synchronous session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bind the engine to Base's metadata
Base.metadata = MetaData(bind=engine)


# Synchronous database session generator
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
