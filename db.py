from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


db_url = "postgresql+asyncpg://postgres:root123@localhost:5432/csv_doc_db"

engine = create_async_engine(
    db_url,
    echo=True
)

async_session = sessionmaker(autoflush=True,bind=engine, class_=AsyncSession)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


Base = declarative_base()