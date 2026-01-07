# Veterinary Clinic Website Architecture Plan

## Project Overview

This document outlines the architecture for a small veterinary clinic website with the following key features:
- Public website with news, contacts, and contact form
- Admin panel for content management (Django admin)
- Docker-based deployment with Django + PostgreSQL
- Nginx as a standalone reverse proxy
- Responsive, modern design for mobile devices

## 1. Project Structure

```
veterinary-clinic/
├── docs/                    # Documentation
├── src/                     # Source code
│   ├── backend/             # Django application
│   │   ├── core/            # Site-wide settings and common phrases
│   │   ├── clinic/          # Main Django project
│   │   ├── news/            # News management app
│   │   ├── contacts/        # Contacts and forms app
│   │   ├── about/           # About page content app
│   │   ├── services/        # Services and pricing app
│   │   ├── reviews/         # Customer reviews app
│   │   └── manage.py        # Django management script
│   └── frontend/            # Frontend assets
│       ├── templates/       # HTML templates
│       ├── static/          # CSS, JS, images
│       └── media/           # User uploaded content
├── docker/                  # Docker configurations
│   ├── django/              # Django Dockerfile
│   └── postgres/            # PostgreSQL initialization
├── nginx/                   # Nginx configuration
├── docker-compose.yml       # Docker Compose configuration
└── README.md                # Project documentation
```

## 2. Technology Stack

- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3 (Bootstrap 5), JavaScript
- **Deployment**: Docker Compose
- **Web Server**: Nginx (standalone)
- **Admin Interface**: Django Admin

## 3. Database Schema

### Core Models (Site-wide)
```python
# core/models.py
class SiteSettings(models.Model):
    site_title = models.CharField(max_length=100)
    meta_description = models.TextField()
    footer_text = models.TextField()
    copyright_text = models.CharField(max_length=200)

class CommonPhrase(models.Model):
    key = models.SlugField(unique=True)
    text = models.TextField()

class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    button_text = models.CharField(max_length=50)

class StatItem(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
```

### News Models
```python
# news/models.py
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

class NewsPageText(models.Model):
    header_title = models.CharField(max_length=200)
    header_subtitle = models.TextField()
```

### Contact Models
```python
# contacts/models.py
class ContactInfo(models.Model):
    clinic_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    working_hours = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    map_zoom = models.IntegerField(default=16)

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ContactsPageText(models.Model):
    header_title = models.CharField(max_length=200)
    by_bus = models.TextField()
    by_car = models.TextField()
```

### About Models
```python
# about/models.py
class AboutPageText(models.Model):
    header_title = models.CharField(max_length=200)
    about_title = models.CharField(max_length=200)
    about_description = models.TextField()

class FeatureItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)

class Veterinarian(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='vets/', blank=True, null=True)
    order = models.IntegerField(default=0)
```

### Services Models
```python
# services/models.py
class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_照顾=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_popular = models.BooleanField(default=False)

class ServicesPageText(models.Model):
    header_title = models.CharField(max_length=200)
    header_subtitle = models.TextField()
```

### Reviews Models
```python
# reviews/models.py
class Review(models.Model):
    author = models.CharField(max_length=100)
    rating = models.IntegerField()
    text = models.TextField()
    is_published = models.BooleanField(default=False)

class ReviewsPageText(models.Model):
    header_title = models.CharField(max_length=200)
    header_subtitle = models.TextField()
```

## 4. Django Admin Configuration

The Django admin is the primary tool for content management.
- **Singleton Models**: Page-specific text models (e.g., `AboutPageText`, `SiteSettings`) are restricted to a single instance.
- **Rich Text**: `TextField`s are used for content that may require formatting.
- **Image Management**: Support for uploading news images, vet photos, etc.
- **Ordering**: Veterinarians and other list items can be ordered manually.

## 5. Docker Configuration

(Refer to `docker-compose.yml` and `docker/` directory for details)
- **Django Container**: Runs Gunicorn, handles application logic.
- **PostgreSQL Container**: Stores all persistent data.
- **Nginx Container**: Serves as a reverse proxy and static file server.

## 6. Nginx Configuration

(Refer to `docker/nginx/nginx.conf` for details)
- Handles SSL termination (in production).
- Serves static and media files directly.
- Proxies application requests to Gunicorn.

## 7. Frontend Structure

- **Base Template**: `base.html` contains the header, navigation, and footer.
- **Context Processor**: `site_content` provides `site_settings` and `common_phrases` to all templates.
- **Responsive Design**: Built with Bootstrap 5 and custom CSS.

## 8. Deployment Architecture

(Refer to `docs/implementation-stages.md` for deployment details)
- CI/CD via GitHub Actions.
- Deployment to VPS via SSH and Docker Compose.