# ChatApp


# Chat Application

A **FastAPI** based real-time chat application with **JWT Authentication**, **Role-Based Access Control (RBAC)**, **WebSocket chat**, and **PostgreSQL** persistence. This app supports **admin** and **user** roles, secure authentication, chat rooms, and message broadcasting.

---

## 📃 API Documentation

✅ Interactive Swagger UI available at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

✅ ReDoc available at:
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🚀 Features

* ✅ **JWT Authentication (OAuth2 Password Flow)**
* ✅ **Role-Based Access Control (Admin/User)**
* ✅ **WebSocket Chat with Room IDs**
* ✅ **Real-time messaging with PostgreSQL persistence**
* ✅ **Secure Password Hashing**
* ✅ **Admin-only room creation**
* ✅ **User info retrieval via secured endpoint**

---

## 🧱 API Endpoints Overview

### ✅ Authentication

#### **Signup**

* **POST /auth/signup**
* Create a new user account.
* **Request Body** (JSON):

```json
{
  "username": "prabesh",
  "email": "prabesh@gmail.com",
  "password": "yourpassword",
  "role": "user"
}
```
role will accept only two values , one is  ```user ``` another is ```admin```

* **Responses:**

  * `200 OK`: Successful user creation
  * `422 Unprocessable Entity`: Validation errors

#### **Login**

* **POST /auth/login**
* Login via OAuth2 Password Flow.
* **Request Body** (Form Data):

```
username=email
password=yourpassword
```
OAuth2 only support username so it show username but you should enter email

* **Response:**

```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

#### **Get User (Protected)**

* **GET /auth/user/{id}**
* Retrieve user details by ID (Requires authentication).
* **Authorization**: Bearer Token via `Authorization: Bearer <token>`
* **Response:**

```json
{
  "id": 1,
  "username": "prabesh",
  "email": "prabesh@gmail.com",
  "role": "user"
}
```

---

### 🏷️ Room Management

#### **Create Room (Admin-only)** 
* **POST /rooms/**
* Only `admin` users can create chat rooms.
* **Request Body** (JSON):

```json
{
  "name": "General Discussion",
  "description": "A place to talk about anything"
}
```

* **Response:**

```json
{
  "id": 1,
  "name": "General Discussion",
  "description": "A place to talk about anything"
}
```

---

### WebSocket Chat

#### **WebSocket Endpoint**

* **/ws/{room\_id}?token=YOUR\_JWT\_TOKEN**
* Secure WebSocket connection using JWT Token.
* **Functionality**:

  * Authenticate using JWT token.
  * Join a specific room via `{room_id}`.
  * On connection: receive recent messages.
  * On sending messages: broadcast to all connected clients and save in DB.

---
![Alt text](images_for_documentation/2025-07-19_19-47.png)


## 🗄️ Database Models Summary

| Model       | Fields                                                             |
| ----------- | ------------------------------------------------------------------ |
| **User**    | `id`, `username`, `email`, `password`, `role` |
| **Room**    | `id`, `name`, `description`                                        |
| **Message** | `id`, `room_id`, `user_id`, `content`, `timestamp`                 |

---

## 📦 Project Setup

### 1. Clone & Setup Virtual Environment

```bash
git clone https://github.com/yourusername/chat-app.git
cd chat-app
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure `.env` file

```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/chatdb
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run the App

```bash
uvicorn app.main:app --reload
```

---

## 🛡️ Authentication Details

* **Token URL**: `/auth/login`
* **Grant Type**: `password`
* **Bearer Token Required** for protected endpoints (user info, room creation, WebSocket).

---

## 🛠️ Development Commands

| Task         | Command                              |
| ------------ | ------------------------------------ |
| Start server | `uvicorn app.main:app --reload`      |
| Migrate DB   | Auto-generated on startup (SQLModel) |
| API Docs     | Visit `/docs` or `/redoc`            |

---

## 📌 Notes

* Admin-only actions (like creating rooms) are protected via role-based dependencies.
* All messages are persisted in PostgreSQL and can be extended with pagination.
* Easy integration with frontend clients (React, Vue, etc.).

---

## 📜 License

Licensed under the **MIT License**.
