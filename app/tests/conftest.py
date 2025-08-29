import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from fastapi.testclient import TestClient
from main import app
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def postgres_container():
    """Spin up Postgres container"""
    with PostgresContainer("postgres:15") as postgres:
        os.environ["DATABASE_URL"] = postgres.get_connection_url()
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    """SQLAlchemy engine bound to the container DB"""
    engine = create_engine(postgres_container.get_connection_url())
    yield engine
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database(engine):
    """Create schema before tests and drop after"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine):
    """Provide a fresh SQLAlchemy session per test"""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session, monkeypatch):
    """FastAPI test client with DB dependency overridden"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Override dependency injection
    from app.db import deps
    app.dependency_overrides[deps.get_db] = override_get_db

    with TestClient(app) as c:
        yield c
