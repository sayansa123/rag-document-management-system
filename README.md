# AI Document Management System
### Intelligent RAG-Powered Document Q&A with Role-Based Access

An enterprise-style AI Document Management System that allows organizations to securely store internal documents and query them using a Retrieval-Augmented Generation (RAG) pipeline powered by HuggingFace models and ChromaDB.

The system enforces **role-based access control (Admin / Staff / User)** ensuring users only retrieve information from documents they are authorized to access.

---

## How It Works (Architecture)

```
Document Upload
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
ChromaDB Vector Storage
      ↓
User Question
      ↓
Permission Filtering (RBAC)
      ↓
Relevant Context Retrieval
      ↓
HuggingFace LLM
      ↓
Grounded AI Answer
```

This prevents hallucination and ensures answers come only from allowed documents.

---

## Features

### Security & Access Control
- JWT Authentication
- Role Based Access Control (Admin / Staff / User)
- Document visibility levels
- Restricted retrieval based on permission
- Secure password hashing

### Document Management
- Upload documents
- Delete documents
- List accessible documents
- Role-restricted viewing

### AI Chat (RAG)
- Context-aware answers from documents
- Multi-session chat history
- Grounded responses (no blind LLM answers)
- HuggingFace model integration

### Admin Controls
- Create staff/admin accounts
- View all users
- Delete users
- Monitor chat sessions

### Frontend
- Streamlit based UI
- Login system
- Chat interface
- Document upload panel

---

## Tech Stack

**Backend**
- FastAPI
- SQLAlchemy
- JWT Authentication

**AI / RAG**
- ChromaDB (Vector Database)
- HuggingFace Inference API
- Embedding Retrieval Pipeline

**Frontend**
- Streamlit

---

##  Project Structure

```
app/
├── api/            # API endpoints
├── core/           # config & security
├── db/             # database setup
├── models/         # database models
├── schemas/        # request/response schemas
├── services/       # business logic
├── rag/            # RAG pipeline
│   ├── ingestion.py
│   ├── retrieval.py
│   └── vector_store.py

main.py
streamlit_frontend.py
requirements.txt
.env.example
```

---

##  Setup Guide

### Clone Repository
```bash
git clone https://github.com/sayansa123/rag-document-management-system.git
cd rag-document-management-system
```

### Create Environment Variables
```bash
cp .env.example .env
```
Fill the values inside `.env`

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Backend
```bash
uvicorn main:app --reload
```
Backend runs at:
```
http://localhost:8000
```

### Run Frontend
```bash
streamlit run streamlit_frontend.py
```
Frontend runs at:
```
http://localhost:8501
```

---

##  Roles

| Role | Permissions |
|----|----|
| **Admin** | Full access (users + documents + chats) |
| **Staff** | Upload & query internal documents |
| **User** | Query public documents only |

---

##  Security Model

The system prevents data leakage using **retrieval-time authorization filtering**:

1. User logs in → JWT issued
2. Query received → role identified
3. Only allowed documents retrieved
4. LLM receives filtered context only

So the model **cannot answer from restricted documents**.

---

## Example Use Cases
- Company knowledge base assistant
- Internal policy Q&A bot
- Research paper search assistant
- Secure enterprise chatbot

---

## Future Improvements
- PDF preview
- OCR support
- Multi-tenant organizations
- Fine-tuned local LLM
- Docker deployment
- Per-chat memory persistence (context retention for each session)
- Strong password hashing & security hardening

---
## Snapshots

### Authentication

<p align="center">
  <img src="images/authentication/01_login.png" alt="Login" width="45%"/>
  &nbsp;&nbsp;
  <img src="images/authentication/02_register.png" alt="Register" width="45%"/>
</p>
<p align="center"><em>Login &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Register</em></p>

---

### End User

<p align="center">
  <img src="images/end_user/01_user_creating_chat_session.png" alt="User Creating Chat Session" width="45%"/>
  &nbsp;&nbsp;
  <img src="images/end_user/02_user_creating_chats_on_the_session.png" alt="User Creating Chats on Session" width="45%"/>
</p>
<p align="center"><em>Creating a Chat Session &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Chatting on the Session</em></p>

<p align="center">
  <img src="images/end_user/03_chatting_with_admin_only_docs.png" alt="Chatting with Admin Only Docs" width="45%"/>
  &nbsp;&nbsp;
  <img src="images/end_user/04_chatting_with_staff_admin_only_docs.png" alt="Chatting with Staff & Admin Docs" width="45%"/>
</p>
<p align="center"><em>Chatting with Admin-Only Docs &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Chatting with Staff & Admin Docs</em></p>

<p align="center">
  <img src="images/end_user/05_chatting_with_user_only_docs.png" alt="Chatting with User Only Docs" width="45%"/>
</p>
<p align="center"><em>Chatting with User-Only Docs</em></p>

---

### Staff

<p align="center">
  <img src="images/staff/01_staff_documents_upload.png" alt="Staff Documents Upload" width="45%"/>
  &nbsp;&nbsp;
  <img src="images/staff/02_staff_create_chat.png" alt="Staff Create Chat" width="45%"/>
</p>
<p align="center"><em>Staff Document Upload &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Staff Create Chat</em></p>

<p align="center">
  <img src="images/staff/03_chatting_with_admin_only_docs.png" alt="Staff Chatting with Admin Only Docs" width="45%"/>
  &nbsp;&nbsp;
  <img src="images/staff/04_chatting_with_staff_admin_only_docs.png" alt="Staff Chatting with Staff & Admin Docs" width="45%"/>
</p>
<p align="center"><em>Chatting with Admin-Only Docs &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Chatting with Staff & Admin Docs</em></p>

<p align="center">
  <img src="images/staff/05_chatting_with_public_docs.png" alt="Staff Chatting with Public Docs" width="45%"/>
</p>
<p align="center"><em>Chatting with Public Docs</em></p>

---

### Admin

<p align="center">
  <img src="images/admin/01_admin_check_own_chat_session.png" alt="Admin Check Own Chat Session" width="45%"/>
  &nbsp;&nbsp;
  <img src="images/admin/02_chatting_with_admin_only_docs.png" alt="Admin Chatting with Admin Only Docs" width="45%"/>
</p>
<p align="center"><em>Admin Own Chat Session &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Chatting with Admin-Only Docs</em></p>

<p align="center">
  <img src="images/admin/03_admin_documents_upload.png" alt="Admin Documents Upload" width="45%"/>
  &nbsp;&nbsp;
  <img src="images/admin/04_admin_check_all_users.png" alt="Admin Check All Users" width="45%"/>
</p>
<p align="center"><em>Admin Document Upload &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Admin View All Users</em></p>

<p align="center">
  <img src="images/admin/05_admin_create_staff.png" alt="Admin Create Staff" width="45%"/>
  &nbsp;&nbsp;
  <img src="images/admin/06_admin_create_admin.png" alt="Admin Create Admin" width="45%"/>
</p>
<p align="center"><em>Admin Create Staff &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Admin Create Admin</em></p>

<p align="center">
  <img src="images/admin/07_admin_check_all_sessions.png" alt="Admin Check All Sessions" width="30%"/>
  &nbsp;
  <img src="images/admin/08_admin_check_all_sessions_2.png" alt="Admin Check All Sessions 2" width="30%"/>
  &nbsp;
  <img src="images/admin/09_admin_check_all_sessions_3.png" alt="Admin Check All Sessions 3" width="30%"/>
</p>
<p align="center"><em>Admin View All Sessions (1) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Admin View All Sessions (2) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Admin View All Sessions (3)</em></p>

## Author
Sayan Sarkar Backend & AI Engineer