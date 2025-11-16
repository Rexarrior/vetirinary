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
│   │   ├── clinic/          # Main Django project
│   │   ├── news/            # News management app
│   │   ├── contacts/        # Contacts and forms app
│   │   ├── about/           # About page content app
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

### News Model
```python
# news/models.py
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "News"
        ordering = ['-created_at']
```

### Contact Information Model
```python
# contacts/models.py
class ContactInfo(models.Model):
    clinic_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    working_hours = models.CharField(max_length=200)
    yandex_map_embed_code = models.TextField(blank=True, help_text="Yandex Maps embed code")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return self.clinic_name
```

### Contact Form Submissions
```python
# contacts/models.py
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Contact Submissions"
        ordering = ['-created_at']
```

### About Page Content Model
```python
# about/models.py
class AboutContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "About Content"
    
    def __str__(self):
        return self.title

class Veterinarian(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='vets/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Order of appearance")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Veterinarians"
        ordering = ['order']
    
    def __str__(self):
        return self.name
```

## 4. Django Admin Configuration

The Django admin will be used to manage:
- News articles (CRUD operations)
- Contact information (dynamic content)
- About page content (clinic description and veterinarians)
- Contact form submissions (read-only)
- User management

Admin features:
- Rich text editor for news content and about page description
- Image upload for news articles, about page, and veterinarian profiles
- Yandex Maps embed code management for contact page
- Filtering and search capabilities
- User authentication and permissions
- Content ordering for veterinarians

## 5. Docker Configuration

### Docker Compose (docker-compose.yml)
```yaml
version: '3.8'

services:
  django:
    build:
      context: .
      dockerfile: docker/django/Dockerfile
    container_name: vet_clinic_django
    ports:
      - "8000:8000"
    environment:
      - DEBUG=0
      - DATABASE_URL=postgresql://vet_user:vet_pass@postgres:5432/vet_db
    depends_on:
      - postgres
    volumes:
      - ./src/backend:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  postgres:
    image: postgres:13
    container_name: vet_clinic_postgres
    environment:
      POSTGRES_DB: vet_db
      POSTGRES_USER: vet_user
      POSTGRES_PASSWORD: vet_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Django Dockerfile (docker/django/Dockerfile)
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src/backend /app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "clinic.wsgi:application"]
```

## 6. Nginx Configuration

Nginx will run standalone (outside Docker) and serve as a reverse proxy:

### nginx.conf
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/static/files/;
        expires 30d;
    }
    
    location /media/ {
        alias /path/to/media/files/;
        expires 30d;
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
}
```

## 7. Frontend Structure

### Pages
1. **Home Page**
   - Welcome message
   - Featured services
   - Latest news preview
   - Contact information

2. **News Page**
   - List of news articles
   - Individual news article view
   - Pagination

3. **Contacts Page**
    - Clinic address and Yandex Maps integration
    - Phone numbers and email
    - Working hours
    - Contact form

4. **About Page**
   - Clinic information
   - Veterinarian profiles
   - Services offered

### Responsive Design Features
- Mobile-first approach
- Flexible grid system (Bootstrap 5)
- Touch-friendly navigation
- Optimized images for different screen sizes
- Accessible forms and navigation

## 8. Deployment Architecture

```
[Internet]
    |
[Nginx - Standalone Server (Port 80/443)]
    |
[Docker Network]
    ├── [Django Container (Port 8000)]
    |       ├── Gunicorn WSGI Server
    |       ├── Static Files Volume
    |       └── Media Files Volume
    |
    └── [PostgreSQL Container (Port 5432)]
            └── Persistent Data Volume
```

### Deployment Steps
1. Set up server with Docker and Docker Compose
2. Install and configure Nginx
3. Configure domain and SSL certificates
4. Deploy Docker containers
5. Set up backup procedures
6. Configure monitoring

## 9. Security Considerations

- Django security best practices
- PostgreSQL secure configuration
- Nginx security headers
- HTTPS enforcement
- Regular security updates
- Backup and disaster recovery plan

## 10. Performance Optimization

- Static file serving via Nginx
- Database indexing
- Caching strategies
- Image optimization
- Gunicorn worker configuration
- Database connection pooling

## 11. Maintenance Plan

- Regular backups of database and media files
- Log rotation
- Security updates
- Performance monitoring
- Error tracking