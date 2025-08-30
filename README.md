# 🚀 Professional FastAPI Application

> A comprehensive, production-ready REST API built with FastAPI, demonstrating best practices for modern backend development. This project showcases advanced FastAPI features, clean architecture, and professional development practices suitable for enterprise applications.

**Built by:** Fares Chehidi  
**Email:** fareschehidi7@gmail.com  
**LinkedIn:** [https://www.linkedin.com/in/fares-chehidi](https://www.linkedin.com/in/fares-chehidi)  
**GitHub:** [https://github.com/FCHEHIDI](https://github.com/FCHEHIDI)

## 🎯 Project Overview

This FastAPI application serves as a complete backend solution for user management and content publishing, featuring JWT authentication, CRUD operations, and comprehensive security measures. It's designed to demonstrate proficiency in backend development for potential employers and serves as a template for production applications.

## ⭐ Key Features

### 🔐 Authentication & Security
- **JWT Token Authentication** with automatic expiration
- **Password Hashing** using bcrypt
- **Role-based Access Control** (User/Superuser)
- **Security Headers** and CORS configuration
- **Input Validation** and sanitization

### 📊 Database & ORM
- **SQLAlchemy ORM** with relationship mapping
- **Database Migrations** support (ready for Alembic)
- **Connection Pooling** and transaction management
- **Support for PostgreSQL and SQLite**

### 🛠️ API Features
- **RESTful API Design** following OpenAPI standards
- **Automatic API Documentation** (Swagger/ReDoc)
- **Request/Response Validation** with Pydantic
- **Error Handling** with custom exception handlers
- **Structured Logging** for monitoring and debugging

### 🏗️ Architecture & Code Quality
- **Clean Architecture** with separation of concerns
- **Service Layer Pattern** for business logic
- **Dependency Injection** with FastAPI's DI system
- **Type Hints** throughout the codebase
- **Comprehensive Testing** with pytest

## 📁 Project Structure

```
fastapi_project/
│
├── app/                          # Main application package
│   ├── main.py                   # FastAPI app instance and configuration
│   ├── api/                      # API route handlers
│   │   ├── routes/               # Individual route modules
│   │   │   ├── auth.py           # Authentication endpoints
│   │   │   ├── users.py          # User management endpoints
│   │   │   └── posts.py          # Post management endpoints
│   │   └── dependencies/         # Shared dependencies
│   │       └── auth.py           # Authentication dependencies
│   ├── core/                     # Core application components
│   │   ├── config.py             # Application configuration
│   │   ├── security.py           # Security utilities
│   │   └── database.py           # Database configuration
│   ├── models/                   # SQLAlchemy models
│   │   └── __init__.py           # Database models (User, Post)
│   ├── schemas/                  # Pydantic schemas
│   │   └── __init__.py           # Request/response models
│   ├── services/                 # Business logic layer
│   │   ├── user_service.py       # User operations
│   │   └── post_service.py       # Post operations
│   └── utils/                    # Utility functions
│       └── helpers.py            # Helper functions and logging
│
├── tests/                        # Test suite
│   ├── conftest.py               # Test configuration and fixtures
│   ├── unit/                     # Unit tests
│   │   └── test_auth.py          # Authentication tests
│   └── integration/              # Integration tests
│       └── test_workflows.py     # End-to-end workflow tests
│
├── requirements.txt              # Project dependencies
├── .env.example                  # Environment variables template
├── .env                         # Environment configuration (local)
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip or poetry for package management

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/FCHEHIDI/APIs-Development-with-FastAPI.git
   cd APIs-Development-with-FastAPI
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   cd app
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

## 📖 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/v1/auth/register` | Register new user | None |
| POST | `/api/v1/auth/login` | Login (form data) | None |
| POST | `/api/v1/auth/login/json` | Login (JSON) | None |
| GET | `/api/v1/auth/me` | Get current user | Bearer Token |
| POST | `/api/v1/auth/logout` | Logout | Bearer Token |

### User Management Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/v1/users/` | List all users | Superuser |
| GET | `/api/v1/users/me` | Get current user | Bearer Token |
| GET | `/api/v1/users/{user_id}` | Get user by ID | Superuser |
| PUT | `/api/v1/users/me` | Update current user | Bearer Token |
| PUT | `/api/v1/users/{user_id}` | Update user by ID | Superuser |
| DELETE | `/api/v1/users/{user_id}` | Delete user | Superuser |

### Post Management Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/v1/posts/` | List posts | Optional |
| GET | `/api/v1/posts/my-posts` | Get user's posts | Bearer Token |
| GET | `/api/v1/posts/{post_id}` | Get post by ID | Optional |
| POST | `/api/v1/posts/` | Create post | Bearer Token |
| PUT | `/api/v1/posts/{post_id}` | Update post | Bearer Token (Owner) |
| DELETE | `/api/v1/posts/{post_id}` | Delete post | Bearer Token (Owner) |

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_auth.py -v
```

## 📊 API Usage Examples

### Register a New User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "username": "newuser",
       "full_name": "New User",
       "password": "securepassword123"
     }'
```

### Login and Get Token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login/json" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser",
       "password": "securepassword123"
     }'
```

### Create a Post
```bash
curl -X POST "http://localhost:8000/api/v1/posts/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -d '{
       "title": "My First Post",
       "content": "This is the content of my first post.",
       "is_published": true
     }'
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DATABASE_URL` | Database connection string | `sqlite:///./app.db` |
| `SECRET_KEY` | JWT secret key | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `CORS_ORIGINS` | Allowed CORS origins | `*` |

### Database Configuration

**SQLite (Default)**
```
DATABASE_URL=sqlite:///./app.db
```

**PostgreSQL**
```
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

## 🐳 Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```

## 📈 Performance & Monitoring

### Health Check
The application includes a health check endpoint at `/health` for monitoring purposes.

### Structured Logging
All operations are logged with structured data for easy monitoring and debugging.

### Request Timing
Response times are automatically tracked and included in response headers.

## 🔒 Security Features

- **Password Hashing**: Uses bcrypt with salt
- **JWT Tokens**: Secure token-based authentication
- **CORS Protection**: Configurable CORS policies
- **Input Validation**: Automatic request validation
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **Rate Limiting**: Ready for implementation

## 🧑‍💻 Developer Experience

### Code Quality Tools

```bash
# Format code with Black
black app/ tests/

# Lint code with Flake8
flake8 app/ tests/

# Type checking with MyPy
mypy app/
```

### Database Migrations (Future Enhancement)

Set up Alembic for database migrations:
```bash
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Skills Demonstrated

This project demonstrates proficiency in:

- **FastAPI Framework**: Advanced usage of FastAPI features
- **Database Design**: SQLAlchemy ORM with relationships
- **Authentication**: JWT implementation and security
- **API Design**: RESTful API principles and documentation
- **Testing**: Comprehensive unit and integration testing
- **Code Architecture**: Clean code and separation of concerns
- **Documentation**: Clear and comprehensive documentation
- **Security**: Implementation of security best practices
- **Error Handling**: Robust error handling and validation

## 📞 Contact

For questions or collaboration opportunities, please reach out:

- **Portfolio**: [GitHub Profile](https://github.com/FCHEHIDI)
- **LinkedIn**: [Fares Chehidi](https://www.linkedin.com/in/fares-chehidi)
- **Email**: fareschehidi7@gmail.com

---

*This project serves as a demonstration of professional backend development skills using FastAPI. Built by Fares Chehidi to showcase expertise in modern Python web development, API design, and backend engineering practices.*
