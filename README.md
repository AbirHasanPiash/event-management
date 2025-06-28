# 🎉 Event Management System

A modern and fully functional **Event Management System** built with Django (MVT architecture), PostgreSQL, HTML, and Tailwind CSS. This platform allows **users, event organizers, and admins** to manage events, RSVP, and notifications with secure access control and email verification.

---

## 🚀 Features

- 🔐 **Access Control** for:
  - Attendees / Regular Users
  - Event Organizers
  - Admin Panel Users
- 📧 **Email Verification** on registration
- 📩 **RSVP Notifications** via email
- 🗓️ Create, update, and delete events
- 🎟️ RSVP to upcoming events
- 🧑‍💼 Organizers can manage their own events
- 📊 Admin can view/manage all users and events
- 🎨 Responsive front-end with **Tailwind CSS**
- 🧭 Clean UI built using **HTML + Tailwind CSS**
- ⚙️ Backend powered by **Django ORM + PostgreSQL**

---

## 🏗️ Tech Stack

| Layer           | Technology             |
|----------------|------------------------|
| Backend         | Django (MVT)           |
| Frontend        | HTML, Tailwind CSS     |
| Database        | PostgreSQL             |
| Email Service   | Django's Email Backend |
| Authentication  | Django Auth + Email Verification |
| Notifications   | Email on RSVP          |

---

## ⚙️ Setup Instructions

```bash
# Clone the Repository
git clone https://github.com/AbirHasanPiash/event-management.git
cd event-management

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Configure PostgreSQL Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Run Migrations
python manage.py makemigrations
python manage.py migrate

# Create Superuser
python manage.py createsuperuser

#Start the Development Server
python manage.py runserver

#Email Setup (for Verification & RSVP Notification)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
EMAIL_USE_TLS = True
```

## 🧑‍💻 Author

**[MD. ABIR HASAN PIASH](https://www.linkedin.com/in/a-h-piash/)**  
📧 [abirhasanpiash@gmail.com](mailto:abirhasanpiash@gmail.com)  
🔗 [GitHub Profile](https://github.com/AbirHasanPiash)

---

## 📄 License

This project is licensed under the **[MIT License](LICENSE)**.  
Feel free to use, modify, and distribute this project with proper attribution.
