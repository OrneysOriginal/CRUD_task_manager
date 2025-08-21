import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.database import Base, get_async_session
from src.main import app
from httpx import AsyncClient

from src.task.models import Task

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

AsyncTestingSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest_asyncio.fixture(scope="session")
async def test_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session(test_db):
    async with AsyncTestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def override_get_db(db_session):
    async def _override_get_db():
        try:
            yield db_session
        finally:
            await db_session.close()

    app.dependency_overrides[get_async_session] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def async_client(override_get_db):
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest_asyncio.fixture(autouse=True)
async def prepopulate_database(db_session):
    """Фикстура для предварительного заполнения БД данными"""
    test_user = Task(
        uuid=0,
        name="cool",
        description="cool",
        status="in_work",
    )
    db_session.add(test_user)
    await db_session.commit()

    yield

    await db_session.delete(test_user)
    await db_session.commit()
