# 🎓 ATHENA – AI-Powered Educational Platform

**FastAPI • Python • MongoDB • LangChain • FAISS • GPU**

An intelligent, production-ready educational backend platform powered by **RAG (Retrieval-Augmented Generation)** and **GPU-accelerated LLMs**.  
ATHENA turns raw course content into **interactive tutoring, quizzes, and analytics** for students, teachers, and admins.

> 🧠 _“Your always-on teaching assistant, quiz engine, and learning companion – in one backend.”_

---

## 📖 Table of Contents

1. [Overview](#-overview)
2. [Key Features](#-key-features)
   - [AI-Powered Assistant](#-ai-powered-assistant)
   - [Intelligent Quiz System](#-intelligent-quiz-system)
   - [User & Role Management](#-user-management)
   - [Conversation System](#-conversation-system)
   - [Production-Ready Backend](#-production-ready)
3. [Architecture](#-architecture)
4. [Tech Stack](#-tech-stack)
5. [Project Structure](#-project-structure)
6. [Screenshots & Demos](#-screenshots--demos)
7. [Installation & Setup](#-installation)
   - [Environment Configuration](#-configure-environment-variables)
   - [MongoDB Atlas Setup](#-mongodb-atlas-setup)
8. [Running the Application](#️-running-the-application)
9. [API Documentation & Endpoints](#-api-documentation)
10. [Example API Requests](#-example-api-requests)
11. [Authentication Flow](#-authentication-flow)
12. [Security Features](#️-security-features)
13. [Environment Variables Reference](#-environment-variables-reference)
14. [Error Handling](#-error-handling)
15. [Testing the API](#-testing-the-api)
16. [Creating the First Admin](#-creating-first-admin)
17. [Deployment](#-deployment)
18. [Roadmap & Ideas](#-roadmap--ideas)
19. [Contributing](#-contributing)
20. [License](#-license)
21. [Authors](#-author)

---

## 📖 Overview

**ATHENA** is an AI-enhanced educational backend built for **real-world use in schools, universities, and online learning platforms**. It combines:

- 🤖 **RAG-based AI Assistant** with FAISS vector store and TinyLlama LLM  
- 📝 **Intelligent Quiz Generator** with multi-topic, multi-difficulty support  
- 👥 **Role-Based Access Control (RBAC)** for Students, Teachers, and Admins  
- 🚀 **GPU Acceleration** for low-latency inference  
- 🔒 **Enterprise-Grade Security** based on JWT and hashed passwords  
- 💬 **Room-Based Conversation Management** with persistent chat history  

ATHENA is designed to be:

- **Modular:** Clear separation between routes, services, models, and schemas  
- **Scalable:** MongoDB Atlas + FAISS + async FastAPI stack  
- **Production-Ready:** Health checks, error handling, input validation, and Docker support  

---

## 🌟 Key Features

### 🤖 AI-Powered Assistant

- **RAG Technology:** Retrieval-Augmented Generation with **FAISS** vector search
- **GPU-Accelerated Inference:**  
  - TinyLlama 1.1B LLM, optimized for **CUDA** (e.g. RTX 3050 6GB)
- **Educationally Tuned Prompts:**  
  - Structured, academic-style explanations  
  - Encourages understanding, not just answers
- **Context-Aware Responses:**  
  - Retrieves relevant course material from `documents/`  
  - Uses similarity search to ground answers
- **Stateless & Stateful Modes:**  
  - One-off question answering  
  - Persistent, room-based conversations

---

### 📝 Intelligent Quiz System

- **Major Topics Covered:**
  - Python
  - Machine Learning
  - Deep Learning
  - NLP
  - Computer Vision
- **Question Bank:**
  - 500+ curated questions  
  - Multiple difficulty levels
- **Dynamic Quiz Generation:**
  - Create quizzes with **1–50 questions**
  - Choose topic(s) and difficulty (Easy, Medium, Hard, Mixed)
- **Auto-Grading:**
  - Instant scoring
  - Detailed feedback and explanations
- **Performance Tracking:**
  - Score percentages
  - Correct / incorrect breakdown  
  - Ideal for building dashboards on the frontend

---

### 👥 User Management

- **Three Roles:**
  - `student`
  - `teacher`
  - `admin`
- **Authentication & Identity:**
  - JWT-based authentication (access + refresh tokens)
  - Unique emails enforced in MongoDB
- **Profile Management:**
  - Role-specific fields (skills, institute, availability, etc.)
- **Security:**
  - **Bcrypt hashing** for passwords (via `passlib`)
  - Centralized **JWT utilities** for signing and verification
- **Fine-Grained Access Control:**
  - Route-level permission checks based on role

---

### 💬 Conversation System

- **Room-Based Chat:**
  - Conversation rooms grouped by subjects, courses, or projects
- **Persistent History:**
  - Stores full conversation logs in MongoDB
- **Context Preservation:**
  - AI assistant can use previous messages for better responses
- **Search & Filter:**
  - Easily find past conversations by room or topic

---

### 🏗️ Production-Ready

- **Async/Await Everywhere:**
  - Built on FastAPI async routes
  - Uses **Motor** for async MongoDB operations
- **CORS Enabled:**
  - Ready to connect with your frontend SPA
- **Robust Error Handling:**
  - Consistent HTTP status codes
  - Human-readable error messages
- **Input Validation:**
  - Pydantic v2 schemas for all request/response objects
- **API Documentation:**
  - Interactive **Swagger UI** (`/docs`)
  - Alternative **ReDoc** (`/redoc`)
- **Health Checks:**
  - API health endpoint
  - GPU availability checks (where applicable)

---

## 🧬 Architecture

At a high level:

```text
Clients (Web / Mobile / LMS)
        │
        ▼
   [ FastAPI Backend ]
        │
        ├── Authentication & RBAC
        ├── AI Assistant (RAG + LLM)
        ├── Quiz Engine
        ├── Conversation Rooms
        │
        ▼
  MongoDB Atlas  (users, profiles, rooms, quizzes, history)
        │
        ▼
  FAISS Index    (vector embeddings for course content)
        │
        ▼
  TinyLlama LLM  (GPU-accelerated inference via PyTorch)
```

- **Services layer** encapsulates business logic:
  - `model_loader.py`, `rag_service.py`, `quiz_generator.py`, `room_service.py`
- **Routes layer** exposes clean, documented REST APIs
- **Schemas layer** enforces request & response contracts

---

## 🛠️ Tech Stack

### Core Framework

- **FastAPI** `0.109.0` – High-performance async web framework
- **Python** `3.11+` – Modern Python with type hints
- **Uvicorn** – ASGI server with auto-reload

### AI & Machine Learning

- **LangChain** – RAG orchestration
- **FAISS** – Vector similarity search
- **TinyLlama 1.1B** – Lightweight, GPU-optimized LLM
- **Sentence Transformers** – Embedding generation
- **PyTorch** – Deep learning framework with CUDA support

### Database & Storage

- **MongoDB Atlas** – Fully-managed NoSQL database
- **Motor** – Async MongoDB driver
- **FAISS Index** – Vector storage for document embeddings

### Security & Auth

- **python-jose** – JWT signing and verification
- **passlib[bcrypt]** – Secure password hashing
- **python-multipart** – File uploads
- **email-validator** – Email validation

---

## 📁 Project Structure

```text
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
├── install_all.bat               # Windows installer
└── README.md                     # This file
```

---

## 🖼️ Screenshots & Demos

![WhatsApp Image 2025-12-23 at 16 02 30](https://github.com/user-attachments/assets/733ed339-1a58-44bf-95e4-92d4ab6fdc85)
![WhatsApp Image 2025-12-23 at 16 04 56](https://github.com/user-attachments/assets/3275dc8e-83a3-4664-8c30-a96d4635361f)
![WhatsApp Image 2025-12-23 at 16 06 48](https://github.com/user-attachments/assets/fd5232b3-1c5f-4712-8894-00d8cb90eb76)
![WhatsApp Image 2025-12-23 at 16 06 11](https://github.com/user-attachments/assets/229fabe1-7456-4100-9107-475bd46dc385)
![WhatsApp Image 2025-12-23 at 16 07 32](https://github.com/user-attachments/assets/a15a05e3-744d-4a02-a167-8bf7f6beff8e)
![WhatsApp Image 2025-12-23 at 16 07 32](https://github.com/user-attachments/assets/028fe02f-b70a-4f01-b4e3-c9546dad2ee6)
![WhatsApp Image 2025-12-23 at 16 10 37](https://github.com/user-attachments/assets/d497c30e-c63c-42b1-af84-77e8a0007cbd)
<img width="1587" height="2245" alt="Flyer-2" src="https://github.com/user-attachments/assets/a683aa5c-7321-432a-9349-07dc568fb7bd" />


---

## 📦 Installation

### Prerequisites

- **Python** 3.11 or higher  
- **MongoDB Atlas** account  
- **Git**  
- (Optional) **NVIDIA GPU + CUDA** for TinyLlama acceleration

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/athena-backend.git
cd athena-backend
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

*(Optionally, for RAG-specific experiments:)*

```bash
pip install -r rag_requirements.txt
```

---

### Step 4: Configure Environment Variables

Copy the example environment file:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Generate a secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Update `.env`:

```env
MONGO_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=athena_db
SECRET_KEY=your_generated_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=False
ALLOWED_ORIGINS=["http://localhost:3000"]
```

---

## 🎯 MongoDB Atlas Setup

1. **Create Account:**  
   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas)

2. **Create Cluster:**
   - Choose **FREE (M0)** tier
   - Select your preferred cloud provider and region

3. **Create Database User:**
   - Go to **“Database Access”**
   - Add a new user with username and password

4. **Whitelist IP:**
   - Go to **“Network Access”**
   - Add IP Address (`0.0.0.0/0` for development)

5. **Get Connection String:**
   - Click **“Connect”** on your cluster
   - Choose **“Connect your application”**
   - Copy the connection string and paste it into `MONGO_URI`  
     (replace `<username>` and `<password>`)

---

## ▶️ Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
python -m app.main
```

The API will be available at:

- API Base: `http://localhost:8000`
- API Docs (Swagger): `http://localhost:8000/docs`
- Alternative Docs (ReDoc): `http://localhost:8000/redoc`
- Health Check: `http://localhost:8000/health`

---

## 📚 API Documentation

The API is fully documented with **OpenAPI**:

- **Interactive Docs (Swagger UI):**  
  - Try endpoints  
  - Authorize with JWT tokens  
  - See schema definitions

- **ReDoc UI:**  
  - Clean, single-page reference for all APIs

---

## 📚 API Endpoints

### 🔑 Authentication

| Method | Endpoint                    | Description              | Auth Required |
|--------|-----------------------------|--------------------------|--------------|
| POST   | `/auth/register/student`    | Register new student     | ❌           |
| POST   | `/auth/register/teacher`    | Register new teacher     | ❌           |
| POST   | `/auth/register/admin`      | Register new admin       | ✅ Admin     |
| POST   | `/auth/login`               | Login (all roles)        | ❌           |

---

### 🎓 Student

| Method | Endpoint                   | Description              | Auth Required |
|--------|----------------------------|--------------------------|--------------|
| GET    | `/student/profile`         | Get student profile      | ✅ Student   |
| PUT    | `/student/profile/edit`    | Update student profile   | ✅ Student   |

---

### 🧑‍🏫 Teacher

| Method | Endpoint                   | Description              | Auth Required |
|--------|----------------------------|--------------------------|--------------|
| GET    | `/teacher/profile`         | Get teacher profile      | ✅ Teacher   |
| PUT    | `/teacher/profile/edit`    | Update teacher profile   | ✅ Teacher   |

---

### 🛡️ Admin

| Method | Endpoint                   | Description              | Auth Required |
|--------|----------------------------|--------------------------|--------------|
| GET    | `/admin/users`             | Get all users            | ✅ Admin     |
| GET    | `/admin/stats`             | Get platform stats       | ✅ Admin     |
| DELETE | `/admin/user/{id}`         | Delete user              | ✅ Admin     |

> ⚙️ Additional endpoints exist for **assistant**, **quiz**, **rooms**, and **conversations** in the `assistant_routes.py`, `rooms_routes.py`, and `conversation_routes.py` modules.

---

## 🧪 Example API Requests

### Register Student

```http
POST /auth/register/student
Content-Type: application/json
```

```json
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

---

### Register Teacher

```http
POST /auth/register/teacher
Content-Type: application/json
```

```json
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

---

### Login

```http
POST /auth/login
Content-Type: application/json
```

```json
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

---

### Get Student Profile

```http
GET /student/profile
Authorization: Bearer <access_token>
```

---

### Update Student Profile

```http
PUT /student/profile/edit
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "bio": "Updated bio text",
  "skills": ["Python", "React", "TensorFlow", "Docker"]
}
```

---

### Admin: Get All Users

```http
GET /admin/users
Authorization: Bearer <admin_access_token>
```

---

### Admin: Delete User

```http
DELETE /admin/user/507f1f77bcf86cd799439011
Authorization: Bearer <admin_access_token>
```

---

## 🔐 Authentication Flow

1. **Register**
   - User registers with role-specific data
2. **Login**
   - Receives **access token** (short-lived) and **refresh token** (longer-lived)
3. **Access Protected Routes**
   - Include token in the `Authorization` header:
     ```http
     Authorization: Bearer <access_token>
     ```
4. **Token Expiration**
   - Access token: ~30 minutes  
   - Refresh token: ~7 days
5. **Refresh**
   - Use refresh token to obtain a new access token (endpoint depending on your implementation)

---

## 🛡️ Security Features

- **Bcrypt Password Hashing**
  - Passwords are **never stored in plain text**
- **JWT Tokens**
  - Stateless authentication with signed tokens
- **Role-Based Access Control**
  - Route-level checks for `student`, `teacher`, and `admin`
- **Token Expiry**
  - Automatic token invalidation after configurable lifetimes
- **MongoDB Constraints**
  - Unique email per user
- **Input Validation**
  - Pydantic schemas validate all payloads
- **CORS Protection**
  - Configurable allowed origins via environment variables

---

## ⚙️ Environment Variables Reference

| Variable                      | Description                       | Default                      |
|------------------------------|-----------------------------------|------------------------------|
| `MONGO_URI`                  | MongoDB Atlas connection string   | **Required**                 |
| `DATABASE_NAME`              | MongoDB database name             | `athena_db`                  |
| `SECRET_KEY`                 | JWT signing secret key            | **Required**                 |
| `ALGORITHM`                  | JWT algorithm                     | `HS256`                      |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| Access token lifetime (minutes)   | `30`                         |
| `REFRESH_TOKEN_EXPIRE_DAYS`  | Refresh token lifetime (days)     | `7`                          |
| `DEBUG`                      | Enable debug mode                 | `False`                      |
| `ALLOWED_ORIGINS`            | CORS allowed origins              | `["http://localhost:3000"]` |

---

## 🐛 Error Handling

The API returns standard HTTP status codes:

- **200 OK:** Successful request
- **201 Created:** Resource created successfully
- **400 Bad Request:** Invalid input
- **401 Unauthorized:** Missing/invalid auth
- **403 Forbidden:** Insufficient permissions
- **404 Not Found:** Resource does not exist
- **409 Conflict:** Duplicate resource (e.g., email)
- **500 Internal Server Error:** Unexpected server error

**Example error response:**

```json
{
  "detail": "Email already registered"
}
```

---

## 🧪 Testing the API

### Using Swagger UI

1. Open `http://localhost:8000/docs`
2. Try endpoints directly from the browser
3. Use the **“Authorize”** button to add JWT token

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

Since `/auth/register/admin` requires an existing admin, you must manually insert the first admin.

### Option 1: Using MongoDB Compass

1. Connect to MongoDB Atlas
2. Open `athena_db.users` collection
3. Insert document:

```json
{
  "email": "admin@athena.com",
  "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqXqmBN7Jm",
  "role": "admin",
  "createdAt": { "$date": "2025-12-08T00:00:00.000Z" }
}
```

> 🔐 The hash above corresponds to password `"admin123"`. Generate your own using:

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("your_password_here"))
```

---

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

Run:

```bash
python create_admin.py
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

---

### Using Railway / Render / Other PaaS

1. Push code to GitHub
2. Connect repository to **Railway**, **Render**, or your preferred PaaS
3. Configure environment variables (from `.env`)
4. Deploy

---

## 🧭 Roadmap & Ideas

Some potential next steps for ATHENA:

- ✅ Export quiz results as CSV / Excel
- ✅ Role-based analytics dashboards (per student / teacher / admin)
- 🔜 Integration with LMS platforms (Moodle, Canvas, etc.)
- 🔜 Multi-language support (English, French, Arabic, …)
- 🔜 More LLM options (OpenAI, Llama 3, etc.)
- 🔜 Advanced analytics (time-on-task, difficulty progression)

> Feel free to open issues or PRs with your own ideas!

---

## 🤝 Contributing

Contributions are welcome!

1. **Fork** the repository
2. Create a new branch: `feature/my-awesome-feature`
3. Commit your changes with clear messages
4. Open a **Pull Request** with a detailed description

Please make sure to:

- Add or update tests where relevant  
- Run the existing test suite before submitting

---

## 📄 License

**MIT License** – you are free to use this project for learning or production.

See the [LICENSE](./LICENSE) file for full details (if available).

---

## 👨‍💻 Author

Created with passion for AI and education by:

- **Tasnim Mtir**  
- **Ikram Menyaoui**  
- **Aya Mekni**  
- **Nour Saibi**  

> If you build something cool with ATHENA, we’d love to hear about it!
