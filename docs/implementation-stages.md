# Veterinary Clinic Website Implementation Stages

This document outlines the step-by-step implementation approach for the veterinary clinic website, divided into three main stages to ensure proper development, testing, and deployment.

## Stage 1: Design, Frontend and Backend with SQLite

### Objective
Create and debug the core functionality and design using a simple SQLite database for local development and testing.

### Tasks

1. **Design Implementation**
   - Create wireframes for all pages (Home, News, Contacts, About)
   - Develop responsive UI components using Bootstrap 5
   - Implement mobile-first design approach
   - Create design system (colors, typography, spacing)

2. **Frontend Development**
   - Set up project structure with HTML, CSS, and JavaScript
   - Implement responsive templates for all pages
   - Integrate Yandex Maps for contact page
   - Create contact form with client-side validation
   - Implement news listing and detail pages
   - Add image optimization for responsive design

3. **Backend Development**
   - Set up Django project with SQLite database
   - Create models for News, ContactInfo, AboutContent, Veterinarian, and ContactSubmission
   - Implement Django admin for content management
   - Create views and URL patterns for all pages
   - Implement contact form processing
   - Set up static and media file handling

4. **Functionality Testing**
   - Test all CRUD operations in Django admin
   - Verify responsive design on different screen sizes
   - Test contact form submission and validation
   - Debug and fix any issues with core functionality
   - Ensure all dynamic content is properly displayed

### Deliverables
- Fully functional website with all pages
- Admin interface for content management
- Responsive design working on desktop and mobile
- Working contact form with validation
- SQLite database with sample data

### Success Criteria
- All core functionality works as expected
- Design is responsive and visually appealing
- Admin interface allows full content management
- No critical bugs or issues

## Stage 2: Docker Compose with PostgreSQL

### Objective
Containerize the application using Docker Compose and migrate to PostgreSQL database for more realistic testing.

### Tasks

1. **Docker Configuration**
   - Create Dockerfile for Django application
   - Create docker-compose.yml with Django and PostgreSQL services
   - Configure environment variables for database connection
   - Set up volume mounting for static and media files
   - Configure Gunicorn as WSGI server

2. **Database Migration**
   - Update Django settings to use PostgreSQL
   - Create PostgreSQL service in Docker Compose
   - Migrate existing data from SQLite to PostgreSQL
   - Update database configuration for production settings

3. **Container Testing**
   - Test application inside Docker containers
   - Verify database connectivity and data persistence
   - Test file uploads and static file serving
   - Debug any container-specific issues
   - Optimize container configuration for performance

4. **Environment Configuration**
   - Set up separate settings for development and production
   - Configure environment variables for sensitive data
   - Implement proper logging within containers
   - Set up health checks for services

### Deliverables
- Docker Compose configuration with Django and PostgreSQL
- Containerized application running in Docker
- PostgreSQL database with migrated data
- Environment-specific configuration files

### Success Criteria
- Application runs correctly in Docker containers
- PostgreSQL database is properly configured and connected
- Data persists across container restarts
- No performance issues with containerized setup

## Stage 3: Deployment with GitHub Actions

### Objective
Create a CI/CD pipeline using GitHub Actions for automated deployment and set up the production environment.

### Tasks

1. **GitHub Actions Workflow**
   - Create workflow for continuous integration
   - Set up automated testing in CI pipeline
   - Create deployment workflow for production
   - Configure environment secrets and variables
   - Implement rollback mechanisms

2. **Production Environment Setup**
   - Configure standalone Nginx as reverse proxy
   - Set up SSL certificates (Let's Encrypt)
   - Configure domain and DNS settings
   - Implement security headers and best practices
   - Set up monitoring and logging

3. **Deployment Process**
   - Create deployment scripts for automated deployment
   - Set up database migration process
   - Configure static and media file serving
   - Implement backup procedures
   - Test deployment pipeline

4. **Final Testing**
   - Test production deployment
   - Verify all functionality in production environment
   - Test performance and load handling
   - Debug any deployment-related issues
   - Document deployment process

### Deliverables
- GitHub Actions workflows for CI/CD
- Production-ready deployment configuration
- Automated deployment scripts
- Documentation for deployment process
- Monitoring and backup procedures

### Success Criteria
- GitHub Actions pipeline successfully deploys the application
- Production environment is secure and performant
- Automated deployment works without manual intervention
- Application is accessible via domain with SSL
- Backup and monitoring systems are in place

## Timeline Overview

```
Stage 1: Design, Frontend and Backend with SQLite
├── Design and Frontend Development (2-3 weeks)
├── Backend Development (1-2 weeks)
└── Testing and Debugging (1 week)

Stage 2: Docker Compose with PostgreSQL
├── Docker Configuration (1 week)
├── Database Migration (3-4 days)
└── Testing and Debugging (3-4 days)

Stage 3: Deployment with GitHub Actions
├── GitHub Actions Setup (1 week)
├── Production Environment (1 week)
├── Deployment Testing (3-4 days)
└── Documentation (2-3 days)
```

## Risk Mitigation

1. **Technical Risks**
   - Regular code backups during each stage
   - Incremental testing after each major feature
   - Version control with Git for rollback capability

2. **Timeline Risks**
   - Buffer time allocated for unexpected issues
   - Regular progress reviews
   - Early identification of blockers

3. **Deployment Risks**
   - Staging environment for testing before production
   - Rollback procedures documented and tested
   - Monitoring alerts for immediate issue detection

## Completed Updates (January 2025)

### Major Redesign and Feature Additions

#### 1. **Design Overhaul Based on Market Analysis**
   - Analyzed websites of major veterinary clinics in Moscow
   - Implemented modern medical/veterinary design system
   - Updated color scheme: professional teal/blue-green primary colors with warm orange accents
   - Implemented clean, trust-inspiring design with professional typography (Montserrat)
   - Added comprehensive CSS variables system for consistent theming
   - Created responsive design with mobile-first approach

#### 2. **New Applications and Features**

   **Services Application (`services/`)**
   - Created `ServiceCategory` model for organizing services (Therapy, Surgery, Vaccination, etc.)
   - Created `Service` model with pricing, duration, and popularity flags
   - Implemented services listing page with category filtering
   - Created detailed price list page
   - Added service category detail pages
   - Full Django admin integration for service management

   **Reviews Application (`reviews/`)**
   - Created `Review` model with rating system (1-5 stars)
   - Support for pet information (name, type) in reviews
   - Photo upload capability for reviews
   - Review moderation system (is_published flag)
   - Reviews listing page with star ratings display

#### 3. **Enhanced Navigation and Structure**
   - Updated main navigation with new sections: Services, Reviews
   - Added emergency banner with 24/7 contact information
   - Implemented sticky navigation bar
   - Added breadcrumb navigation on all pages
   - Created comprehensive footer with contact information and social links

#### 4. **Improved Homepage**
   - Hero section with clinic badges and call-to-action buttons
   - Statistics section (years of experience, patients, doctors, rating)
   - Services preview cards with icons
   - "Why choose us" section with feature highlights
   - Online appointment booking form on homepage
   - Latest news section
   - Contact information section with map

#### 5. **Contact Information Centralization**
   - Created Django context processor (`clinic/context_processors.py`) for global contact info access
   - Created template filter (`contacts/templatetags/contact_filters.py`) for phone number formatting
   - All contact information now stored in database (`ContactInfo` model)
   - Removed hardcoded phone numbers from templates
   - Contact info automatically available in all templates
   - Configured clinic address: улица Ленина, 42А, Константиновск, Ростовская область, 347250
   - Phone number: +7 (863) 123-45-67

#### 6. **Template Updates**
   - Completely redesigned all templates with modern UI
   - Updated `base.html` with new navigation and footer
   - Enhanced `home.html` with multiple sections and CTAs
   - Redesigned `about/about.html` with team showcase
   - Updated `contacts/contacts.html` with improved layout
   - Enhanced `contacts/contact_form.html` with better UX
   - Created `contacts/contact_success.html` confirmation page
   - Updated `news/list.html` and `news/detail.html` with modern cards
   - Created new templates for services and reviews

#### 7. **CSS and Styling**
   - Complete CSS rewrite with modern design system
   - CSS variables for colors, shadows, spacing, transitions
   - Professional medical color palette
   - Card-based layouts with hover effects
   - Responsive typography and spacing
   - Animation system for smooth interactions
   - Mobile-responsive breakpoints
   - Custom component styles (buttons, forms, cards, alerts)

#### 8. **Backend Improvements**
   - Fixed contact form redirect issue (now uses `redirect` instead of `render`)
   - Added proper form validation and error handling
   - Improved admin interface configuration
   - Added Russian language support (LANGUAGE_CODE = "ru-ru")
   - Enhanced model meta options with verbose names

#### 9. **Technical Enhancements**
   - Created template tags for phone number URL formatting
   - Implemented context processors for global data access
   - Improved code organization and structure
   - Added proper docstrings to functions
   - Fixed static file loading (using `{% static %}` tag)
   - Added Bootstrap Icons for consistent iconography

### Files Created/Modified

**New Applications:**
- `services/` - Services and pricing management
- `reviews/` - Customer reviews system

**New Files:**
- `clinic/context_processors.py` - Global context processor
- `contacts/templatetags/contact_filters.py` - Template filters
- `templates/services/list.html` - Services listing
- `templates/services/prices.html` - Price list
- `templates/services/category.html` - Service category detail
- `templates/reviews/list.html` - Reviews listing

**Major Updates:**
- `static/css/style.css` - Complete redesign (600+ lines)
- `templates/base.html` - New navigation and footer
- `templates/home.html` - Enhanced homepage
- `templates/about/about.html` - Redesigned about page
- `templates/contacts/*.html` - All contact pages updated
- `templates/news/*.html` - News pages redesigned
- `clinic/settings.py` - Added new apps and context processor
- `clinic/urls.py` - Added new URL patterns
- `contacts/views.py` - Fixed redirect issues
- `contacts/forms.py` - Improved form styling

### Database Changes
- Created migrations for `ServiceCategory` and `Service` models
- Created migrations for `Review` model
- Initialized `ContactInfo` with clinic address and contact details

### Design Principles Applied
- Professional medical/veterinary aesthetic
- Trust-building through clean design
- Clear call-to-action buttons
- Easy navigation and information architecture
- Mobile-responsive design
- Accessibility considerations
- Performance optimization

#### 10. **Yandex Maps Integration (November 2025)**

**Model Updates (`contacts/models.py`):**
- Added `latitude` field (DecimalField) for map coordinates
- Added `longitude` field (DecimalField) for map coordinates  
- Added `map_zoom` field (IntegerField, default=16) for zoom level
- Added `has_coordinates()` method to check if coordinates are set
- Kept `yandex_map_embed_code` as fallback option

**Admin Interface (`contacts/admin.py`):**
- Structured fieldsets for better UX:
  - "Основная информация" - clinic details
  - "Яндекс Карты - координаты" - lat/lng/zoom fields
  - "Яндекс Карты - альтернативный способ" - embed code fallback
- Added `has_coordinates` indicator in list display

**Template Integration:**
- Integrated Yandex Maps JavaScript API 2.1
- Interactive map with custom placemark (medical icon)
- Balloon popup with clinic info and "Build route" button
- **Fixed localization issue:** Used `{% load l10n %}` and `{% localize off %}` to prevent Russian locale from converting decimal points to commas in JavaScript
- Map displayed on both `/contacts/` and homepage
- Disabled scroll zoom for better page navigation

**Configured Coordinates:**
- Address: улица Ленина, 42А, Константиновск, Ростовская область, 347250
- Latitude: 47.577457
- Longitude: 41.100736
- Zoom: 17

**Files Modified:**
- `contacts/models.py` - Added coordinate fields
- `contacts/admin.py` - Structured admin with fieldsets
- `contacts/migrations/0002_*.py` - Migration for new fields
- `templates/contacts/contacts.html` - Yandex Maps JS integration
- `templates/home.html` - Map on homepage
- `static/css/style.css` - Map container styles

---

## Stage 2: Completed (November 2025)

### Docker Configuration Created

**Files Created:**
- `docker/django/Dockerfile` - Django container with Python 3.11, Gunicorn
- `docker/nginx/Dockerfile` - Nginx reverse proxy
- `docker/nginx/nginx.conf` - Nginx configuration for static files and proxy
- `docker-compose.yml` - Main orchestration file
- `entrypoint.sh` - Container startup script with migrations
- `.env.example` - Environment variables template
- `.dockerignore` - Docker build exclusions
- `Makefile` - Convenient commands for Docker management

**Settings Updated:**
- `clinic/settings.py` - Environment-based configuration (SQLite/PostgreSQL)
- `requirements.txt` - Added gunicorn, psycopg2-binary, python-dotenv, whitenoise

**Docker Services:**
- `db` - PostgreSQL 15 Alpine with health checks
- `web` - Django + Gunicorn (3 workers)
- `nginx` - Nginx 1.25 Alpine reverse proxy

**Commands Available:**
```bash
make build      # Build Docker images
make up         # Start all services
make down       # Stop all services
make logs       # View logs
make migrate    # Run migrations
make shell      # Django shell
make bash       # Container bash
```

**Access:**
- Website: http://localhost
- Admin: http://localhost/admin (admin / admin123)

---

## Stage 3: GitHub Actions & Deployment (November 2025)

### GitHub Actions Workflows Created

**CI Workflow (`.github/workflows/ci.yml`):**
- Runs on push to `main`/`develop` and pull requests
- Sets up PostgreSQL service for testing
- Lints code with flake8
- Runs Django checks and migrations
- Executes test suite
- Builds Docker image to verify Dockerfile

**Deploy Workflow (`.github/workflows/deploy.yml`):**
- Triggered on push to `main` or manually
- Runs tests before deployment
- Connects to server via SSH
- Pulls latest code, rebuilds containers
- Runs migrations and collects static files
- Cleans up old Docker images

### Production Configuration

**Files Created:**
- `.github/workflows/ci.yml` - CI pipeline
- `.github/workflows/deploy.yml` - Deployment pipeline
- `docker-compose.prod.yml` - Production Docker Compose
- `docker/nginx/nginx.prod.conf` - Production Nginx config
- `.env.prod.example` - Production environment template
- `scripts/server-setup.sh` - Server initialization script
- `scripts/backup-db.sh` - Database backup script
- `scripts/restore-db.sh` - Database restore script

### GitHub Secrets Required

Configure in: Repository → Settings → Secrets and variables → Actions

| Secret | Description |
|--------|-------------|
| `SERVER_HOST` | Server IP or domain |
| `SERVER_USER` | SSH username (default: `deploy`) |
| `SERVER_PORT` | SSH port (default: `22`) |
| `SSH_PRIVATE_KEY` | Private SSH key for authentication |

### Server Setup Instructions

1. **Provision server** (Ubuntu 22.04 LTS recommended)

2. **Run setup script:**
```bash
wget https://raw.githubusercontent.com/YOUR_USER/vetirinary/main/scripts/server-setup.sh
chmod +x server-setup.sh
sudo ./server-setup.sh
```

3. **Clone repository:**
```bash
sudo -u deploy git clone https://github.com/YOUR_USER/vetirinary.git /opt/vetclinic
```

4. **Configure environment:**
```bash
cd /opt/vetclinic
sudo -u deploy cp .env.prod.example .env.prod
sudo -u deploy nano .env.prod  # Edit with production values
```

5. **Generate SSH key for GitHub Actions:**
```bash
sudo -u deploy ssh-keygen -t ed25519 -C "github-actions" -f /home/deploy/.ssh/github_deploy -N ""
cat /home/deploy/.ssh/github_deploy.pub >> /home/deploy/.ssh/authorized_keys
cat /home/deploy/.ssh/github_deploy  # Add this to GitHub Secrets
```

6. **Set up SSL:**
```bash
sudo certbot --nginx -d your-domain.com
```

7. **Start application:**
```bash
cd /opt/vetclinic
sudo -u deploy docker-compose -f docker-compose.prod.yml up -d
```

### Backup Configuration

Add to crontab for automatic daily backups at 3 AM:
```bash
sudo -u deploy crontab -e
# Add line:
0 3 * * * /opt/vetclinic/scripts/backup-db.sh
```

### Architecture

```
[GitHub Repository]
        │
        ▼
[GitHub Actions CI/CD]
        │
        ├── Run tests (PostgreSQL)
        ├── Lint code
        └── Deploy via SSH
                │
                ▼
[Production Server (VPS)]
        │
        ├── Nginx (host) → SSL termination
        │       │
        │       ▼
        ├── Docker Compose
        │   ├── nginx (container) → reverse proxy
        │   ├── web (Django + Gunicorn)
        │   └── db (PostgreSQL)
        │
        └── Certbot (SSL auto-renewal)
```

### Deployment Checklist

- [x] GitHub Actions workflows created
- [x] Production Docker Compose configured
- [x] Server setup script created
- [x] Backup/restore scripts created
- [x] Server provisioned
- [x] GitHub Secrets configured
- [x] Domain DNS configured
- [x] SSL certificate obtained
- [x] First deployment completed

---

## AI Chatbot Assistant (December 2025)

### Overview

Added an AI-powered chat assistant widget available on all website pages. The assistant can:
- Answer questions about the clinic (address, hours, services, prices)
- Provide information about veterinarians
- Answer general veterinary questions
- Search the internet for veterinary topics (with restrictions)

### Technology Stack

- **LLM**: z-ai/glm-4.5-air:free via OpenRouter API
- **Framework**: LangChain + LangGraph for agentic capabilities
- **Search**: DuckDuckGo Search (restricted to veterinary topics)
- **Frontend**: Vanilla JavaScript chat widget with session storage

### Files Created

**New Django App: `chatbot/`**
- `chatbot/prompts.py` - System prompts with restrictions
- `chatbot/tools.py` - Custom tools for clinic data and search
- `chatbot/agent.py` - LangChain/LangGraph agent configuration
- `chatbot/views.py` - API endpoint for chat
- `chatbot/urls.py` - URL routing

**Frontend:**
- `static/js/chat-widget.js` - Chat widget JavaScript
- `static/css/chat-widget.css` - Widget styling

**Modified:**
- `templates/base.html` - Include widget on all pages
- `clinic/settings.py` - Add chatbot app and OpenRouter config
- `clinic/urls.py` - Add API route `/api/chatbot/chat/`
- `requirements.txt` - Add langchain, langchain-openai, duckduckgo-search

### Configuration

Set the `OPENROUTER_API_KEY` environment variable:
```bash
export OPENROUTER_API_KEY=your-api-key-here
```

Get your API key at: https://openrouter.ai/keys

### Features

1. **Floating Chat Widget**
   - Available on all pages (bottom-right corner)
   - Responsive design (mobile-friendly)
   - Session-based message history
   - Quick action buttons for common questions

2. **AI Capabilities**
   - Access to clinic database (contacts, services, veterinarians)
   - DuckDuckGo search for veterinary topics
   - Strict topic restrictions (veterinary only)
   - Critical analysis of search results

3. **Safety Features**
   - Only discusses veterinary topics
   - Never provides diagnoses or prescriptions
   - Always recommends consulting a real veterinarian
   - Search restricted to veterinary keywords

### API Endpoint

**POST** `/api/chatbot/chat/`

Request body:
```json
{
    "message": "User message",
    "history": [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]
}
```

---

## Frontend Text Refactoring (January 2026)

### Overview

Refactored the entire project to manage all frontend text through models, moving hardcoded strings from templates into a manageable and localizable system.

### Key Changes

1. **Centralized Common Text (`core/`)**
   - Created a new `core` app for site-wide settings and common phrases.
   - `SiteSettings`: Global site info (title, meta description, footer text, copyright).
   - `CommonPhrase`: Reusable text snippets (button labels, navigation items, section titles).
   - `HeroSection`: Content for the home page hero section.
   - `StatItem`: Statistics displayed on the home page.

2. **Thematic Text Management**
   - Added page-specific text models to existing apps:
     - `AboutPageText` (in `about`)
     - `ServicesPageText` (in `services`)
     - `NewsPageText` (in `news`)
     - `ReviewsPageText` (in `reviews`)
     - `ContactsPageText` (in `contacts`)
     - `FeatureItem` (in `about`)

3. **Context Processors**
   - Implemented `site_content` context processor in `clinic/context_processors.py`.
   - Provides global access to `site_settings` and `common_phrases` in all templates.

4. **Template Refactoring**
   - Refactored all 12 templates to use dynamic content from models.
   - Implemented graceful fallbacks using the `|default` filter.
   - Fixed minor JavaScript issues in `home.html` and `contacts/contacts.html`.

5. **Admin Interface**
   - Registered all new models in Django Admin.
   - Enforced singleton behavior for page-specific text models.
   - Organized fields for better usability.

### Files Created/Modified

- `core/` - New application
- `clinic/context_processors.py` - New context processor
- `clinic/settings.py` - Registered new app and context processor
- `*/models.py` - Added text models to all apps
- `*/admin.py` - Registered models and configured singleton behavior
- `*/views.py` - Updated views to pass text objects to templates
- `templates/*.html` - Refactored all templates