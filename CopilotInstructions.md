# 📘 CopilotInstructions.md  
**Project Title**: APIs Development with FastAPI  
**Role**: Coding Assistant (VS Code Environment)  
**Objective**: Build scalable, secure, and well-documented RESTful APIs using FastAPI.

---

## 🛠️ Environment Setup

### 1. Prerequisites
- Python 3.10+
- VS Code with the following extensions:
  - Python
  - Pylance
  - FastAPI Snippets (optional)
  - REST Client or Thunder Client (for testing)
- Git (configured with SSH or HTTPS)
- Virtual Environment tool (`venv` or `poetry`)

### 2. Project Initialization
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install --upgrade pip
pip install fastapi uvicorn

fastapi_project/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── routes/
│   │   └── dependencies/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   └── utils/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── requirements.txt
├── .env
└── README.md
