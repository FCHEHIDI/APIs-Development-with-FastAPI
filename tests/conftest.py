"""
Test configuration and fixtures.
"""
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base
from app.core.security import security
from app.models import User
from app.schemas import UserCreate

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client() -> Generator:
    """Create test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db() -> Generator:
    """Create test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db) -> User:
    """Create test user."""
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password="testpassword123"
    )
    
    hashed_password = security.get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_superuser(db) -> User:
    """Create test superuser."""
    user_data = UserCreate(
        email="admin@example.com",
        username="admin",
        full_name="Admin User",
        password="adminpassword123"
    )
    
    hashed_password = security.get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user) -> dict:
    """Create authentication headers for test user."""
    access_token = security.create_access_token(data={"sub": test_user.username})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def superuser_headers(test_superuser) -> dict:
    """Create authentication headers for test superuser."""
    access_token = security.create_access_token(data={"sub": test_superuser.username})
    return {"Authorization": f"Bearer {access_token}"}
