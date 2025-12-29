<div align="center">

# 🎓 ATHENA - AI-Powered Educational Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/cloud/atlas)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-121212?style=for-the-badge)](https://www.langchain.com/)
[![GPU](https://img.shields.io/badge/CUDA-GPU%20Accelerated-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-zone)

**An intelligent educational assistant powered by RAG (Retrieval-Augmented Generation) and GPU-accelerated LLMs**

[Features](#-key-features) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Quiz System](#-quiz-system) • [Architecture](#-architecture)

</div>

---
## Frontend Implementation

👉 [Frontend Repo](https://github.com/ikrammenyaoui/athena-s-learning-hub)

---

## 📖 Overview

**ATHENA** is a production-ready, AI-powered educational backend platform that combines:
- 🤖 **RAG-based AI Assistant** with FAISS vector store and TinyLlama LLM
- 🎯 **Intelligent Quiz Generator** with multi-topic support
- 👥 **Role-Based Access Control** for Students, Teachers, and Admins
- 🚀 **GPU Acceleration** for fast inference
- 🔒 **Enterprise-grade Security** with JWT authentication
- 📚 **Conversation Management** with room-based organization
- 💬 **Real-time Chat** with context-aware responses


---

## 🌟 Key Features

### 🤖 AI-Powered Assistant
- **RAG Technology**: Retrieval-Augmented Generation with FAISS vector search
- **GPU-Accelerated**: TinyLlama LLM with CUDA support (RTX 3050 6GB optimized)
- **Educational Prompts**: Structured, professional academic responses
- **Context-Aware**: Retrieves relevant course material for accurate answers
- **Stateless & Stateful**: Support for both conversation modes

### 📝 Intelligent Quiz System
- **5 Major Topics**: Python, Machine Learning, Deep Learning, NLP, Computer Vision
- **500+ Curated Questions**: Across all difficulty levels
- **Dynamic Generation**: Custom quizzes with 1-50 questions
- **Difficulty Levels**: Easy, Medium, Hard, and Mixed
- **Auto-Grading**: Instant feedback with detailed explanations
- **Performance Tracking**: Score percentages and answer reviews

### 👥 User Management
- **Three Roles**: Students, Teachers, Admins
- **JWT Authentication**: Secure token-based authentication
- **Profile Management**: Role-specific profile customization
- **Bcrypt Hashing**: Industry-standard password security
- **Access Control**: Fine-grained permission system

### 💬 Conversation System
- **Room-Based Organization**: Create and manage conversation rooms
- **Multi-Topic Support**: Organize by subject or purpose
- **Conversation History**: Persistent chat storage
- **Context Preservation**: Maintain conversation flow
- **Search & Filter**: Find conversations easily

### 🏗️ Production-Ready
- **Async/Await**: Full async support with Motor MongoDB driver
- **CORS Enabled**: Ready for frontend integration
- **Error Handling**: Comprehensive error management
- **Input Validation**: Pydantic schemas for all endpoints
- **API Documentation**: Interactive Swagger UI and ReDoc
- **Health Checks**: Monitor system status and GPU availability

---

## 🛠️ Tech Stack

### Core Framework
- **FastAPI** 0.109.0 - Modern, high-performance web framework
- **Python** 3.11+ - With type hints and async support
- **Uvicorn** - ASGI server with auto-reload

### AI & Machine Learning
- **LangChain** - RAG chain orchestration
- **FAISS** - High-performance vector similarity search
- **TinyLlama** 1.1B - Lightweight, GPU-optimized LLM
- **Sentence Transformers** - Embeddings generation
- **PyTorch** - Deep learning framework with CUDA

### Database & Storage
- **MongoDB Atlas** - Cloud NoSQL database
- **Motor** - Async MongoDB driver
- **FAISS Index** - Vector embeddings storage

### Security & Auth
- **python-jose** - JWT token generation/validation
- **passlib** - Password hashing with bcrypt
- **python-multipart** - File upload support

---

## 📁 Project Structure

```
Athena-backend/
├── app/
│   ├── core/                      # Core configuration
│   │   ├── config.py              # Environment settings
│   │   └── security.py            # JWT & auth utilities
│   │
│   ├── db/                        # Database
│   │   └── mongodb.py             # MongoDB connection
│   │
│   ├── models/                    # Data models
│   │   ├── user.py                # User model
│   │   ├── student.py             # Student profile
│   │   ├── teacher.py             # Teacher profile
│   │   └── room.py                # Conversation rooms
│   │
│   ├── schemas/                   # Pydantic schemas
│   │   ├── auth.py                # Auth request/response
│   │   ├── user.py                # User schemas
│   │   ├── student.py             # Student schemas
│   │   ├── teacher.py             # Teacher schemas
│   │   ├── room.py                # Room schemas
│   │   ├── conversation.py        # Conversation schemas
│   │   └── assistant_schema.py    # AI & Quiz schemas
│   │
│   ├── routes/                    # API endpoints
│   │   ├── auth_routes.py         # Authentication
│   │   ├── student_routes.py      # Student operations
│   │   ├── teacher_routes.py      # Teacher operations
│   │   ├── admin_routes.py        # Admin operations
│   │   ├── assistant_routes.py    # AI assistant & quizzes
│   │   ├── conversation_routes.py # Chat history
│   │   ├── rooms_routes.py        # Room management
│   │   └── rag_router.py          # RAG testing
│   │
│   ├── services/                  # Business logic
│   │   ├── model_loader.py        # LLM initialization
│   │   ├── rag_service.py         # RAG orchestration
│   │   ├── quiz_generator.py      # Quiz generation
│   │   ├── rag_loader.py          # FAISS loading
│   │   └── room_service.py        # Room operations
│   │
│   ├── utils/                     # Utilities
│   │   ├── jwt.py                 # JWT operations
│   │   └── password.py            # Password hashing
│   │
│   └── main.py                    # FastAPI application
│
├── documents/                     # Knowledge base
│   ├── python_basics.txt
│   ├── ml_basics.txt
│   ├── dl_basics.txt
│   ├── algorithms.txt
│   └── data_structures.txt
│
├── athena_faiss_index/           # Vector embeddings
│   └── index.faiss
│
├── tests/                        # Test files
│   ├── test_auth.py
│   ├── test_quiz_api.py
│   └── test_comprehensive_rooms.py
│
├── requirements.txt              # Python dependencies
├── rag_requirements.txt          # RAG-specific dependencies
├── download_model.py             # Model downloader
├── install_all.bat              # Windows installer
└── README.md                    # This file
```

---

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- MongoDB Atlas account
- Git

### Step 1: Clone the Repository

```bash
cd backend
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy the example environment file:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

2. Edit `.env` and add your MongoDB URI and generate a secret key:

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

Update `.env`:

```env
MONGO_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=athena_db
SECRET_KEY=your_generated_secret_key_here
```

---

## 🎯 MongoDB Atlas Setup

1. **Create Account**: Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. **Create Cluster**: 
   - Choose FREE tier (M0 Sandbox)
   - Select your preferred cloud provider and region
3. **Create Database User**:
   - Go to "Database Access"
   - Add new user with username and password
4. **Whitelist IP**:
   - Go to "Network Access"
   - Add IP Address (0.0.0.0/0 for development)
5. **Get Connection String**:
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<username>` and `<password>` with your credentials

---

## ▶️ Running the Application

### Development Mode

```bash
# Start the server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Start the server
python -m app.main
```

The API will be available at: **http://localhost:8000**

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register/student` | Register new student | ❌ |
| POST | `/auth/register/teacher` | Register new teacher | ❌ |
| POST | `/auth/register/admin` | Register new admin | ✅ Admin |
| POST | `/auth/login` | Login (all roles) | ❌ |

### Student

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/student/profile` | Get student profile | ✅ Student |
| PUT | `/student/profile/edit` | Update student profile | ✅ Student |

### Teacher

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/teacher/profile` | Get teacher profile | ✅ Teacher |
| PUT | `/teacher/profile/edit` | Update teacher profile | ✅ Teacher |

### Admin

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/admin/users` | Get all users | ✅ Admin |
| GET | `/admin/stats` | Get platform stats | ✅ Admin |
| DELETE | `/admin/user/{id}` | Delete user | ✅ Admin |

---

## 🧪 Example API Requests

### Register Student

```bash
POST /auth/register/student
Content-Type: application/json

{
  "email": "student@example.com",
  "password": "securepass123",
  "firstName": "John",
  "lastName": "Doe",
  "institute": "MIT",
  "year": "3rd",
  "speciality": "Computer Science",
  "phone": "+1234567890",
  "skills": ["Python", "React", "Machine Learning"],
  "bio": "Passionate about AI and education",
  "links": {
    "github": "https://github.com/johndoe",
    "linkedin": "https://linkedin.com/in/johndoe",
    "portfolio": "https://johndoe.dev"
  }
}
```

### Register Teacher

```bash
POST /auth/register/teacher
Content-Type: application/json

{
  "email": "teacher@example.com",
  "password": "securepass123",
  "firstName": "Jane",
  "lastName": "Smith",
  "teaching": "Mathematics",
  "institute": "Harvard University",
  "phone": "+1234567890",
  "availability": {
    "days": ["Monday", "Wednesday", "Friday"],
    "hours": "9:00 AM - 5:00 PM"
  },
  "bio": "20 years of teaching experience"
}
```

### Login

```bash
POST /auth/login
Content-Type: application/json

{
  "email": "student@example.com",
  "password": "securepass123"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "student@example.com",
    "role": "student",
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

### Get Student Profile

```bash
GET /student/profile
Authorization: Bearer <access_token>
```

### Update Student Profile

```bash
PUT /student/profile/edit
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "bio": "Updated bio text",
  "skills": ["Python", "React", "TensorFlow", "Docker"]
}
```

### Admin: Get All Users

```bash
GET /admin/users
Authorization: Bearer <admin_access_token>
```

### Admin: Delete User

```bash
DELETE /admin/user/507f1f77bcf86cd799439011
Authorization: Bearer <admin_access_token>
```

---

## 🔐 Authentication Flow

1. **Register**: User creates account with role-specific information
2. **Login**: User receives JWT access token and refresh token
3. **Access Protected Routes**: Include token in Authorization header
   ```
   Authorization: Bearer <access_token>
   ```
4. **Token Expiration**: Access token expires in 30 minutes
5. **Refresh**: Use refresh token to get new access token (valid for 7 days)

---

## 🛡️ Security Features

- **Bcrypt Password Hashing**: Passwords are never stored in plain text
- **JWT Tokens**: Stateless authentication with signed tokens
- **Role-Based Access Control**: Each endpoint checks user permissions
- **Token Expiration**: Automatic token expiry for security
- **MongoDB Unique Constraints**: Prevents duplicate emails
- **Input Validation**: Pydantic validates all request data
- **CORS Protection**: Configurable allowed origins

---

## ⚙️ Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB Atlas connection string | Required |
| `DATABASE_NAME` | MongoDB database name | `athena_db` |
| `SECRET_KEY` | JWT signing secret key | Required |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | `7` |
| `DEBUG` | Enable debug mode | `False` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `["http://localhost:3000"]` |

---

## 🧰 Dependencies

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
motor==3.3.2
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
email-validator==2.1.0
```

---

## 🐛 Error Handling

The API returns proper HTTP status codes:

- **200 OK**: Successful request
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Invalid or missing authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **409 Conflict**: Duplicate resource (e.g., email already exists)
- **500 Internal Server Error**: Server error

Example error response:

```json
{
  "detail": "Email already registered"
}
```

---

## 🧪 Testing the API

### Using Swagger UI

1. Open http://localhost:8000/docs
2. Try the endpoints directly from the browser
3. Use the "Authorize" button to add JWT token

### Using cURL

```bash
# Register a student
curl -X POST http://localhost:8000/auth/register/student \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "firstName": "Test",
    "lastName": "User",
    "institute": "Test Institute",
    "year": "1st",
    "speciality": "Testing"
  }'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

---

## 📝 Creating First Admin

Since the `/auth/register/admin` endpoint requires admin authentication, you need to manually create the first admin in MongoDB:

### Option 1: Using MongoDB Compass

1. Connect to your MongoDB Atlas cluster
2. Navigate to `athena_db.users` collection
3. Insert document:

```json
{
  "email": "admin@athena.com",
  "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqXqmBN7Jm",
  "role": "admin",
  "createdAt": {"$date": "2025-12-08T00:00:00.000Z"}
}
```

**Note**: The password hash above is for `"admin123"`. Generate your own using:

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("your_password_here"))
```

### Option 2: Using Python Script

Create `create_admin.py`:

```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin():
    client = AsyncIOMotorClient("your_mongo_uri_here")
    db = client.athena_db
    
    admin_doc = {
        "email": "admin@athena.com",
        "password": pwd_context.hash("admin123"),
        "role": "admin",
        "createdAt": datetime.utcnow()
    }
    
    result = await db.users.insert_one(admin_doc)
    print(f"Admin created with ID: {result.inserted_id}")
    client.close()

asyncio.run(create_admin())
```

---

## 🚀 Deployment

### Using Docker (Recommended)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t athena-backend .
docker run -p 8000:8000 --env-file .env athena-backend
```

### Using Railway/Render

1. Push code to GitHub
2. Connect repository to Railway/Render
3. Add environment variables
4. Deploy automatically

---

## 📄 License

MIT License - feel free to use this project for learning or production.

---

## 👨‍💻 Author
**Tasnim Mtir** - **Ikram Menyaoui** - **Aya Mekni** - **Nour Saibi**

---



