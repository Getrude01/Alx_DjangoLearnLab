# Social Media API

A simple Django REST API that supports user registration, login, token authentication, and profile management.

## Features
- Custom user model (bio, profile picture)  
- Register users  
- Login using username or email  
- Token-based authentication  
- View & update profile  

## Setup

```bash
git clone https://github.com/<username>/Alx_DjangoLearnLab.git
cd social_media_api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoints

### Register  
POST `/accounts/register/`
```json
{
  "username": "Getty",
  "email": "Getty@example.com",
  "password": "password123"
}
```

### Login  
POST `/accounts/login/`
```json
{
  "email": "Getty@example.com",
  "password": "password123"
}
```

### Profile  
GET `/accounts/profile/`  
PUT `/accounts/profile/`

Header:  
`Authorization: Token <your_token>`

## Project Structure
```
social_media_api/
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
└── social_media_api/
```