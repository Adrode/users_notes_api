# 📝 Users & Notes API

Users & Notes API is a backend REST API for managing users and notes.
It is built with FastAPI and demonstrates authentication, role-based authorization, and relational database modeling.

The project focuses on implementing secure user management, ownership-based access control, and admin-level permissions.

## 🚀 Key Features
- JWT-based authentication (login/register)
- Password hashing using bcrypt
- Role-based access control (admin / user)
- Users can manage only their own notes
- Admin panel for managing all users and notes
- Notes support `is_done` status
- Users support `is_active` status
- PostgreSQL database running in Docker

## 🧠 Domain Model Overview
The application models a simple but secure user-note system:
```text
User
├── Notes
└── Role (admin / user)
```

### Core relationships
- **User → Notes**
  - Each user can create multiple notes
  - Notes are owned and accessible only by their creator

- **Role-based access**
  - Admin users can access and manage all users and notes
  - Regular users are restricted to their own data

## 🧱 Tech Stack
- Python
- FastAPI
- SQLAlchemy ORM
- Pydantic
- Alembic
- PostgreSQL
- Docker & Docker Compose
- JWT (python-jose)
- bcrypt (passlib)

## 🔐 Authentication & Authorization
- JWT tokens used for authentication
- Passwords are hashed using bcrypt
- Dependency injection protects endpoints
- Role-based access control (admin / user)
- Ownership checks prevent unauthorized access to notes

## 📡 API Overview
### Auth
- POST `/auth/register` — Create new user (public)
- POST `/auth/login` — Obtain JWT token (public)

### Users
- GET `/users/me` — Get current user (authenticated)
- PATCH `/users/me` — Update current user (authenticated)

### Notes
- POST `/notes/` — Create note (authenticated)
- GET `/notes/` — Get user notes (authenticated)
- GET `/notes/{id}` — Get note by id (ownership required)
- PATCH `/notes/{id}` — Update note (ownership required)
- DELETE `/notes/{id}` — Delete note (ownership required)

### Admin
- GET `/admin/users` — List all users (admin only)
- GET `/admin/notes` — List all notes (admin only)
- DELETE `/admin/users/{id}` — Delete user (admin only)

## ⚙️ Setup & Run
### 1. Clone repository
```bash
git clone https://github.com/Adrode/fastapi_users_notes_api.git
cd users_notes_api
```
2. Create virtual environment
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
3. Start database
```bash
docker compose up -d
```
4. Run migrations
```bash
alembic upgrade head
```
5. Run server
```bash
uvicorn main:app --reload
```
API docs:
http://127.0.0.1:8000/docs

## 🧩 Architecture Notes
- Clean separation between authentication and business logic
- Role-based access control implemented via dependencies
- Ownership validation on resource access
- PostgreSQL with Alembic migrations

## 🧠 What This Project Demonstrates
- Backend API design with FastAPI
- JWT authentication & authorization
- Role-based access control
- Relational database modeling
- Secure CRUD API design