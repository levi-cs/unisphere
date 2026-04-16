# 🎓 UniSphere — Official College Student Portal

A full-stack Django student portal for colleges with Student, Teacher, and Admin roles.

---

## ✅ Features

| Feature | Student | Teacher | Admin |
|---|---|---|---|
| Dashboard Overview | ✅ | ✅ | ✅ |
| View Subjects | ✅ | ✅ | ✅ |
| Attendance Report | ✅ | — | ✅ |
| Timetable | ✅ | ✅ | ✅ |
| Study Materials Download | ✅ | ✅ | ✅ |
| View Notices | ✅ | ✅ | ✅ |
| Post Announcements | — | ✅ | ✅ |
| Sign Up with OTP | ✅ | — | — |
| Forgot / Reset Password | ✅ | ✅ | ✅ |
| Django Admin Panel | — | — | ✅ |

---

## 🚀 Quick Start

### 1. Install Python 3.10+
Make sure Python is installed: `python --version`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run One-Click Setup (creates DB + demo data)
```bash
python setup.py
```

### 4. Start the Server
```bash
python manage.py runserver
```

### 5. Open in Browser
```
http://127.0.0.1:8000
```

---

## 🔑 Demo Login Credentials

| Role | ID / Username | Password |
|---|---|---|
| 👨‍💼 Admin | `admin` | `admin123` |
| 📖 Teacher | `TCH001` | `teacher123` |
| 🎒 Student | `U18CS001` | `student123` |
| 🎒 Student | `U18CS002` | `student456` |

---

## 📂 Project Structure

```
unisphere/
├── manage.py
├── setup.py              ← Run once to set up DB + demo data
├── requirements.txt
├── db.sqlite3            ← Created automatically
├── unisphere/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── main/
    ├── models.py         ← Student, Teacher, Subject, Attendance, etc.
    ├── views.py          ← All page logic
    ├── urls.py           ← URL routes
    ├── admin.py          ← Django admin config
    ├── templates/main/
    │   ├── base.html
    │   ├── login.html
    │   ├── signup.html
    │   ├── verify_otp.html
    │   ├── forgot_password.html
    │   ├── reset_password.html
    │   └── dashboard.html    ← All sections in one template
    └── static/main/
        ├── css/style.css
        └── js/main.js
```

---

## 📧 Email / OTP Setup (for real emails)

Edit `unisphere/settings.py` and replace the email section:

```python
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-gmail-app-password'   # NOT your login password
DEFAULT_FROM_EMAIL  = 'UniSphere <your-email@gmail.com>'
```

> 💡 To get a Gmail App Password: Google Account → Security → 2-Step Verification → App Passwords

---

## 🌐 Deploying to Production

1. Set `DEBUG = False` in `settings.py`
2. Change `SECRET_KEY` to a secure random value
3. Set `ALLOWED_HOSTS = ['yourdomain.com']`
4. Use WhiteNoise or nginx to serve static files
5. Use gunicorn: `gunicorn unisphere.wsgi`

---

## 🛠️ Adding Data via Admin Panel

1. Go to `http://127.0.0.1:8000/admin/`
2. Login with `admin` / `admin123`
3. Add: Courses, Semesters, Students, Teachers, Subjects, Attendance, Materials, Notices, Timetable
