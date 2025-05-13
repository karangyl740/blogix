
# 📝 Blogix – Django + Flask API Integration Project

**Blogix** is a full-stack blog management system that uses a **Django-powered frontend** and a **Flask backend**. The two parts communicate securely through a REST API built using **Django REST Framework (DRF)**. It supports blog creation, editing, deletion, user management, and more.

---

## 📌 Features

- 🔐 JWT-based authentication
- 📝 Create, edit, delete blog posts
- 👥 Role-based access (admin, staff, regular users)
- 📦 DRF-powered API for secure Django-to-Flask communication
- 🖥️ Django admin panel
- 🌐 Flask frontend templates (Jinja2)
- 📁 Media upload support (images, thumbnails)

---

## 🛠 Tech Stack

| Technology              | Role                  |
|-------------------------|------------------------|
| Django                  | Frontend Framework     |
| Flask                   | Backend/API Server     |
| Django REST Framework   | API Communication      |
| SQLite3                 | Database               |
| HTML/CSS                | Frontend Templates     |
| JWT                     | Authentication         |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/blogix.git
cd blogix
```

### 2. Set Up a Virtual Environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run Django Server

```bash
cd e2_blog
python manage.py migrate
python manage.py runserver
```

### 5. Run Flask Server

```bash
cd flask_app
python app.py
```

---

## 🌐 API Overview

### Django Auth APIs

- `POST /api/token/` – Login and get JWT
- `POST /api/register/` – Register new users

### Blog APIs (Flask Backend)

- `GET /api/posts/` – List all blog posts
- `POST /api/create_post/` – Create a blog post
- `PUT /api/edit_post/<id>/` – Edit a blog post
- `DELETE /api/delete_post/<id>/` – Delete a blog post

---

## 🔐 Authentication

All protected endpoints require a JWT token:

**Header example:**

```
Authorization: Bearer <your_jwt_token>
```

---

## 📸 Screenshots

_Add UI screenshots here (optional)_

---

## 🙌 Contribution

1. Fork this repo
2. Create your feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -m "Add some feature"`
4. Push to the branch: `git push origin feature/new-feature`
5. Create a new Pull Request

---

## 📄 License

This project is licensed under the MIT License.
