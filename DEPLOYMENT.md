# 🚀 Production Deployment Guide

This guide covers deploying the FastAPI Professional API to production environments.

## 📋 Pre-deployment Checklist

### Security
- [ ] Change `SECRET_KEY` to a strong, random key
- [ ] Set `DEBUG=False` in production
- [ ] Configure proper CORS origins (not `*`)
- [ ] Set up HTTPS/TLS certificates
- [ ] Configure trusted hosts
- [ ] Review and set appropriate rate limits

### Database
- [ ] Set up production PostgreSQL database
- [ ] Configure database connection pooling
- [ ] Set up database backups
- [ ] Run database migrations

### Environment
- [ ] Configure production environment variables
- [ ] Set up logging destination (file/service)
- [ ] Configure monitoring and health checks
- [ ] Set up error tracking (Sentry, etc.)

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY app/ ./app/
COPY .env ./

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/fastapi_db
      - SECRET_KEY=your-production-secret-key
      - DEBUG=False
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=fastapi_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
```

## ☁️ Cloud Deployment Options

### 1. AWS Deployment (Recommended)

#### Using AWS ECS with Fargate
```bash
# Build and push to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-west-2.amazonaws.com
docker build -t fastapi-app .
docker tag fastapi-app:latest 123456789.dkr.ecr.us-west-2.amazonaws.com/fastapi-app:latest
docker push 123456789.dkr.ecr.us-west-2.amazonaws.com/fastapi-app:latest

# Deploy using ECS CLI or AWS Console
```

#### AWS RDS for Database
- Set up PostgreSQL RDS instance
- Configure security groups
- Update DATABASE_URL environment variable

### 2. Heroku Deployment

#### Procfile
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### Deployment Commands
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-fastapi-app

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main
```

### 3. DigitalOcean App Platform

#### app.yaml
```yaml
name: fastapi-professional-api
services:
- name: api
  source_dir: /
  github:
    repo: your-username/fastapi-professional-api
    branch: main
  run_command: uvicorn app.main:app --host 0.0.0.0 --port 8080
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DEBUG
    value: "False"
  - key: SECRET_KEY
    value: "your-production-secret-key"
  routes:
  - path: /
databases:
- name: fastapi-db
  engine: PG
  version: "13"
```

## 🔧 Environment Configuration

### Production .env
```bash
# Application
DEBUG=False
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/fastapi_production
DATABASE_ECHO=False

# Security
SECRET_KEY=your-super-secure-production-key-minimum-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (restrict in production)
ALLOWED_HOSTS=["yourdomain.com","www.yourdomain.com"]
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# Rate Limiting
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=3600
```

## 🔍 Monitoring & Logging

### Application Logging
The application uses structured logging with structlog. Configure log aggregation:

```python
# In production, send logs to external service
LOGGING_CONFIG = {
    "level": "INFO",
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/fastapi.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    }
}
```

### Health Monitoring
Set up monitoring for:
- `/health` endpoint
- Database connectivity
- Response times
- Error rates
- Memory/CPU usage

## 📊 Performance Optimization

### Database Optimization
```python
# Connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=300
)
```

### Caching (Redis)
```python
# Add Redis for caching
import redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis_client = redis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
```

## 🛡️ Security Hardening

### HTTPS Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location / {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Security Headers
```python
from fastapi.middleware.security import SecurityHeadersMiddleware

app.add_middleware(
    SecurityHeadersMiddleware,
    hsts_max_age=31536000,
    hsts_include_subdomains=True,
    content_type_options_nosniff=True,
    frame_options_deny=True,
    xss_protection_enabled=True
)
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer (AWS ALB, Nginx)
- Implement database read replicas
- Consider microservices architecture for larger applications

### Vertical Scaling
- Monitor resource usage
- Optimize database queries
- Implement caching strategies
- Use async operations where appropriate

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/ -v
    - name: Code quality checks
      run: |
        black --check app/ tests/
        flake8 app/ tests/
        mypy app/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to production
      run: |
        # Your deployment commands here
        echo "Deploying to production..."
```

---

**🎯 This deployment guide ensures your FastAPI application is production-ready and scalable!**

---

**Built by Fares Chehidi**  
📧 Email: fareschehidi7@gmail.com  
🔗 LinkedIn: https://www.linkedin.com/in/fares-chehidi  
💻 GitHub: https://github.com/FCHEHIDI
