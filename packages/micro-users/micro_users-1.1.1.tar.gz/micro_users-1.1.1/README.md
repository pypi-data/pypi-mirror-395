# Micro Users - Arabic Django User Management App

[![PyPI version](https://badge.fury.io/py/micro-users.svg)](https://pypi.org/project/micro-users/)

**Arabic** lightweight, reusable Django app providing user management with abstract user, permissions, localization, and activity logging.


## Requirements
- **Must be installed on a fresh database.**
- Python 3.11+
- Django 5.1+
- django-crispy-forms 2.4+
- django-tables2 2.7+
- django-filter 24.3+
- pillow 11.0+
- babel 2.1+


## Features
- Custom AbstractUser model
- User permissions system  
- Activity logging (login/logout, CRUD tracking)
- Localization support
- Admin interface integration
- CRUD views and templates
- Filtering and tabulation

## Installation

```bash
pip install git+https://github.com/debeski/micro-users.git
# OR local
pip install micro-users
```

## Configuration

1. Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    'users',  # Preferably on top
    'django.contrib.admin',
    'django.contrib.auth',
    ...
]
```

2. Set custom user model in settings.py:
```python
AUTH_USER_MODEL = 'users.CustomUser'
```

3. Include URLs in your main project folder `urls.py`:
```python
urlpatterns = [
    ...
    path('manage/', include('users.urls')),
]
```

4. Run migrations:
```bash
python manage.py migrate users
```


## Structure
```
users/
├── models.py      # User model, permissions, activity logs
├── views.py       # CRUD operations
├── urls.py        # URL routing
├── admin.py       # Admin integration
├── templates/     # HTML templates
└── migrations/    # Database migrations
```
